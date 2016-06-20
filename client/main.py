import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from vidgets import MainWindow


class MyApp(App):

    def build(self):
        return MainWindow()


if __name__ == '__main__':
    MyApp().run()