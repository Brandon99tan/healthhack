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
def buildheader_body():
    accesstoken = "ya29.a0AfB_byBaYuMqumy8XMdZ-Xl66pfTcj_uUj0fMm6u81PB5RCro6iN_rZZeyuUFiNI40BCcQYFTgumbTbkpPqLJ9oaKcjoj9l1snRREzwzQUiI0M771loIoIIoNrRI4UQ6BRJ46gSy9Jg1TQVmRJwsAKoKWEvpc6emI86YjBvns65CgbT5I-D01WFm0jZht4r5Udg6JK1zsSC8fl7Ct2vnwc7Txl_KG38VAiAQkCT51mJ1DpRKE9CfiUI7e52GH05atMgAgtAIqEmrXfxHo45AzX-vq-mTdFNQ4T8OqLWHCAnuLdWnGg0-lTZkYLyZnczt1db2N5psoggwiD6rC6t1vjNJY2DHqqlPwuf5jhfuF69ezW4KxYcGDBx5dqXxlaJ5H_HjvhUogVoCU1sonyjH7OwdW2YP6rkaCgYKAU4SARMSFQHGX2MikYA-WIcNdTDOMFK8-S0mlQ0422"
    url = "https://us-central1-aiplatform.googleapis.com/v1/projects/healthhack-412317/locations/us-central1/publishers/google/models/text-bison:predict?access_token="+accesstoken
    payload ={
        "instances": [
            {
                "context": "You are to explain medical reports to people who does not understand complex terms. Please breakdown the medical jargons and explain it to them as simply as you can. Explain if it is a positive or negative result",
                "examples": [
                    {
                        "input": {
                            "author": "user",
                            "content": "No Trichomonas or Candida organisms are seen."
                        },
                        "output": {
                            "author": "bot",
                            "content": "These are organisms that cause infections. Trichomonas is a protozoan parasite causing the sexually transmitted infection trichomoniasis, primarily affecting the urogenital tract in both men and women.\
        While Candida is a genus of yeast, with Candida albicans being a common species that can cause various infections, including yeast infections in the genital or oral areas, skin, nails, and mucous membranes"
                        }
                    }
                ],
                "messages": [
                    {
                        "author": "user",
                        "content": "Trichomonas or Candida organisms are seen."
                    }
                ]
            }
        ],
        "parameters": {
            "candidateCount": 1,
            "maxOutputTokens": 1024,
            "temperature": 0.9,
            "topP": 1
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text



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
