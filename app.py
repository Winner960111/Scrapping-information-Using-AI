import json
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
load_dotenv()
client = OpenAI()

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key = openai_api_key)

def extract_data_image(file_name):

    files = {"file": open(f"./data/{file_name}", 'rb')}
    url = "https://api.edenai.run/v2/ocr/ocr"
    data = {
        "providers": "google",
        "language": "en",
        "fallback_providers": ""
    }
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjM1MjUxOTQtMTUyMy00OTNhLTkxNzMtODNkYjcwOTc1NGM0IiwidHlwZSI6ImFwaV90b2tlbiJ9.plqIfgXVVxTvIuVrv-zGV1Vn-QCc7lbADOpFUeKPEao"}

    response = requests.post(url, data=data, files=files, headers=headers)

    result = json.loads(response.text)
    data = result["google"]["text"]

    extract_info = [
        {
            "type": "function",
            "function": {
                "name": "extracte_info",
                "description": "extract the essetial information from given text. If the same content is repeated, ignore that.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Extract the full name from given information.",
                        },
                        "job": {
                            "type": "string",
                            "description": "extract the job from given information. If this information is not exist, you should answer as empty.",
                        },
                        "height":{
                            "type":"string",
                            "description":"extract the height from given information. If this information is not exist, you should answer as empty."
                        },
                        "first_education":{
                            "type":"string",
                            "description":"Extract the first education information from given information. If this information is not exist, you should answer as empty.",
                        },
                        "second_education":{
                            "type":"string",
                            "description":"Extract the second education information from given information. If this information is not exist, you should answer as empty.",
                        },
                        "address":{
                            "type":"string",
                            "description":"extract the address information from given information. You should extract only the name of locaion. If this information is not exist, you should answer as empty."
                        },
                        "distance":{
                            "type":"string",
                            "description":"extract the distant information from given information. If this information is not exist, you should answer as empty."
                        },
                    },
                    "required": ["name", "job", "hight", "first_education", "second_education", "address", "distance"]
                },
            }
        }
    ]

    messages = [
        {"role": "system", "content": "Please extract the essential information from the data that is inputted by user. You should answer in all of question."},
        {"role": "user", "content": data}
        ]

    response = openai_client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        temperature=0,
        tools=extract_info,
    )

    return response.choices[0].message.tool_calls[0].function.arguments

# Directory path
directory = './data'
# Get a list of all files in the directory
file_name = os.listdir(directory)

for index, item in enumerate(file_name):
    res = extract_data_image(item)
    data = json.loads(res)
    print(f"{data}\n")
