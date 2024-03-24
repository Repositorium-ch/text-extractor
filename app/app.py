import json
import requests
import flask
import io
import os
from flask import request, jsonify
from waitress import serve
from unstructured.partition.pdf import partition_pdf

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def run_unstructured(file):
    elements = partition_pdf(file=file)
    arr = []
    for element in elements:
        dict = element.metadata.to_dict()
        dict["text"] = element.text
        arr.append(dict)
    return json.dumps(arr)

def is_api_ok(api_key):
    correct = os.getenv('API_KEY')
    print('good api key: ' + correct)
    return api_key == correct

@app.route('/', methods=['GET'])
def home():
  return '''
<h1>Submit URL</h1>
<p>Send a PDF link to get text parts</p>
<form action="/byurl" method="POST">
    <label for="url">URL:</label><br>
    <input type="text" id="url" name="url" value=""><br>
    <label for="api_key">API KEY:</label><br>
    <input type="text" id="api_key" name="api_key" value=""><br>
    <input type="submit" value="Submit">
</form>
<br/>
<p>Send a PDF link to get JSON (Derulo) parts:</p>
<form action="/api/byurl" method="POST">
    <label for="url">URL:</label><br>
    <input type="text" id="url" name="url" value=""><br>
    <label for="api_key">API KEY:</label><br>
    <input type="text" id="api_key" name="api_key" value=""><br>
    <input type="submit" value="Submit">
</form> 

<h1>PDF-Upload</h1>
<p>Upload a PDF to get text parts</p>
<form action = "/upload" method = "post" enctype="multipart/form-data">   
    <input type="file" name="file" /><br/>
    <label for="api_key">API KEY:</label><br>
    <input type="text" id="api_key" name="api_key" value=""><br>
    <input type = "submit" value="Upload">   
</form>
<br/>
<p>Upload a PDF to get JSON (Derulo) parts:</p>
<form action = "/api/upload" method = "post" enctype="multipart/form-data">   
    <input type="file" name="file" /><br/>
    <label for="api_key">API KEY:</label><br>
    <input type="text" id="api_key" name="api_key" value=""><br>
    <input type = "submit" value="Upload">   
</form>
'''

@app.route("/upload", methods=["POST"])
def upload():
    api_key = request.form.get('api_key')
    if not is_api_ok(api_key):
        return "Invalid API key", 401
    file = request.files['file']
    elements_array = run_unstructured(file=file)
    num_elements = str(len(arr))
    return '''
    <h1>PDF-Upload</h1>
    <a href="/">Back</a>
    <p>Number of text parts: ''' + num_elements + '''</p>
    <p>''' + str(elements_array) + '''</p>
    '''

@app.route("/byurl", methods=["POST"])
def byurl():
    api_key = request.form.get('api_key')
    if not is_api_ok(api_key):
        return "Invalid API key", 401
    url = request.form.get('url')
    response = requests.get(url)
    file_like_object = io.BytesIO(response.content)
    elements_array = run_unstructured(file=file_like_object)
    num_elements = str(len(elements_array))
    return '''
    <h1>PDF-Upload</h1>
    <a href="/">Back</a>
    <p>Number of text parts: ''' + num_elements + '''</p>
    <p>''' + str(elements_array) + '''</p>
    '''

@app.route("/api/upload", methods=["POST"])
def api_upload():
    api_key = request.form.get('api_key')
    if not is_api_ok(api_key):
        return "Invalid API key", 401
    file = request.files['file']
    elements_array = run_unstructured(file=file)
    return jsonify(elements_array)

@app.route("/api/byurl", methods=["POST"])
def api_byurl():
    api_key = request.form.get('api_key')
    if not is_api_ok(api_key):
        return "Invalid API key", 401
    url = request.form.get('url')
    response = requests.get(url)
    file_like_object = io.BytesIO(response.content)
    elements_array = run_unstructured(file=file_like_object)
    return jsonify(elements_array)

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    serve(app, host="0.0.0.0", port=5000)