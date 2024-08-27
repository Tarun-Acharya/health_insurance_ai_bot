import argparse
from langchain_community.vectorstores.chroma import Chroma
from langchain.prompts import PromptTemplate
from llm_configs import get_embedding_function, get_model


CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question in detail based on the above context: {question}
"""


def main():
    # Create CLI.
    # parser = argparse.ArgumentParser()
    # parser.add_argument("query_text", type=str, help="The query text.")
    # args = parser.parse_args()
    # query_text = args.query_text
    while 1:
        query_text = input("\nAsk a question\n>>>")
        if query_text == "exit":
            exit()
        query_rag(query_text)


def get_vector_db(embedding_function):
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    vectordb = get_vector_db(embedding_function)
    # Search the DB.
    results = vectordb.similarity_search_with_score(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    prompt_template = PromptTemplate.from_template(template=PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    messages = [
        {"role": "user", "content": prompt},
    ]

    model = get_model("llama3-trained")

    # tokenizer, model = get_model("llama3-trained")
    # inputs = tokenizer.apply_chat_template(
    #     messages,
    #     tokenize=True,
    #     add_generation_prompt=True,  # Must add for generation
    #     return_tensors="pt",
    # )

    # response_text = model(context=context_text, question=query_text, max_seq_len=500)
    # from transformers import TextStreamer

    # text_streamer = TextStreamer(tokenizer)
    # response_text = model.generate(
    #     input_ids=inputs, streamer=text_streamer, max_new_tokens=256, use_cache=True
    # )
    response_text = model.invoke(prompt)

    # _ =
    # print(response_text)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()
