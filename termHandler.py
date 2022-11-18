import re
import json
import requests
from bs4 import BeautifulSoup


class Term:
    def __init__(self, text):
        self.cleaned = ''
        self.url = ''
        self.definition = ''
        self.text = text

    def clean_url(self):
        text = self.text.replace("@definancebot ", '')
        self.cleaned = re.sub(r'[^a-zA-Z0-9-]', '', text)

    def get_url(self):
        #self.url = f'https://coinmarketcap.com/alexandria/glossary/{self.cleaned}'
        self.url = f'https://www.investopedia.com/terms/{self.cleaned[0]}/{self.cleaned}.asp'

    def get_definition(self):
        data = requests.get(self.url)
        if data.status_code == 200:
            soup = BeautifulSoup(data.text, 'html.parser')
            definition = soup.find_all('p')[1].get_text()
            if definition.startswith('Investopedia'):
                self.definition='Here you go! ' + self.url
            else:
                self.definition = soup.find_all('p')[1].get_text() + ' Source: ' + self.url
        else:
            print("Definition not found :(")
    
    def format_term(self):
        self.clean_url()
        self.get_url()
        self.get_definition()
        return self.definition

