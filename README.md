# BOM_scraper
Scraping data from the Australian Bureau of Meteorology website using Selenium

Required packages:
- selenium
- time
- logging
- pandas
- os
- zipfile
- glob

Steps to get started:
- fork this repo
- specify location of 'weatherAutomation' folder for 'filePath' variable
- ensure Selenium webdriver is installed for your version of Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
  - update the 'subset' variable in 'getStations()' to target required number of weather stations
    - Default value is set to 3
- run command 'python bom.py' in terminal to get weather station data for QLD.
 
  
    
