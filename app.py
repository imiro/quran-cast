# https://kivy.org/doc/stable/guide/basic.html#quickstart

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from api import get_chapters_list_async
from devices import device_manager
from components import ChaptersComponents, DeviceComponents

class QCastApp(App):

    def __init__(self):
        super().__init__()
        self.device_components = DeviceComponents(self)
        self.chapters_components = ChaptersComponents(self)

        self.screen = BoxLayout(
                orientation = 'vertical',
                spacing = 10
        )
        self.screen.add_widget(self.device_components)
        self.screen.add_widget(self.chapters_components)

        get_chapters_list_async(self.chapters_components.set_chapters)

    def build(self):
        return self.screen
    
    def register_status_listeners(self):
        try:
            device_manager.device.register_status_listener(self)
            device_manager.device.media_controller.register_status_listener(self)
            self.new_cast_status(device_manager.device.status)
            self.new_media_status(device_manager.device.media_controller.status)
        except:
            pass

    def new_cast_status(self, status):
        # propagate
        self.device_components.new_cast_status(status)

    def new_media_status(self, status):
        self.device_components.new_media_status(status)

if __name__ == '__main__':
    QCastApp().run()
