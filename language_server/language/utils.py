from urllib.parse import quote
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


starts = ('a', 'to')


def clear_word(word):
    word = word.split()
    if len(word):
        if word[0] in starts:
            word = word[1:]
    return " ".join(word)


def get_meanings(word):
    url = "https://www.vocabulary.com/dictionary/%s" % quote(word)

    q = Request(url)
    q.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5')

    resp = urlopen(q).read().decode("utf-8")
    soup = BeautifulSoup(resp, 'html.parser')

    response = []
    for meanings in soup.find_all("div", {'class': "ordinal first"}):
        response.append(tuple(meanings.find("h3", {'class': "definition"}).stripped_strings))

    return response

