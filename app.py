from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)



@app.route('/')
def index():
    connect_str = 'DefaultEndpointsProtocol=https;AccountName=allmyfiles;AccountKey=6kHeRxzeEIwkywZ5gv4dKC9/aLdiQjZqfS+VbBukijNTZin7kLDjfrbNDd4Y8J05s6rXJ/TiQYvop0J5DzJCpg==;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    #container_client = blob_service_client.create_container('secondcontainer')

    blob_client = blob_service_client.get_blob_client(container='secondcontainer', 
                                                      blob='image.jfif')
    #blob_client.upload_blob(open('image.jfif', 'rb'))
    blob_client.download_blob().readinto(open('image.jfif', 'wb'))
    
    return send_file('image.jfif')
    #return render_template('index.html')


if __name__ == '__main__':
    app.run()