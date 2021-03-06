from bs4 import BeautifulSoup
import requests
import pandas as pd

source = requests.get('https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/').text
soup = BeautifulSoup(source, 'lxml')

moive_reviews = {'ratings': [], 'critics': []}

for m in soup.find_all('table', class_='table')[0].find_all('a', href=True):
    url = 'https://www.rottentomatoes.com/' + m['href']
    sub_source = requests.get(url).text
    sub_soup = BeautifulSoup(sub_source, 'lxml')
    try:
        critic = sub_soup.find('div', class_='col-sm-12 tomato-info hidden-xs')
        c = critic.text.split('Critics Consensus:')[1]
    except Exception as e:
        c = None

    try:
        rating = sub_soup.find('div', class_='superPageFontColor')
        r = rating.text.split('Average Rating:')[1].split('/')[0]
    except Exception as e:
        r = None

    moive_reviews['ratings'].append(r)
    moive_reviews['critics'].append(c)

moive_reviews_df = pd.DataFrame(moive_reviews) # moive_reviews_df is now a dataframe and ready to be outputed as a csv file

