from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from django.conf import settings
import PyPDF2
import docx
from resume.models import ResumeFeedback, CorrectedResume
from resume.serializers import ResumeFeedbackSerializer, CorrectedResumeSerializer
from rest_framework.response import Response
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import torch
import warnings
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser
import threading





def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# HUGGINGFACE_TOKEN=settings.HUGGINGFACE_TOKEN

                                                         #PROMPT FOR GRADING RESUME
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it")

generator = pipeline(
    "text-generation",
    model=model,
    device=-1,
    tokenizer=tokenizer,
    max_new_tokens=300,
    temperature=0.7,
    )

llm = HuggingFacePipeline(pipeline=generator)

prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
Evaluate the following resume using this rubric:
- Skills match (out of 10)
- Clarity and grammar (out of 10)
- Formatting (out of 10)
- Soft skills demonstrated (out of 10)
- Give job suggestions

Give a total score, and then explain each sub-score briefly.

Resume:
{resume}
"""
)


                                        #PROMPT FOR CORRECTING THE RESUME

correction_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
You are an expert resume editor.

Please revise the following resume to improve:
- Grammar and spelling
- Sentence clarity
- Professional tone and formatting

Only return the improved resume text. Do not explain your changes. Do not summarize.

Resume:
{resume}
"""
)

resume_chain = prompt | llm
correct_resume_chain = correction_prompt | llm


def generate_resume_feedback(text: str):
    return resume_chain.invoke({"resume": text})

def generate_corrected_resume(text: str):
    return correct_resume_chain.invoke({"resume": text})


def grade_resume_and_notify(user_email, feedback_url):
    send_mail(
        subject="✅ Your Resume Has Been Graded!",
        message=f"Hello!\n\nYour resume has been successfully graded. You can view the feedback here:\n\n{feedback_url}",
        from_email="noreply@yourdomain.com",
        recipient_list=[user_email],
        fail_silently=False,
    )

class ResumeViewSet(mixins.RetrieveModelMixin,mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ResumeFeedback.objects.all()
    serializer_class = ResumeFeedbackSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 

    def get_queryset(self):
        return ResumeFeedback.objects.filter(user=self.request.user)



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resume_file = serializer.validated_data["resume_file"]
        file_name = resume_file.name.lower()

        if file_name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_file)
        elif file_name.endswith(".docx"):
            resume_text = extract_text_from_docx(resume_file)
        else:
            return Response(
                {"error": "Unsupported file format. Please upload PDF or DOCX."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ai_response = generate_resume_feedback(resume_text)
        prompt_text = prompt.format(resume=resume_text).strip()
        feedback = ai_response.replace(prompt_text, "").strip()

        instance = ResumeFeedback.objects.create(
            resume_file=resume_file,
            feedback=feedback,
            user = request.user
        )

        feedback_url = f"http://localhost:8000/resume/{instance.id}/"


        threading.Thread(
            target=grade_resume_and_notify,
            args=(request.user.email, feedback_url)
        ).start()

        output = self.get_serializer(instance)
        return Response(output.data, status=status.HTTP_201_CREATED)
    





    
class CorrectedResumeViewset(mixins.RetrieveModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = CorrectedResume.objects.all()
    serializer_class = CorrectedResumeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return CorrectedResume.objects.filter(user=self.request.user)

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        original_resume = serializer.validated_data['original_resume']
        file_name = original_resume.name.lower()
        if file_name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(original_resume)
        elif file_name.endswith(".docx"):
            resume_text = extract_text_from_docx(original_resume)
        else:
            return Response(
                {"error": "Unsupported file format. Please upload PDF or DOCX."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        ai_response = generate_corrected_resume(resume_text)

        instance = CorrectedResume.objects.create(
            user = request.user,
            corrected_resume_text = ai_response,
            original_resume=original_resume

        )


        feedback_url = f"http://localhost:8000/corrected/{instance.id}/"

        
        threading.Thread(
            target=grade_resume_and_notify,
            args=(request.user.email, feedback_url)
        ).start()

        output = self.get_serializer(instance)
        return Response(output.data, status=status.HTTP_201_CREATED)




warnings.filterwarnings("ignore", category=UserWarning)
