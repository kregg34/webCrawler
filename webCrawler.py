import requests
from bs4 import BeautifulSoup


def job_spider(num_days_ago_posted):
    url = 'https://ca.indeed.com/jobs?q=software%20developer&l=Moncton,%20NB&fromage=' + str(num_days_ago_posted)
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


job_spider(21)
