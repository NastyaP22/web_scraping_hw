import requests
import fake_headers
import unicodedata
import json
from bs4 import BeautifulSoup

headers_gen = fake_headers.Headers(browser='chrome', os='win')

response = requests.get('https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python+Django+flask&excluded_text=&area=2&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=7&items_on_page=20', headers=headers_gen.generate())
html_data = response.text

hh_main = BeautifulSoup(html_data, 'lxml')
vacancies_list = hh_main.find_all('div', class_='vacancy-serp-item__layout')
vacancies_info_list = []

for vacancy in vacancies_list:
    header_tag = vacancy.find('h3')
    a_tag = header_tag.find('a')

    salary_tag = vacancy.find('span', class_='bloko-header-section-2')
    company_info_tag = vacancy.find('div', class_='vacancy-serp-item__meta-info-company')
    company_tag = company_info_tag.find('a')
    city_tag = vacancy.find('div', {'data-qa':'vacancy-serp__vacancy-address'})

    link = a_tag['href']
    if salary_tag:
        salary = salary_tag.text
    else:
        salary = 'Зарплата не указана'
    city = city_tag.text.split(',')[0]
    company = company_tag.text
    
    dict = {
        'link': link,
        'salary': salary,
        'company': company,
        'city': city
    }

    dict['salary'] = unicodedata.normalize('NFKD', salary)
    dict['company'] = unicodedata.normalize('NFKD', company)

    vacancies_info_list.append(dict)

with open('json_data', 'w') as f:
    json.dump(vacancies_info_list, f, ensure_ascii=False, indent=2)