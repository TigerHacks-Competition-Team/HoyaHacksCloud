import functions_framework
import ffmpeg
import urllib.request
from google.cloud import storage
import os

class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

@functions_framework.http
def video2mp3(request):
    extension = 'wav'
    url = request.json["video"]
    print(url.split("/")[9])

    filename= url.split("/")[-1]
    opener = AppURLOpener()
    response = opener.open(url)
    outfile = open(f"/tmp/{filename}", "wb")
    outfile.write(response.read())
    
    videoPath = f"/tmp/{filename}"
    audioPath = f"/tmp/{filename}.{extension}"
    cmd = f"ffmpeg -i {videoPath} -vn {audioPath}"
    os.system(cmd)

    bucket = "hoya-hacks-video-files"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket, timeout = 60)

    file = bucket.blob(f"{filename}.{extension}")
    file.upload_from_filename(audioPath)

    outfile.close()

    if request.method == 'POST':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }

            return("gs://hoya-hacks-video-files/" + f"{filename}.{extension}", 200, headers)

    headers = {
        'Content-Type':'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    return ('', 200, headers)

