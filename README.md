Extract Data from Indeed Website
============

  The code is a Python script that uses BeautifulSoup to extract job titles, company names, locations, and salaries from Indeed job listings. The script works by first parsing **the HTML source code** of a Indeed job search page using BeautifulSoup. 
  Once the HTML is parsed, the script uses method to **find all of** the elements on the page These elements contain the individual **job listings**.
**After the script has processed** all of the job listings on the page, **it checks to see if there is a next button**. If there is a next button and it is enabled, the script clicks the button to navigate to the next page of job listings. **If the close button is enabled, then close the popup**.
  
