from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
import os


def get_model(model_name):
    if model_name == "llama3":
        return Ollama(model="llama3")
    if model_name == "gemma2":
        return Ollama(model="gemma2")
    if model_name == "llama3-trained":
        return Ollama(model="unsloth_model")


def get_embedding_function():
    embeddings = OllamaEmbeddings(model="llama3")
    return embeddings


# def get_prompt(model_name):
#     if model_name == "layoutlm":
#         # context = (

#         # )
#         # question =

#         prompt = {
#             "inputs": {
#                 "question": "This is an example invoice document text with the invoice number 12345",
#                 "context": "What is the invoice number?",
#             }
#         }

#         return prompt
