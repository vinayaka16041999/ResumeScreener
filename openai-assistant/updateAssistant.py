#!/usr/bin/env python
# coding: utf-8

from openai import OpenAI
import os
import openai
import json
import sys

with open('config.json', 'r') as json_file:
    config = json.load(json_file)

os.environ['OPENAI_API_KEY'] =config['api_key']
os.getenv('OPENAI_API_KEY')
client = OpenAI()

metadata = config['metadata_path'] + "\\" + "assistants.json"

with open(metadata, "r") as json_file:
    assistants = json.load(json_file)


def update_assistant(new_file_path_list):
    for new_file_path in new_file_path_list:
        assistant_name = new_file_path.split("\\")[-1][:-5]
        assistant_id = assistants[assistant_name]
        file = client.files.create(
            file=open(new_file_path, "rb"),
            purpose='assistants')
        new_file_id = file.id
        response = client.beta.assistants.update(
        assistant_id=assistant_id)
        old_file_ids = response.file_ids
        for old_file_id in old_file_ids:
            client.files.delete(old_file_id)
        print(f"Assistant {assistant_name} with ID {assistant_id} updated.")
        client.beta.assistants.update(
        assistant_id=assistant_id,
        file_ids = [new_file_id])





