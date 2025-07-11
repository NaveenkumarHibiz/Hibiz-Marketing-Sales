import requests
from bs4 import BeautifulSoup
import os
import ollama
import json
from pinecone import Pinecone
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import json
import time
import pandas as pd
from openai import OpenAI
import ollama
import datetime
from jinja2 import Template
import os
from openai import OpenAI
from openai import AzureOpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

PINECONE_HOST_URL = os.getenv("PINECONE_HOST_URL")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HOME_URL = os.getenv("HOME_URL")
SERVICES_URL = os.getenv("SERVICES_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host = PINECONE_HOST_URL)

client = OpenAI(api_key=OPENAI_API_KEY)
# EMBEDDINGS = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07", google_api_key=GOOGLE_API_KEY)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


# Parse the HTML content


def get_openai_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

# def get_gemini_embedding(chunk_data):
#     vector = EMBEDDINGS.embed_query(chunk_data, output_dimensionality = 1536)
#     return vector


with open("prompt_template.md", "r", encoding="utf-8") as f:
    template_text = f.read()

# Create Jinja2 template
template = Template(template_text)

#get partners of the company


#get testimonials
def search_testimonials(search_vector):
    match_results = index.query(
        namespace="testimonials",
        vector=search_vector, 
        top_k=2,
        include_metadata=True,
        include_values=False
    )
    print("\Testimonials retrieval successful")
    return match_results

#get certifications
def search_certifications(search_vector):
    match_results = index.query(
        namespace="certifications",
        vector=search_vector, 
        top_k=15,
        include_metadata=True,
        include_values=False
    )
    print("\nCertifications retrieval successful")
    return match_results

#get services offered by the company
def get_services_provided(URL):
    response = requests.get(URL, headers=headers)
    #service_response = requests.get(os.getenv("SERVICES_URL"), headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    #service_soup = BeautifulSoup(service_response.text, 'html.parser')
    services_content = soup.find_all('h2', class_ = "elementor-heading-title elementor-size-default")
    print(len(services_content))

    services_provided = []
    for tag in services_content:
        services_provided.append(tag.get_text(strip=True))
    return services_provided  

#------------------------------------------------------------------------
      
# Initialize Azure OpenAI client with Entra ID authentication

client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_version="2025-01-01-preview",
)

def get_prompt_response(user_input, service_url, client):
    final_prompt = template.render(
        user_input=user_input,
        services=get_services_provided(service_url),
        testimonial_data=search_testimonials(get_openai_embedding(user_input)),
        certification_data=search_certifications(get_openai_embedding(user_input))
    )
    response = client.chat.completions.create(  
        model = 'gpt-4.1', 
        temperature= 0.6,
        frequency_penalty=0,
        presence_penalty=0,
        messages=[
            {"role": "system", "content":final_prompt},

      ]
    )
    content = response.choices[0].message.content.strip()

    #call the response model
    print(content)
    return content


# 🎯 UI Title
st.title("🧠 PRIDE Prompt Assistant")

# 📝 User input
user_input = st.text_area("Enter your prompt/question below:", height=150)

# 🚀 On button click
if st.button("Generate Response"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Generating response..."):
            response = get_prompt_response(user_input, HOME_URL, client)
        # 📄 Display as markdown
        st.markdown(response)
