import json
from difflib import get_close_matches
import gradio as gr
import openai


ans = ""
def load_knowledge_base(file_path:str) -> dict:
    with open(file_path,'r') as file:
        data: dict = json.load(file)
    return data

def save_knowldege_base(file_path:str,data:dict):
    with open(file_path,'w') as file:
        json.dump(data,file,indent=2)

def find_best_match(user_question:str,questions:list[str]) -> str|None:
    matches:list = get_close_matches(user_question,questions,n=1,cutoff=0.7)
    return matches[0] if matches else None

def get_answer_for_question(question:str,knowledge_base:dict) -> str|None:
    for q in knowledge_base["questions"]:
        if q["questions"] == question:
            return q["answer"]
        
def chat_bot(input, history):
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input:str = input
        if user_input.lower() == "quite":
            break
        best_match: str | None = find_best_match(user_input, [q["questions"] for q in knowledge_base["questions"]])

        if best_match:
            answer:str = get_answer_for_question(best_match,knowledge_base)
            x = answer
            return x
        else:
            messages = []
            openai.api_key = "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"
            messages.append({"role": "user", "content": input})
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
            reply = response["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": reply})
            knowledge_base["questions"].append({"questions":user_input,"answer":reply})
            save_knowldege_base('knowledge_base.json',knowledge_base)
            return reply
        # for training purpose only
"""        else:
            print("Can you please teach me the answer to the question: ")
            new_answer = input("Please input the answer: ")
            knowledge_base["questions"].append({"questions":user_input,"answer":new_answer})
            save_knowldege_base('knowledge_base.json',knowledge_base)"""



gr.ChatInterface(
    chat_bot,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7),
    title="Digital India",
    description="Ask Digitalsavvy any question",
    theme="soft",
    examples=["Hello", "What is digital India?", "What is digilocker?"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
).launch(share=True)