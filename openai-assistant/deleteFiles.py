from openai import OpenAI
import time
import os
import json

with open('config.json', 'r') as json_file:
    config = json.load(json_file)

os.environ['OPENAI_API_KEY'] =config['api_key']
os.getenv('OPENAI_API_KEY')
client = OpenAI()
count = 0
for file in client.files.list():
    if count==60:
        print("60 File Limit Reached. Waiting.........")
        time.sleep(60)
        count=0
    client.files.delete(file.id)
    count+=1
    print(f"{count} File {file.id} deleted.")
    