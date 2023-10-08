import json
from difflib import get_close_matches
import gradio as gr
ans = ""
def load_knowledge_base(file_path:str) -> dict:
    with open(file_path,'r') as file:
        data: dict = json.load(file)
    return data

def save_knowldege_base(file_path:str,data:dict):
    with open(file_path,'w') as file:
        json.dump(data,file,indent=2)

def find_best_match(user_question:str,questions:list[str]) -> str|None:
    matches:list = get_close_matches(user_question,questions,n=1,cutoff=0.1)
    return matches[0] if matches else None

def get_answer_for_question(question:str,knowledge_base:dict) -> str|None:
    for q in knowledge_base["questions"]:
        if q["questions"] == question:
            return q["answer"]
        
def chat_bot(input):
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
        # for training purpose only
"""        else:
            print("Can you please teach me the answer to the question: ")
            new_answer = input("Please input the answer: ")
            knowledge_base["questions"].append({"questions":user_input,"answer":new_answer})
            save_knowldege_base('knowledge_base.json',knowledge_base)"""
    

gr.Interface(fn=chat_bot,
             inputs=gr.inputs.Textbox(lines=3, label="You:"), 
             outputs=gr.outputs.Textbox(label="DigitalSavvy: "), 
             title="Digital India",
             description="Inquire anything regarding Digital India: ",
             theme="shivi/calm_seafoam").launch(share=True)