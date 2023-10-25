"""
Web scraping with BeautifulSoup AND Selenium at Indeed.com

1. Download the Google Chrome Webdriver "https://chromedriver.chromium.org/".
2. Find the job elements.
3. Make the job elements into a list.
4. Loop through the list and copy on each job.
5. Extract the job title, company, location, and salary.
6. Change to the next page. 
7. Cloes the pop-up.
8. This code will continue scrape all of the job postings from Indeed.
9. Save it into a csv file.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

CHROME_DRIVER_PATH = '/Users/hborin/Desktop/code_demo/chromedriver-mac-x64/chromedriver'
JOBCLASS = ['jobTitle css-1u6tfqq eu4oa1w0', 'jobTitle css-mr1oe7 eu4oa1w0']
COMPANY = 'companyName'
LOCATION = 'companyLocation'
SALARY = 'css-1ihavw2 eu4oa1w0' 
URL = 'https://th.indeed.com/jobs?q=data+engineer&l=Thailand&fromage=14&vjk=940145f94de5243f'

chrome_service = ChromeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=chrome_service)
driver.get(URL)
time.sleep(5)

job_titles = []
company_names = []
locations = []
salaries = []
    
while True:
    # Get the HTML source of the current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Find all of the job posting elements on the page
    li_elements = soup.find_all('li', class_='css-5lfssm eu4oa1w0')

    for li in li_elements:
        job_title_element = li.find('h2', class_=JOBCLASS)
        job_title_text = job_title_element.find('span').text.strip() if job_title_element and job_title_element.find('span') else 'N/A'

        company_name_element = li.find('span', class_=COMPANY)
        company_name_text = company_name_element.text.strip() if company_name_element else 'N/A'

        location_element = li.find('div', class_=LOCATION)
        location_text = location_element.text.strip() if location_element else 'N/A'

        salary_element = li.find('div', class_=SALARY)
        salary_text = salary_element.text.strip() if salary_element else 'N/A'


        job_titles.append(job_title_text)
        company_names.append(company_name_text)
        locations.append(location_text)
        salaries.append(salary_text)

    # Try to find the next button
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="jobsearch-JapanPage"]/div/div[5]/div[1]/nav/div[6]/a')
        if not next_button.is_enabled():
            break
        next_button.click()
        time.sleep(5)

    except Exception as e:
        close_button = driver.find_element(By.XPATH, '//*[@id="mosaic-desktopserpjapopup"]/div[1]/button')

        # If the close button is enabled, then close the popup
        if close_button.is_enabled():
            close_button.click()
            time.sleep(5)

        else:
            next_button.click()
            time.sleep(5)

        print(e)
        break

time.sleep(5)

driver.quit()
Indeed_jobs = pd.DataFrame({'JobTitle': job_titles, 'Company': company_names, 'Location': locations, 'Salary': salaries})
print(Indeed_jobs)
Indeed_jobs.to_csv('indeed_post_job.csv', index=False)

