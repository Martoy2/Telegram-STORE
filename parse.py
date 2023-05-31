import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data():
    URL_TEMPLATE = "https://docs.google.com/document/d/1lsajdW3-UyZFmoZY6lmZPft4VsK_79VXoFYlFCt9GJ8/edit"
    r = requests.get(URL_TEMPLATE)
    bs = BeautifulSoup(r.text,"lxml")

    temp = bs.find('meta', property='og:description')
    temp=str(temp)

    login=str(temp.split('login:')[1])
    login=str(login.split('pass:')[0])
    password=str(temp.split('pass: ')[1])
    password=str(password.split(' ')[0])

    return(login.replace(" ", ''), password.replace(" ", ''))
