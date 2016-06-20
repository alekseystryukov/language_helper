from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.network.urlrequest import UrlRequest
from urllib.parse import urlencode
from settings import *


class MainWindow(BoxLayout):

    def __init__(self, **kwargs):
        kwargs['orientation'] = 'vertical'
        super(MainWindow, self).__init__(**kwargs)

        spinner = Spinner(
            # default value shown
            text='Home',
            # available values
            values=('Home', 'Test', 'AddWord'),
            # just for positioning in our example
            size_hint=(1, None),
            size=(100, 44),
            pos_hint={'center_x': .5, 'center_y': .5})

        spinner.bind(text=self.set_page_vidget)

        self.add_widget(spinner)

        self.work_area = BoxLayout()
        self.work_area.add_widget(Home())
        self.add_widget(self.work_area)

    def set_page_vidget(self, _, name):
        self.work_area.clear_widgets()
        vidget = globals()[name]
        self.work_area.add_widget(vidget())


class Home(Label):
    def __init__(self, **kwargs):
        kwargs['text'] = 'Use Menu'
        super(Home, self).__init__(**kwargs)


class AddWord(ScreenManager):

    def __init__(self, **kwargs):
        super(AddWord, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        self.word_input = TextInput(multiline=False, size_hint=(1, .5))
        layout.add_widget(self.word_input)

        self.button = Button(
            on_press=self.send_word,
            on_error=self.on_error,
            text="Send", size_hint=(1, .5),
            pos_hint={'center_x': .5, 'center_y': .5})
        layout.add_widget(self.button)

        add = Screen(name='Add')
        add.add_widget(layout)
        self.add_widget(add)

        # --
        self.status_layout = BoxLayout(orientation='vertical')
        status = Screen(name='Status')
        status.add_widget(self.status_layout)
        self.add_widget(status)

    def send_word(self, *args):
        self.status_layout.clear_widgets()
        self.status_layout.add_widget(Label(text='Loading..'))
        self.current = 'Status'
        word = self.word_input.text
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}

        UrlRequest(POST_WORD_URL, method="POST",
                   req_headers=headers,
                   req_body=urlencode({'word': word}),
                   on_success=self.show_response,
                   on_error=self.on_error,
                   on_failure=self.on_error)

    def show_response(self, _, data):
        if data['name']:
            text = "%s \n\n%s" % (data['name'], "\n".join(["-(%s) %s" % tuple(i) for i in data['meanings_list']]))
        else:
            text = "The word wasn't found"

        self.status_layout.clear_widgets()
        self.status_layout.add_widget(Label(text=text, text_size=(self.width, None), padding_x=10))
        self.status_layout.add_widget(Button(text='OK', on_press=self.reset))

    def on_error(self, *args):
        print('on_error', args)

    def reset(self, *args):
        self.word_input.text = ""
        self.current = 'Add'
        self.status_layout.clear_widgets()


class Test(ScreenManager):

    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)

        screen = Screen(name='Home')
        self.home_page = HomePage()
        screen.add_widget(self.home_page)
        self.add_widget(screen)

        screen = Screen(name='Question')
        self.question_page = QuestionPage()
        screen.add_widget(self.question_page)
        self.add_widget(screen)

        self.question = None
        self.answered = None
        self.new_question()

    def show_question(self, resp, data):
        self.answered = False
        self.question = data
        self.question_page.question.text = data['name']
        self.question_page.answers.clear_widgets()
        for meaning in data['meanings']:
            button = Button(
                on_press=self.send_answer,
                text=meaning['text'],
                size_hint=(1, .2),
                halign='center',
                text_size=(self.width, None)
            )
            button.is_right_meaning = meaning['right']
            self.question_page.answers.add_widget(button)

        self.current = 'Question'

    def send_answer(self, *args):
        if not self.answered:
            self.answered = True
            for button in  self.question_page.answers.children:
                button.background_color = [0, 1, 0, 1] if button.is_right_meaning else [1, 0, 0, 1]
        else:
            self.new_question()

    def new_question(self):
        self.current = 'Home'
        UrlRequest(GET_QUESTION_URL, on_success=self.show_question)


class BasePage(BoxLayout):

    def __init__(self, **kwargs):
        kwargs['orientation'] = 'vertical'
        super(BasePage, self).__init__(**kwargs)

    @property
    def manager(self):
        return self.parent.parent


class HomePage(BasePage):

    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.question = Label(text='Welcome! \n '
                                   'We are loading next question')
        self.add_widget(self.question)


class QuestionPage(BasePage):

    def __init__(self, **kwargs):
        super(QuestionPage, self).__init__(**kwargs)

        self.question = Label()
        self.add_widget(self.question)
        self.answers = BoxLayout(orientation='vertical')
        self.add_widget(self.answers)
