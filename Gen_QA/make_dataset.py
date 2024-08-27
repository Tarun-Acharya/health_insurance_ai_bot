# Tip: By now, install transformers from source
import warnings
import sys
import json
import random
import os
import glob

warnings.filterwarnings("ignore")
from transformers import AutoModelWithLMHead, AutoTokenizer
from Gen_QA.get_pdf_text import get_chunks

tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/t5-base-finetuned-question-generation-ap", use_fast=False, legacy=False
)
model = AutoModelWithLMHead.from_pretrained(
    "mrm8488/t5-base-finetuned-question-generation-ap"
)


def main():
    DIR_NAME = sys.argv[1]
    result_object = []
    pdf_files = glob.glob(os.path.join(DIR_NAME, "*.pdf"))
    for filename in pdf_files:
        chunks = get_chunks(filename)
        json_object = []
        for chunk in chunks:
            context = chunk.page_content
            item = {"context": context, "answer": ""}
            json_object.append(item)
        random.shuffle(json_object)
        result_object.extend(random.sample(json_object, min(len(json_object), 8)))
    dataset = "output.json"

    # Write the list of dictionaries to a JSON file
    with open(dataset, "w", encoding="utf8") as json_file:
        json.dump(result_object, json_file, indent=4, ensure_ascii=False)


def get_question(answer, context, max_length=100):
    input_text = "answer: %s  context: %s </s>" % (answer, context)
    features = tokenizer([input_text], return_tensors="pt")
    # print(features)

    output = model.generate(
        input_ids=features["input_ids"],
        attention_mask=features["attention_mask"],
        max_length=max_length,
    )
    return tokenizer.decode(output[0])


context = """Monthly rates
            OPTima Basic  OPTima Enhanced  
            18-24 $39 $79 
            25-29 $69 $109 
            30-64 $119  $179"""
answer = "$109"

print(get_question(answer, context))

# output: question: Who created the RuPERTa-base?
if __name__ == "__main__":
    main()
