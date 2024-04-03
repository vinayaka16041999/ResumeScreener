#!/usr/bin/env python
# coding: utf-8

# In[73]:


from openai import OpenAI
import os
import openai
import json
import sys

with open('config.json', 'r') as json_file:
    config = json.load(json_file)

os.environ['OPENAI_API_KEY'] = config['api_key']
os.getenv('OPENAI_API_KEY')
client = OpenAI()
instructions="for any prompt only return the closest label"


delimiter = "####"
system_message = f"""
You will be provided with user queries. \
The customer service query will be delimited with \
{delimiter} characters.
Classify each query into a primary category based on which technology the query is about
Provide your output in json format with the key: resp
 
Primary categories: .Net Developer - Any and all Web Development related technologies, 
Data Engineer - Any and all ETL and Cloud related technologies, 
Drupal Developer - Any and all Drupal related technologies, 
Power BI - Any and all Business Intelligence and Reporting related technologies,
Project Manager - Any and all project management related queries, 
Sharepoint Developer - Any and all Sharepoint related technologies,
Default - For anything that dosent match the above categories.
"""

metadata = config['metadata_path'] + "\\assistants.json"

def get_completion_from_messages(messages, model=config['cc_model_name'], temperature=0, max_tokens=config['max_tokens']):
 response = client.chat.completions.create(
   model=model,
   messages=messages,
   temperature=temperature, 
   max_tokens=max_tokens,
 )
 return response.choices[0].message.content

def get_assistantID(msg):
  messages =  [  
  {'role':'system', 
  'content': system_message},    
  {'role':'user', 
  'content': f"{delimiter}{msg}{delimiter}"},  ] 
  response = json.loads(get_completion_from_messages(messages))
  with open(metadata, "r") as json_file:
    assistants = json.load(json_file)
  assistant_name = response['resp']
  assistant_id = assistants[response['resp']]
  return assistant_id



