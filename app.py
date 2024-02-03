import tempfile

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

    payload = json.dumps({
        "instances": [
            {
                "context": "you are a doctor talking to a 5 year old",
                "examples": [
                    {
                        "input": {
                            "content": "You have a temperature of 39 degree celcius"
                        },
                        "output": {
                            "content": "you will feel weak and tired. Feeling hot. "
                        }
                    }
                ],
                "messages": [
                    {
                        "author": "User",
                        "content": "No Trichomonas or Candida organisms are seen."
                    }
                ]
            }
        ]
    })
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


@app.route('/vertex2', methods=['POST'])
def run():
    import requests
    import json
    data = request.json
    question = data['question']
    # question = "Trichomonas or Candida organisms are seen."
    access_token = "ya29.a0AfB_byDbhKY2QPd2JcEcRFoWJA0BwoGCLGAFEvycn6t31_3fS8GFQnRjoEwarsPzzINDd5fdi_QG0PfMoc1HqJZdo68VdXMbyTsPqv8VExa5n1X670Odus8ypqvKIR1FEh2GiLcShaV_t2UqeWusIgXsf3tvgp_bC3amoFRFQXKzLyhpvcDuQVeySZjYJw1s6Zk99uBf_pXPEjgGDz1yUkcJeOfMkjqxdGuth4PKywwVYuUsgEoMfF-B-JF13sFckY57Oo4Vidau45RsmtNGI1-zdmQXH1-J4pvTwWZw5nCHSQURMTzUJjhXakO4w3sfNQIDwgemcH012JvPqHlUQf6L73UTOwy37IHlWdAZNifd1vrPMuJbh9-b721G-Elkh9ZCl_17zf788_Aw-jJ7BwN3Wv54yuIaCgYKAWoSARMSFQHGX2Migm_wU_JtE2wrmhqk_Rmhtg0422"
    url = "https://us-central1-aiplatform.googleapis.com/v1/projects/healthhack-412317/locations/us-central1/publishers/google/models/chat-bison:predict?access_token="+access_token

    payload = json.dumps({
        "instances": [
            {
                "context": "You are to explain medical reports to people who does not understand complex terms. Please breakdown the medical jargons and explain it to them as simply as you can. Explain if it is a positive or negative result",
                "examples": [
                    {
                        "input": {
                            "content": "No Trichomonas or Candida organisms are seen."
                        },
                        "output": {
                            "content": "These are organisms that cause infections. Trichomonas is a protozoan parasite causing the sexually transmitted infection trichomoniasis, primarily affecting the urogenital tract in both men and women.\
    While Candida is a genus of yeast, with Candida albicans being a common species that can cause various infections, including yeast infections in the genital or oral areas, skin, nails, and mucous membranes. "
                        }
                    }
                ],
                "messages": [
                    {
                        "author": "User",
                        "content": question
                    }
                ]
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code)
    if response.status_code ==200:
        response_json = response.json()
        print(response_json)
        print("--------")
        # print(response_json['predictions'][0]['candidates'][0]['content']) #only for deployed on render
        return (response_json['predictions'][0]['candidates'][0]['content'])
    else:
        return (response.text)


import argparse
# To read the PDF
import PyPDF2
# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
# To extract text from tables in PDF
import pdfplumber
# To remove the additional created files
import os
def text_extraction(element):
    print("Extracting text")
    line_text = element.get_text()
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    format_per_line = list(set(line_formats))
    return (line_text, format_per_line)

def extract_table(pdf_path, pagenum, table_num):
    print("Extracting table", pagenum, table_num)
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[pagenum]
    table = table_page.extract_tables()[table_num]
    return table

def table_converter(table):
    print("table",table)
    table_string = ''
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
    table_string = table_string[:-1]
    return table_string

def process_pdf(pdf_path):
    pdfFileObj = open(pdf_path, 'rb')
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)

    text_per_page = {}

    for pagenum, page in enumerate(extract_pages(pdf_path)):
        print("Processing page", pagenum + 1, "of", len(pdfReaded.pages))
        pageObj = pdfReaded.pages[pagenum]
        page_text = []
        text_from_tables = []
        page_content = []
        table_num = 0
        first_element = True
        table_extraction_flag = False
        pdf = pdfplumber.open(pdf_path)
        page_tables = pdf.pages[pagenum]
        tables = page_tables.find_tables()

        page_elements = [(element.y1, element) for element in page._objs]
        page_elements.sort(key=lambda a: a[0], reverse=True)

        for i, component in enumerate(page_elements):
            print("Processing component", i + 1, "of", len(page_elements))
            pos = component[0]
            element = component[1]

            if isinstance(element, LTTextContainer):
                if not table_extraction_flag:
                    (line_text, format_per_line) = text_extraction(element)
                    page_text.append(line_text)
                    page_content.append(line_text)
                else:
                    pass

            if isinstance(element, LTRect):
                if first_element and (table_num + 1) <= len(tables):
                    lower_side = page.bbox[3] - tables[table_num].bbox[3]
                    upper_side = element.y1
                    table = extract_table(pdf_path, pagenum, table_num)
                    table_string = table_converter(table)
                    text_from_tables.append(table_string)
                    page_content.append(table_string)
                    table_extraction_flag = True
                    first_element = False
                if element.y0 >= lower_side and element.y1 <= upper_side:
                    pass
                elif not isinstance(page_elements[i + 1][1], LTRect):
                    table_extraction_flag = False
                    first_element = True
                    table_num += 1

        dctkey = 'Page_' + str(pagenum)
        text_per_page[dctkey] = [page_text, text_from_tables, page_content]

    pdfFileObj.close()

    result_text = ""
    print("Creating result text", len(text_per_page))
    for page_key in text_per_page:
        print("Processing page", page_key)
        page_content = ''.join(text_per_page[page_key][2])
        result_text += f"Page: {page_key}\n"
        result_text += page_content
        result_text += "\n\n"
        print(result_text)

    return result_text

@app.route('/process_pdf', methods=['POST'])
def process_pdf_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    print("File received")

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        temp_pdf, temp_pdf_path = tempfile.mkstemp(suffix=".pdf")
        file.save(temp_pdf_path)
        print("File saved")
        result_text = process_pdf(temp_pdf_path)
        print("File processed", result_text)
        # os.remove(temp_pdf_path)
        print(jsonify({'result': result_text}))
        return jsonify({'result': result_text})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})
if __name__ == '__main__':
    app.run()
