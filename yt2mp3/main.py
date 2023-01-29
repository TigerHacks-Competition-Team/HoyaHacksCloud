import functions_framework
import yt_dlp
from google.cloud import storage
import os
from flask import Response
import json

final_filename = None

def yt_dlp_monitor(d):
    global final_filename
    if final_filename is None:
        final_filename = d.get('info_dict').get('_filename')

@functions_framework.http
def yt2mp3(request):
    global final_filename
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # Extract audio using ffmpeg
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        "outtmpl": "/tmp/%(id)s.%(ext)s",
        "no-part": True,
        "progress_hooks": [yt_dlp_monitor]
    }

    URL = [request.json["url"]]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            error_code = ydl.download(URL)
        except:
            return('', 500)

        bucket = "hoya-hacks-video-files"

        storage_client = storage.Client()

        bucket = storage_client.get_bucket(bucket, timeout = 60)

        id = final_filename.split("/")[2].split(".")[0]

        mp3_path = "/tmp/" + id + ".m4a"

        file = bucket.blob(id + ".m4a")

        print("Uploading Audio to Bucket")
        file.upload_from_filename(mp3_path)

        #file.make_public()

        #os.remove(mp3_path)

        final_filename = None

        if request.method == 'POST':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }

            return("https://storage.cloud.google.com/hoya-hacks-video-files/" + id + ".m4a", 200, headers)

    headers = {
        'Content-Type':'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    return ('', 200, headers)