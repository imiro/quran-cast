import pychromecast
import time
# https://github.com/home-assistant-libs/pychromecast
# https://developers.google.com/cast/docs/developers

class DeviceManager:
    
    def __init__(self):
        self.cast_infos = []
        self.cast = None
        self.device = None

    def discover(self):
        self.cast_infos, self.browser = pychromecast.discovery.discover_chromecasts()
        print(f"{len(self.cast_infos)} devices discovered") 
        # print(self.cast_infos)
        pychromecast.discovery.stop_discovery(self.browser)
        return self.cast_infos

    def connect_to_discovered_device(self, i):
        if i >= len(self.cast_infos):
            print("index out of range")
            return False
        self.casts, self.browser = pychromecast.get_listed_chromecasts(
                uuids=[self.cast_infos[i].uuid])
        if not self.casts:
            return False
        # initiate waiting thread
        self.device = self.casts[0]
        self.device.wait()
        self.device.register_status_listener(self)
        return True
    
    def get_device_status(self):
        if not self.device:
            return
        # volume status, stand by, active input, etc
        return self.device.status

    def set_device_volume(self,v):
        if not self.device:
            return
        self.device.set_volume(v)

    def play_and_queue_audio(self, urls, repeat = 1):
        if not self.device:
            return
        # https://github.com/home-assistant-libs/pychromecast/blob/master/examples/media_enqueue.py
        self.device.media_controller.play_media(urls[0], "audio/mp3")
        while self.device.media_controller.status.player_state != "PLAYING":
            time.sleep(0.1)
        for url in urls[1:]:
            self.device.media_controller.play_media(url, "audio/mp3", enqueue=True)
        for x in range(repeat-1):
            for url in urls:
                self.device.media_controller.play_media(url, "audio/mp3", enqueue=True)

    def new_cast_status(self, status):
        print(status)

device_manager = DeviceManager()
# ask user to determine which cast to connect

