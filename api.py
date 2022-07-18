import requests
import threading

API_URL = "https://api.quran.com/api/v4"
AUDIO_URL = "https://download.quranicaudio.com/verses/Alafasy/mp3/"

def get_chapters_list():
    try:
        r = requests.get(API_URL + '/chapters')
    except:
        print("Network request error")
        return None
    if(r.ok):
        return r.json()['chapters']

def get_chapters_list_async(callback):
    def run(cb):
        chapters = get_chapters_list()
        cb(chapters)
    threading.Thread(target=run, args=[callback]).start()

def get_audio_urls(chapter, start, end):
    urls = [AUDIO_URL + f"{chapter:03d}{i:03d}" + ".mp3"
            for i in range(start,end+1)]
    return urls
