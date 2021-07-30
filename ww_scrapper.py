import requests
from bs4 import BeautifulSoup

def extract_job(html):   
  company = html.find("span", {"class":"company"}).text
  title = html.find("span", {"class":"title"}).string
  location = html.find("span", {"class":"region"})
  if location is None:
    location = "no office location"
  else:
    location = location.string  
  a_link = html.find_all("a")[1]['href']
  link = f"https://weworkremotely.com{a_link}"

  return {
     'title': title, 
     'company': company, 
     'location': location,
     'link': link
  }     

def extract_jobs(url):      
  jobs = []

  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  sections = soup.find_all("section", {"class":"jobs"})

  for section in sections:  
      lists = section.find_all("li")[:-1]
      for li in lists:
        print(f"Scrapping WW:")
        job = extract_job(li)
        jobs.append(job)
  return jobs  

def get_jobs(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  jobs = extract_jobs(url)
  return jobs               


    