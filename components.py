from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
import threading
import time

from api import get_audio_urls, get_chapters_list_async 
from devices import device_manager


class ChaptersComponents(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        # formatting properties
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 12

        # child widgets
        # chapters list, values will be given once chapters list are retrieved
        self.chapters_list = Spinner(
                size_hint = (0.9, None),
                size = (300, 64),
                pos_hint = {'center_x': .5},
        )
        self.chapters_list.bind(text=self.on_chapter_select)
        self.chapters_list.disabled = True

        self.verse_start = Spinner(
            size_hint = (0.3, None),
            size = (150, 64),
            pos_hint = {'center_y': .5},
        )
        self.verse_start.bind(text=self.on_verse_start_select)
        self.verse_end = Spinner(
            size_hint = (0.3, None),
            size = (150, 64),
            pos_hint = {'center_y': .5},
        )
        self.verse_end.bind(text=self.on_verse_end_select)
        self.verse_start.disabled = self.verse_end.disabled = True

        box1 = BoxLayout(size_hint = (1, None))
        box1.add_widget(Label(text = "From: ", size_hint = (None, None),
                             pos_hint = {'center_y': .5}))
        box1.add_widget(self.verse_start)
        box1.add_widget(Label(text = "To: ", size_hint = (None, None),
                            pos_hint = {'center_y': .5}))
        box1.add_widget(self.verse_end)

        box_play = BoxLayout(spacing=6, size_hint=(1,None))
        box_play.add_widget(Label(text="Repeat count", size_hint=(0.4, None)))
        self.selector_repeat = Spinner(
                values=[str(i) for i in range(1,11)],
                size_hint = (0.2, None),
                size = (100, 64)
        )
        self.button_play = Button(
            text = "Play",
            size_hint = (0.3, None),
            size = (150, 64)
        )
        self.button_play.bind(on_release=self.on_button_play_release)
        box_play.add_widget(self.selector_repeat)
        box_play.add_widget(self.button_play)
        box_play.disabled = True
        self.box_play = box_play

        self.add_widget(self.chapters_list)
        self.add_widget(box1)
        self.add_widget(box_play)

    def set_chapters(self, chapters):
        if not chapters:
            # error on chapter list retrieval
            return
        self.chapters = chapters
        self.selected_chapter = None
        names = [ "{}. {}".format(c['id'], c['name_simple']) for c in self.chapters ]
        self.chapters_list.values = names 
        self.chapters_list.disabled = False

    def on_chapter_select(self, instance, value):
        i = instance.values.index(value)
        self.selected_chapter = i+1
        self.verse_start.values = [str(x) for x in range(1,int(self.chapters[i]['verses_count'])+1)]
        self.verse_start.disabled = False
        self.verse_end.disabled = True
        self.box_play.disabled = True

    def on_verse_start_select(self, instance, value):
        self.verse_end.values = instance.values[int(value)-1:]
        self.verse_end.text = instance.text
        self.verse_end.disabled = False

    def on_verse_end_select(self, *args):
        if(device_manager.device):
            self.box_play.disabled = False

    def on_button_play_release(self, *args):
        try:
            rep = int(self.selector_repeat.text)
        except ValueError:
            # repeat is not selected
            self.selector_repeat.text = str(1)
            rep = 1

        device_manager.play_and_queue_audio(
            get_audio_urls(
              self.selected_chapter,
              int(self.verse_start.text),
              int(self.verse_end.text)
            ),
            repeat = rep)


""" A helper class for having buttons that sizes according to its text """
class ButtonWrap(Button):
    
    def __init__(self, **kwargs):
        if ('padding' not in kwargs.keys()):
            kwargs['padding'] = (15,10)
        if('size_hint' not in kwargs.keys()):
            kwargs['size_hint'] = (None, None)
        super().__init__(**kwargs)
        self.bind(texture_size = self._wrap_text)

    def _wrap_text(self, s, sz):
        s.size = s.texture_size

class DeviceComponents(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        # formatting properties
        self.padding = 6
        self.spacing = 6
        self.orientation = 'vertical'

        # first part: device discovery and connection
        self.button_discover = ButtonWrap(
                text = 'Discover',
        )

        self.label_discovery_status = Label(
                size = (0,0), size_hint = (None, None) )
        self.button_discover.bind(on_release=self.discover)

        self.selector_devices = Spinner(
                values = (),
                size_hint = (0.5, None),
                size = (300, 64)
        )
        self.selector_devices.bind(text=self.on_devices_select)

        self.button_connect = ButtonWrap(
                text = 'Connect',
                disabled = True
        )
        self.button_connect.disabled = True
        self.button_connect.bind(on_release=self.on_button_connect_release)

        # second part: media player status and volume control
        self.media_player_status = BoxLayout(
                size_hint = (1, 0.6)
        )
        self.button_play = Button(
                padding = [20, 20],
                size_hint = (0.2, 1),
                text = 'Play'
        )
        self.button_play.bind(on_release=self.on_button_play_release)

        self.box2 = BoxLayout(size_hint = (0.8, 1), orientation='vertical',
                      spacing=12, padding=10)
        box3 = BoxLayout()
        self.label_player_status = Label()
        self.volume_status = Label()
        box3.add_widget(self.label_player_status)
        box3.add_widget(self.volume_status)
        
        self.slider_volume = Slider(min=0, max=10, step=1, padding=10)
        self.slider_volume.bind(value=self.on_volume_change)
        self.box2.add_widget(box3)
        self.box2.add_widget(self.slider_volume)

        self.media_player_status.add_widget(self.button_play)
        self.media_player_status.add_widget(self.box2)
        self.media_player_status.disabled = True

        # add all the parts
        self.add_widget(self.button_discover)
        self.add_widget(self.label_discovery_status)
        self.add_widget(self.selector_devices)
        self.add_widget(self.button_connect)
        self.add_widget(self.media_player_status)

    def discover(self, instance):
        def discover_async(start_time):
            discovered = device_manager.discover()
            self.label_discovery_status.size = (130, 64)
            self.label_discovery_status.size_hint_x = 0.3
            # device discovery won't always succeed on the first try
            # attempt to retry discovery for one minute
            if(not discovered and ((start_time + 60.0) > time.time())):
                self.label_discovery_status.text = f"No devices found (retrying)."
                return discover_async(start_time)
            self.label_discovery_status.text = f"{len(discovered)} device(s) found."
            if discovered:
                self.selector_devices.values = [f"{d.friendly_name} ({d.host})" for d in discovered]
            self.button_discover.text = "Discover"
            self.button_discover.disabled = False

        self.button_discover.text = "Discovering..."
        self.button_discover.disabled = True
        threading.Thread(target=discover_async, args=[time.time()]).start()

    def on_devices_select(self, *args, **kwargs):
        print(args)
        self.button_connect.disabled = False

    def on_volume_change(self, instance, *args):
        if(device_manager.device):
            device_manager.device.set_volume(instance.value_normalized)

    def on_button_connect_release(self, instance):
        i = self.selector_devices.values.index(self.selector_devices.text)
        def connect_to_device_async(start_time):
            instance.text = "Connecting..."
            instance.disabled = True
            connected = device_manager.connect_to_discovered_device(i)
            print(connected)
            if(not connected and ((start_time + 60.0) > time.time())):
                return connect_to_device_async(start_time)
            instance.text = "Connect"
            instance.disabled = False
            if(connected):
                self.media_player_status.disabled = False
                self.app.register_status_listeners()

        threading.Thread(target=connect_to_device_async, args=[time.time()]).start()

    def on_button_play_release(self, instance):
        try:
            if(instance.text == "Play"):
                    device_manager.device.media_controller.play()
            elif(instance.text == "Pause"):
                    device_manager.device.media_controller.pause()
        except:
            pass

    def new_cast_status(self, status):
        if(not status):
            self.media_player_status.disabled = True
            return
        self.slider_volume.value = round(10.0 * status.volume_level)
        self.volume_status.text = "Volume: " + f"{(100.0*status.volume_level):.0f}%"

    def new_media_status(self, status):
        if(status):
            self.label_player_status.text = "Status: " + status.player_state
            self.button_play.text = "Pause" if(status.player_state == "PLAYING") else "Play"
        else:
            self.label_player_status.text = "(make sure device is connected)"
