#!/usr/bin/env python
# coding: utf-8

# In[147]:


import selenium, time, logging, pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os, os.path, zipfile, glob

logging.basicConfig(level=logging.DEBUG)

#specify location of 'weatherAutomation' folder
filePath = "/Users/rohinchhabra/Desktop/"

#setting default download folder
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : filePath + "/weatherAutomation/data"}
chromeOptions.add_experimental_option("prefs",prefs)

#specifying chromedriver file

chromedriver = filePath + "/weatherAutomation/chromedriver"

def getStations():
    
    #read station list
    weather_stat = pd.read_csv("station_list.csv")
    weather_stat = weather_stat.rename(columns={"STA":"state"})

    #*** update this command for any other state from the station_list.csv file***#
    qld_stations = weather_stat[(weather_stat.state == 'QLD')]

    #filter on active stations
    qld_active = qld_stations[(qld_stations.End == '..')]
    qld_active_stations = list(qld_active['Site'].unique())

    #filter on stations which have ended during or after 2001
    qld_inactive = qld_stations[(qld_stations.End >= '2001')]

    #concat the two DFs for a total list of weather stations
    frames = [qld_active, qld_inactive]
    qld_master = pd.concat(frames)

    #extract Site IDs only
    qld_master_stations = list(qld_master['Site'].unique())
    
#     len(qld_master_stations)
#     qld_master_stations.index('40785')
    
    #get remaining data after 'timeout'
    subset = qld_master_stations[10:13]
    
    return subset

def getData(data):
#update list variable with station IDs
    for i in data:
        driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

        #navigate to BOM through webdriver
        #*** update as per desired website name ***#
        driver.get("http://www.bom.gov.au/climate/data/")

        #selecting option from dropdown for Rainfall
        #*** update this variable with relevent element_id for required information ***#
        data_about = Select(driver.find_element_by_id('ncc_obs_code_group'))
        data_about.select_by_value('2')

        #choose Daily data
        #*** choose the type of data you are after, daily or monthly ***#
        daily_rainfall = driver.find_element_by_id('dt1')
        daily_rainfall.click()

        #navigate to station Id text box
        #*** choose the correct text box to navigate to ***#
        station_id = driver.find_element_by_id('p_stn_num').send_keys(i)

    # station_id.click()
    # station_id.send_keys('27031')

        #get data
        get_data = driver.find_element_by_id('getData')
        get_data.click()

        #focus on new window opened by Chrome
        window_after = driver.window_handles[1]
        #get all years of data
        driver.switch_to.window(window_after)

        try:
            data_link = driver.find_element_by_xpath('//*[@id="content-block"]/ul[2]/li[2]/a')

            if (data_link.is_displayed()):

                data_link.click()
                time.sleep(5)
                logging.info('%s Downloaded ', i)
                driver.quit()  

            else:
                time.sleep(5)
                logging.info('%s Page refresh ', i)
                driver.refresh()

        except selenium.common.exceptions.NoSuchElementException:
            pass
            logging.error('%s Data not available ', i)
            driver.quit()
    return

def zipFile():
    dir_name = filePath + '/weatherAutomation/data'
    extension = ".zip"

    os.chdir(dir_name) # change directory from working dir to dir with files

    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(dir_name) # extract file to dir
            zip_ref.close() # close file
            os.remove(file_name) # delete zipped file

    #creating a backup of all files before deleting .txt files and merging csvs
    os.system('zip -r -D weather_backup.zip *')

    #merging all CSVs
    csvs_only = glob.glob(dir_name + "/*.csv") 
    df = pd.concat((pd.read_csv(f, header = 0) for f in csvs_only))
    df.to_csv("master_weather.csv")

    #deleting all files except backup and master_weather
    #!/usr/bin/env python
    os.system('mv -v master_weather.csv weather_backup.zip ..')
    os.system('rm *')
    os.chdir( filePath + '/weatherAutomation')
    os.system('mv weather_backup.zip ' + dir_name)
    os.system('mv master_weather.csv ' + dir_name)
    
    return

def main():
    getData(getStations())
    print("Data collection complete")
    zipFile()
    print("Backup and Master file created")
    
main()
    



# In[ ]:




