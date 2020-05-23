from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import os, io
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

connect_str = open('string.txt', 'r').read().rstrip()
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = 'uploads'
blob_container_client = blob_service_client.get_container_client(container_name)

@app.route('/')
def index():
    html = """ Click <a href = "/upload_file"> here </a> to upload a file.
        Click <a href = "/show_all_files" here </a> to show all files.
    """
    return html

@app.route('/upload_file')
def upload_file():
    html = """
    <form action = "/upload_success" method = "post" enctype="multipart/form-data">
        <input type = "file" name = "file_name">
        <input type = "submit" name = "Upload">
    </form>
    
    <a href = 'https://www.somesite.info/'> Visit another site </a>
    """
    return html

@app.route('/upload_success', methods = ['POST'])
def upload_success():
    all_files = [b.name for b in blob_container_client.list_blobs()]
    file = request.files['file_name']
    if file.filename in all_files:
        blob_container_client.delete_blob(file.filename)
    blob_client = blob_container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file)
    return file.filename + ' uploaded succesfully. Show all <a href = "/show_all_files"> files </a>'


@app.route('/show_all_files')
def show_all_files():
    all_files = [b.name for b in blob_container_client.list_blobs()]
    html = ""
    for filename in all_files:
        html = html + "<a href = '/download_file/" + filename + "'> " + filename + " </a>" + "<br/>"
    return html

@app.route('/download_file/<filename>')
def download_file(filename):
    all_files = [b.name for b in blob_container_client.list_blobs()]
    if filename not in all_files:
        return filename + " does not exist. Go to <a href = '/'> home page </a>"
    return send_file(io.BytesIO(blob_container_client.get_blob_client(filename).download_blob().readall()), 
                     as_attachment = True, 
                     attachment_filename = filename)

if __name__ == '__main__':
    app.run()
