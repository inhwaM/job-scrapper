import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  pages = soup.find("div", {"class": "s-pagination"}).find_all('a')
  last_page = pages[-2].get_text(strip=True)
  last_page = int(last_page)
  return last_page
  

def extract_job(html):
  job = {}
  title = html.find("h2").find("a")["title"]
  com_loc = html.find("h3").find_all("span", resursive=False)
  company = com_loc[0].get_text(strip=True)
  location = com_loc[1].get_text(strip=True)
  job_id = html['data-jobid']

  job['title'] = title
  job['company'] = company
  job['location'] = location
  job['link'] = f"https://stackoverflow.com/jobs/{job_id}"
  
  return job 


def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO: Page: {page}")
    result = requests.get(f"{url}&pg={page + 1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs  


def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs