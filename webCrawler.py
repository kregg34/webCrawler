import requests
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

job_search_terms = ["Software developer", "software engineer", "programmer", "Java", "Python", "software internship",
                    "software junior", "software entry level"]
job_cities = ["Moncton", "Saint John", "Shediac", "Fredericton", "Sussex"]
job_province = "NB"
num_days_posted = 7

FILE_NAME = 'Job Ad Info.json'


def job_spider_indeed(search_term, province, city, num_days_ago_posted):
    url = 'https://ca.indeed.com/jobs?q=' + search_term.replace(' ', '%20') + '&l=' + \
            city.replace(' ', '%20') + ',%20' + province + '&fromage=' + str(num_days_ago_posted) + \
            '&radius=0'
    src_code = requests.get(url)
    plain_text = src_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    for jobAd in soup.findAll('div', {'class': 'jobsearch-SerpJobCard'}):
        # removes new jobs from showing "new" in the job title
        for span in jobAd.findAll('span', {'class': 'new'}):
            span.decompose()

        job_title_tag = jobAd.find('h2', {'class': 'title'})
        job_company_tag = jobAd.find('span', {'class': 'company'})
        days_ago_posted_tag = jobAd.find('span', {'class': 'date'})

        job_title = job_title_tag.text.replace("\n", "")
        job_company = job_company_tag.text.replace("\n", "")
        days_ago_posted = days_ago_posted_tag.text.replace("\n", "")
        date_posted = convert_to_date(days_ago_posted)

        add_to_json(job_title, job_company, days_ago_posted, date_posted, city)


def add_to_json(job_title, job_company, days_ago_posted, date_posted, city):
    new_ad = {"Job title": job_title,
              "Company": job_company,
              "Date posted": date_posted,
              "City": city}

    if job_already_exists(new_ad):
        None
    else:
        with open(FILE_NAME) as f:
            data = json.load(f)
            f.close()

        with open(FILE_NAME, 'w') as f:
            data.append(new_ad)
            json.dump(data, f)
            f.close()

        print('Job title: ' + job_title + '\nCompany: ' + job_company + '\nDate posted: ' +
              date_posted + '\nCity: ' + city + '\nPosted: ' + days_ago_posted + '\n')


def job_already_exists(ad):
    with open(FILE_NAME) as f:
        data = json.load(f)
        f.close()

    for existing_ad in data:
        if existing_ad["Job title"] == ad["Job title"]:
            if existing_ad["Company"] == ad["Company"]:
                if existing_ad["Date posted"] == ad["Date posted"]:
                    if existing_ad["City"] == ad["City"]:
                        return True
    return False


def convert_to_date(days_ago_str):
    if days_ago_str == '30+ days ago':
        return "Exact date unknown. Job posted 30+ days ago..."

    if days_ago_str == 'Today' or days_ago_str == 'Just posted':
        days_ago = 0
    else:
        try:
            days_ago = [int(word) for word in days_ago_str.split() if word.isdigit()][0]
        except IndexError:
            return "Error"

    old_date = datetime.now() - timedelta(days=days_ago)
    date_posted = old_date.strftime('%Y-%m-%d')
    return date_posted


def file_setup():
    with open(FILE_NAME, 'a+') as json_file:
        if os.stat(FILE_NAME).st_size == 0:
            blank_data = []
            json.dump(blank_data, json_file)
    json_file.close()


file_setup()

for job_city in job_cities:
    for term in job_search_terms:
        job_spider_indeed(term, job_province, job_city, num_days_posted)
