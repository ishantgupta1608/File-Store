from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)



@app.route('/')
def index():
    print('cadf')
    connect_str = open('string.txt', 'r').read().rstrip()
    
    #container_client = blob_service_client.create_container('secondcontainer')
    
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    blob_client = blob_service_client.get_blob_client(container='secondcontainer', 
                                                      blob='posture image.jpg')
    #blob_client.upload_blob(open('image.jfif', 'rb'))
    blob_client.download_blob().readinto(open('myimg.jpg', 'wb'))
    
    return send_file(filename_or_fp = 'myimg.jpg', 
                     attachment_filename = 'downdown.jpg', 
                     as_attachment = True)
    #return 'Hii'
    #return render_template('index.html')


if __name__ == '__main__':
    app.run()