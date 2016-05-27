import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from urllib.parse import urlencode


HOST = 'http://localhost:8888/'
API_URL = HOST + 'api/v1/'
GET_QUESTION_URL = API_URL + 'get_random_word/'


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

        screen = Screen(name='Answer')
        self.answer_page = AnswerPage()
        screen.add_widget(self.answer_page)
        self.add_widget(screen)

        self.question = None
        self.new_question()

    def show_answer(self, text):
        self.answer_page.answer.text = text
        self.current = 'Answer'

    def show_question(self, resp, data):
        self.question = data
        self.question_page.question.text = data['name']
        self.answer_page.question.text = data['name']
        self.current = 'Question'

    def new_question(self):
        self.current = 'Home'
        UrlRequest(GET_QUESTION_URL, on_success=self.show_question)

    def send_answer(self):
        def bug_posted(req, result):
            print('Our bug is posted !')
            print(result)

        params = urlencode({'@number': 12524, '@type': 'issue',
                            '@action': 'show'})
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}
        req = UrlRequest('bugs.python.org',
                         on_success=bug_posted,
                         req_body=params,
                req_headers=headers)


class BasePage(GridLayout):

    def __init__(self, **kwargs):
        super(BasePage, self).__init__(**kwargs)
        self.cols = 1

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

        self.answer = TextInput(multiline=True)
        self.add_widget(self.answer)

        self.reply_button = Button(
            on_press=self.send_answer,
            text="Reply", size_hint=(.5, .5),
            pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(self.reply_button)

    def send_answer(self, *args):
        text = self.answer.text
        self.answer.text = ""
        self.manager.show_answer(text)


class AnswerPage(BasePage):

    def __init__(self, **kwargs):
        super(AnswerPage, self).__init__(**kwargs)

        self.question = Label()
        self.add_widget(self.question)

        self.answer = Label()
        self.add_widget(self.answer)

        self.reply_button = Button(
            on_press=self.next_question,
            text="Next", size_hint=(.5, .5),
            pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(self.reply_button)

    def next_question(self, *args):
        self.manager.new_question()


class MyApp(App):

    def build(self):
        return Test()


if __name__ == '__main__':
    MyApp().run()