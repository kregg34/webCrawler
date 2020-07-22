import requests
from bs4 import BeautifulSoup


def job_spider(search_term, province, city, num_days_ago_posted):
    url = 'https://ca.indeed.com/jobs?q=' + search_term + '&l=' + city + ',%20' + \
          province + '&fromage=' + str(num_days_ago_posted)
    src_code = requests.get(url)
    plain_text = src_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    for jobAd in soup.findAll('div', {'class': 'jobsearch-SerpJobCard'}):
        # removes "new" jobs from showing new in the job title
        for span in jobAd.findAll('span', {'class': 'new'}):
            span.decompose()

        job_title_tag = jobAd.find('h2', {'class': 'title'})
        job_company_tag = jobAd.find('span', {'class': 'company'})
        job_date_posted_tag = jobAd.find('span', {'class': 'date'})

        print(job_title_tag.text.rstrip("\n") + job_company_tag.text.rstrip("\n") +
              '\n' + job_date_posted_tag.text.rstrip("\n"))


job_search_term = 'software developer'.replace(' ', '%20')
job_province = 'NB'
job_city = 'Fredericton'.replace(' ', '%20')
num_days_posted = 3

job_spider(job_search_term, job_province, job_city, num_days_posted)
