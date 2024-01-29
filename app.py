import google.auth
from flask import Flask, request, jsonify
import vertexai
import googleapiclient
import requests
import json
import os
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return "gigi"
@app.route('/send')
def buildheader_body(text):
    headers = {}
    accesstoken = "ya29.a0AfB_byDIEiPoS3tbfmEqLP2wzoFv4sYYJt3ZA9SEyx_qErPorm-OIteBpHjD2zBD6rMMbXA3yDBLTXwGD_DzP1X4UMTyxOpecJ-A68v4hCKDvBPeFp87u064n8JK7vykcgXJTcHUBWSvfLWMaY89QglQEP78OedH4XPY33nLYjIQpNXSF28q5NivP_2Q4F2ylgdTU-Me2k00rfcFFJquxDHxVVRz5N0-I7ZKa4kLB1EYzs2-7S-slZfTDhW4TBlchrW-PBme47XYvs-82DfFSIGgVFEHjcc-AdO7tLYAe_omsUXgI7P7fuVxG32KdvfTNoyG3mq2-R4TXx8PAnhY9n3V4SjYnhh9LT83m3MfDrwakDNlH9JAFNUPGEFXNH_I7XgIUIkd4qvaJph0buzokkRjF3OwEAAaCgYKAX4SARMSFQHGX2MiDH0Af_bjx4myUcriX7q2ug0422"
    url = "https://us-central1-aiplatform.googleapis.com/v1/projects/healthhack-412317/locations/us-central1/publishers/google/models/text-bison:predict?access_token="+accesstoken
    payload = json.dumps({
        "instances": [
            {
                "prompt": "Give me ten interview questions for the role of program manager."
            }
        ],
        "parameters": {
            "temperature": 0.2,
            "maxOutputTokens": 256,
            "topK": 40,
            "topP": 0.95,
            "logprobs": 2
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response



@app.route('/vertex', methods=['GET'])
def vertex(candidate_count=1, max_output_tokens=1024, temperature=0.9, top_p=1):


    print("vertex")
    from vertexai.language_models import ChatModel, InputOutputTextPair
    req = str(request.args.get("q"))
    print(req)
    User = os.environ['USER']
    Pass = os.environ['PASS']
    print(User, Pass)
    vertexai.init(project="fyp-ntu", location="us-central1")
    chat_model = ChatModel.from_pretrained("chat-bison")
    parameters = { #these are default param
        "candidate_count": candidate_count,
        "max_output_tokens": max_output_tokens,
        "temperature": temperature,
        "top_p": top_p
    }
    chat = chat_model.start_chat(
        context="""You are to explain medical reports to people who does not understand complex terms. Please breakdown the medical jargons and explain it to them as simply as you can. Explain if it is a positive or negative result""",
        examples=[
            InputOutputTextPair(
                input_text="""No Trichomonas or Candida organisms are seen.""",
                output_text="""These are organisms that cause infections. Trichomonas is a protozoan parasite causing the sexually transmitted infection trichomoniasis, primarily affecting the urogenital tract in both men and women.
    While Candida is a genus of yeast, with Candida albicans being a common species that can cause various infections, including yeast infections in the genital or oral areas, skin, nails, and mucous membranes."""
            )
        ]
    )
    response = chat.send_message(req, **parameters)
    return (f"Response from Model LOL: {response.text}")
if __name__ == '__main__':
    app.run()
