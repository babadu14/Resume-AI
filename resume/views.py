from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from django.conf import settings
import PyPDF2
import docx
from resume.models import ResumeFeedback
from resume.serializers import ResumeFeedbackSerializer
from rest_framework.response import Response
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import torch
from huggingface_hub import login
import warnings





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

HUGGINGFACE_TOKEN=settings.HUGGINGFACE_TOKEN

login(token=HUGGINGFACE_TOKEN)

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it", token=HUGGINGFACE_TOKEN)
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it", token=HUGGINGFACE_TOKEN, torch_dtype=torch.float32)

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

resume_chain = LLMChain(llm=llm, prompt=prompt)

def generate_resume_feedback(text: str) -> str:
    return resume_chain.run(resume=text)

class ResumeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ResumeFeedback.objects.all()
    serializer_class = ResumeFeedbackSerializer

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

        feedback = generate_resume_feedback(resume_text)

        instance = ResumeFeedback.objects.create(
            resume_file=resume_file,
            feedback=feedback
        )

        
        output = self.get_serializer(instance)
        return Response(output.data, status=status.HTTP_201_CREATED)
    

warnings.filterwarnings("ignore", category=UserWarning)
