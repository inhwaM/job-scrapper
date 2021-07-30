import requests
from bs4 import BeautifulSoup

def extract_job(html):  
  a_link = html.find("a",{"itemprop":"url"})['href']
  link = f"https://remoteok.io/{a_link}"
  title = html.find("h2").string
  company = html.find("h3").string
  location = html.find("div", {"class":"location"})
  if location is None:
    location = "no office location"  
  else:
    if "$" in location.string:
      location = "no office location"
    else:   
      location = location.string
      
  return {
     'title': title, 
     'company': company, 
     'location': location,
     'link': link
  }         
        
def extract_jobs(url): 
  hdr = {'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\Safari/537.36'),} 
  jobs = []

  result = requests.get(url,headers=hdr)
  soup = BeautifulSoup(result.text, 'html.parser')
  trs = soup.find("table").find_all("tr",{"class": "job"})

  for tr in trs:
    tds = tr.find_all("td", {"class":"company"})
    for td in tds:
      print(f"Scrapping RO:")
      job = extract_job(td)
      jobs.append(job)
  return jobs 

def get_jobs(word):
  url = f"https://remoteok.io/remote-{word}-jobs"
  jobs = extract_jobs(url)
  return jobs           