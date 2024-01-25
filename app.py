from flask import Flask, request, jsonify
import vertexai
import googleapiclient
import os
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return "gigi"

@app.route('/vertex', methods=['GET'])
def vertex(candidate_count=1, max_output_tokens=1024, temperature=0.9, top_p=1):
    print("vertex")
    from vertexai.language_models import ChatModel, InputOutputTextPair
    req = str(request.args.get("q"))
    print(req)
    User = os.environ['USER']
    Pass = os.environ['PASS']

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
