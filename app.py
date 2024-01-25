from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:

        ## Convert the pdf to image
        images= pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        #convert to bytes to return pdf parts
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format="JPEG")
        img_byte_arr =img_byte_arr.getvalue()

        pdf_parts = [{
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() ## encode to base 64
            }]
            
        return pdf_parts
    else:
       raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key='input')
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1=st.button("Tell me about the resume")
submit2=st.button("How can I improvise my skills")
submit3=st.button("Percentage match")
submit4=st.button("Keywords Missing")

input_prompt1="""
You are an expereinced HR with Tech Experience in the field of any one job role from Data Science, Full Stack Web Devlopment, 
Big Data Engineering, Devops, Data Analytics, Machine Learning, Deep Learning, your task is to reveiw
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weakness of the applicant in relation to the specified job requirements in
job description.
"""

input_prompt2="""
You are an expereinced HR with Tech Experience in the field of any one job role from Data Science, Full Stack Web Devlopment, 
Big Data Engineering, Devops, Data Analytics, Machine Learning, Deep Learning, your role is to scrutinize
the job resume in the light of the job description provided.
Share your insights on the candidate's suitability for the role from an HR Perspective 
"""
 
input_prompt3="""
You are an skilled ATS(Application Tracking System) scanner with a deep understanding of any one job role from data science,
Full Stack Web Devlopment, Big Data Engineering, Devops, Data Analytics, Machine Learning, Deep Learning
and Deep ATS Functionality, your task is to evaluate the resume against the provided job description,
give me the percentage match if the resume matches the job description. First the output should come as
percentage an then keywords missing and last final thoughts.
"""

input_prompt4="""
You are an skilled ATS(Application Tracking System) scanner with a deep understanding of any one job role from data science,
Full Stack Web Devlopment, Big Data Engineering, Devops, Data Analytics, Machine Learning, Deep Learning
and Deep ATS Functionality, your task is to evaluate the resume against the provided job description,
give me the keywords missing if the resume not matches or matches the job description.The output should come as the name of
keywords missing one by one .
"""
if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif  submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
