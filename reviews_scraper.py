import requests
from bs4 import BeautifulSoup
import pandas as pd

#url = "https://www.amazon.com/Covergirl-Clean-Fresh-Skin-Light/product-reviews/B07YX84L8J/ref=cm_cr_getr_d_paging_btm_next_103?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

#while ('li', {'class': 'a-disabled a-last'})
#a-last means keep going

x = 98 #number of pages

rList = []

from requests import get

def findSoup(url):
  r = requests.get('http://localhost:8050/render.html', params= {'url': url, 'wait': 2})
  #print(r.status_code) #200 means webpage successfully downloaded
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup

#strip() to remove whitespaces
def getReviews(soup):
  reviews = soup.find_all('div', {'data-hook': 'review'})
  try:
    for rev in reviews:
      rDict = {
      "name" : "Covergirl: Clean Fresh Skin Milk Foundation",
      "title" : rev.find('a', {'data-hook': 'review-title'}).text.strip(),
      "date" : rev.find('span', {'data-hook': 'review-date'}).text.partition("on")[2].strip(),
      "shade" : rev.find('a', {'data-hook': 'format-strip'}).text.partition("FoundationColor: ")[2].strip(),
      #badge = rev.find('span', {'data-hook': 'avp-badge'}).text
      "rating" : float(rev.find('i', {'data-hook': 'review-star-rating'}).text.replace("out of 5 stars", "").strip()),
      "body" : rev.find('span', {'data-hook': 'review-body'}).text.strip()
      }
      rList.append(rDict)
  except:
    pass
  return rList
  
for i in range(1,x+1):
  currUrl = f'https://www.amazon.com/Covergirl-Clean-Fresh-Skin-Light/product-reviews/B07YX84L8J/ref=cm_cr_getr_d_paging_btm_next_103?ie=UTF8&reviewerType=all_reviews&pageNumber={i}'
  #curr_url = url.replace(url[-1], str(i))
  currSoup = findSoup(currUrl)
  print(f'Scraping page: {i}')
  currReviews = getReviews(currSoup)
  if not currSoup.find('li', {'class': 'a-disabled a-last'}):
    pass
  else:
    break

df = pd.DataFrame(currReviews)
df.to_excel('covergirl-sentiment.xlsx', index = False)
#why didn't df.to_csv work

print(currReviews)
print("Done")


