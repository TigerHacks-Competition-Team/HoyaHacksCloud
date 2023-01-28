import functions_framework
import yt_dlp
from google.cloud import storage
import os
from flask import Response

final_filename = None

def yt_dlp_monitor(d):
    global final_filename
    if final_filename is None:
        final_filename = d.get('info_dict').get('_filename')

@functions_framework.http
def yt2mp3(request):
    global final_filename
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        # Extract audio using ffmpeg
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        "outtmpl": "/tmp/%(id)s.%(ext)s",
        "no-part": True,
        "progress_hooks": [yt_dlp_monitor]
    }

    URL = [request.json["url"]]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URL)

        bucket = "hoya-hacks-video-files"

        storage_client = storage.Client()

        bucket = storage_client.get_bucket(bucket, timeout = 0.1)

        id = final_filename.split("/")[2].split(".")[0]

        mp3_path = "/tmp/" + id + ".mp3"

        file = bucket.blob(id + ".mp3")

        file.upload_from_filename(mp3_path)

        #file.make_public()

        os.remove(mp3_path)

        final_filename = None

        return Response(status = 200)

    return request.json["url"]