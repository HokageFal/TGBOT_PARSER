import requests
from bs4 import BeautifulSoup


url = "https://hh.ru/resume/671941deff0ebbdb430039ed1f78786d5a6576"



response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


print(response.text)