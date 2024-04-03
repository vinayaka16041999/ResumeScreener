#!/usr/bin/env python
# coding: utf-8


from openai import OpenAI
import os
import openai
import json
import time

with open('config.json', 'r') as json_file:
    config = json.load(json_file)

os.environ['OPENAI_API_KEY'] =config['api_key']
os.getenv('OPENAI_API_KEY')
client = OpenAI()
instructions="""
The structure of the knowledge file is a json file where keys are the resume file names and values are the resume content as string.

You will be provided with various queries related to candidates whose resumes are stored in knowledge files.

Your queries will be mainly to shortlist or select the best candidates for a given requirement.

Canculate the candidate score out of 100 based on their skills, experience, certification and education.

Provide the output in below format
-Candidate Name:
-Candidate Score:
-Candidate's Strengths:
-Candidate's Weakness:
-Candidate's short summary:

"""




def get_assistant_ids(path):
    assistant_mapping = {}
    for filename in os.listdir(path):
        file_path = os.path.join(path,filename)
        assistant_name = filename[:-5]
        print(f"Creating assistant {assistant_name} with gpt-3.5-turbo-1106, Retrieval configurations.")
        file = client.files.create(
            file=open(file_path, "rb"),
            purpose='assistants')
        assistant = client.beta.assistants.create(
            name = assistant_name,
            instructions=instructions,
            model=config['assistant_model_name'],
            tools=[{"type": "retrieval"}],
            file_ids=[file.id])
        assistant_mapping[assistant_name] = assistant.id
    assistant = client.beta.assistants.create(
            name = "Default",
            instructions="",
            model=config['assistant_model_name'])
    assistant_mapping['Default'] = assistant.id
    file_path = config['metadata_path'] +"\\assistants.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(assistant_mapping, json_file)


def delete_assistants():
    try:
        count = 0
        for assistant in client.beta.assistants.list():
            if count==60:
                print("60 Assistant Limit Reached. Waiting.........")
                time.sleep(60)
                count=0
            print(f"{count} Assistant {assistant.id} deleted.")
            client.beta.assistants.delete(assistant.id)
            count+=1
    except:
        print("All assistants deleted!")



#delete_assistants()



def delete_files():
    try:
        count = 0
        for file in client.files.list():
            if count==60:
                print("60 File Limit Reached. Waiting.........")
                time.sleep(60)
                count=0
            print(f"{count} File {file.id} deleted.")
            client.files.delete(file.id)
            count+=1
    except Exception as e:
        print("")



#delete_files()





