import argparse
import os
import sys
import shutil

# from health_insurance_ai.llm_configs import get_embedding_function
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

# FILE_NAME = "ISO.pdf"
DATA_PATH = "./Read_DIR"
CHROMA_PATH = "./chroma"


def get_chunks(filename):

    # Check if the database should be cleared (using the --clear flag).
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--reset", action="store_true", help="Reset the database.")
    # args = parser.parse_args()
    # FILE_NAME = sys.argv[1]

    # Create (or update) the data store.
    documents = load_document(filename)
    # print(documents)
    chunks = split_documents(documents)
    return chunks
    # add_to_chroma(chunks)


def load_document(FILE_PATH):
    print(FILE_PATH)
    document_loader = PyPDFLoader(FILE_PATH)
    return document_loader.load()


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


if __name__ == "__main__":
    get_chunks(sys.argv[1])
