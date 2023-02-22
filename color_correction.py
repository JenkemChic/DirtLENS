# Import necessary modules
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty

# Import helper module for GPS coordinates
import GPS_Helper

# Import color values from colors.py file
from colors import COLORS

# Define main layout using KivyMD
Builder.load_string('''
<MyLayout>:
    orientation: 'vertical'
    MDLabel:
        id: rgb_label
        text: root.rgb_text
        halign: 'center'
        valign: 'middle'
    MDLabel:
        id: gps_label
        text: root.gps_text
        halign: 'center'
        valign: 'middle'
    MDFloatLayout:
        id: image_layout
        MDRaisedButton:
            id: capture_button
            text: 'Capture'
            pos_hint: {'center_x': 0.5, 'y': 0.1}
            size_hint: 0.3, 0.1
            on_press: root.capture_image()
''')

# Define main layout class
class MyLayout(BoxLayout):
    # Define StringProperties for labels
    rgb_text = StringProperty('')
    gps_text = StringProperty('')

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

        # Set up camera
        self.camera = Image(source=0, allow_stretch=True)
        self.ids.image_layout.add_widget(self.camera)

    def capture_image(self):
        # Get RGB values from captured image
        rgb = self.camera.texture.pixels
        r, g, b = rgb[0], rgb[1], rgb[2]

        # Find closest color match from COLORS list
        color_name = min(COLORS, key=lambda x: abs(COLORS[x][0]-r)+abs(COLORS[x][1]-g)+abs(COLORS[x][2]-b))

        # Update RGB label
        self.rgb_text = f'RGB: {r}, {g}, {b}\nColor: {color_name}'

        # Get GPS coordinates
        lat, lon = GPS_Helper.get_coordinates()

        # Find cardinal direction based on GPS coordinates
        direction = GPS_Helper.get_cardinal_direction(lat, lon)

        # Update GPS label
        self.gps_text = f'GPS: {lat}, {lon}\nDirection: {direction}'

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()

