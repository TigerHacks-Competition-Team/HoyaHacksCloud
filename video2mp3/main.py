import functions_framework
import ffmpeg
import urllib.request

class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

@functions_framework.http
def video2mp3(request):
    url = request.json["video"]
    print(url.split("/")[9])

    filename= url.split("/")[-1]
    opener = AppURLOpener()
    response = opener.open(url)
    outfile = open(f"/tmp/${filename}", "wb")
    outfile.write(response.read())
    print(outfile)
    outfile.close()

    return 'OK'

