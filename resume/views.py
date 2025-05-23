from django.shortcuts import render
from rest_framework import mixins, viewsets, status
# Create your views here.
import PyPDF2
import docx
from resume.models import ResumeFeedback
from resume.serializers import ResumeFeedbackSerializer
from rest_framework.response import Response

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

from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

generator = pipeline(
    "text-generation",
    model="gpt2",
    max_new_tokens=200)

llm = HuggingFacePipeline(pipeline=generator)

prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
Evaluate the following resume using this rubric:
- Skills match (out of 10)
- Clarity and grammar (out of 10)
- Formatting (out of 10)
- Soft skills demonstrated (out of 10)

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

        feedback = resume_chain.run(resume=resume_text)

        instance = ResumeFeedback.objects.create(
            resume_file=resume_file,
            feedback=feedback
        )

        
        output = self.get_serializer(instance)
        return Response(output.data, status=status.HTTP_201_CREATED)