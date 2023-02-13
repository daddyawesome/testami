import pandas as pd 
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os


# Get the current working directory
current_directory = os.getcwd()

# Set the download directory to the current working directory
download_directory = os.path.join(current_directory, "data")

# Handle the download
options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": download_directory,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
 })

# Load the website
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
driver.get("https://jobs.homesteadstudio.co/data-engineer/assessment/download/")

# Wait for 5 seconds to load the webpage completely
time.sleep(5)

# Locate the download button
download_button = driver.find_element(By.CLASS_NAME, 'wp-block-button__link')
#download_button = driver.find_element(By.XPATH, "//a[@class='wp-block-button__link wp-element-button']")

# Trigger the download
download_button.click()

# Wait for 5 seconds to complete download
time.sleep(5)

# Close the browser
driver.quit()

print("Download done!")
#read the downloaded excel file
df = pd.read_excel("data/skill_test_data.xlsx", sheet_name ="data")

#select the neede columns
df_new = df[["Platform (Northbeam)","Spend","Attributed Rev (1d)","Imprs","Visits","New Visits","Transactions (1d)","Email Signups (1d)"]]

#Pivot
df_pivot = df_new.groupby(["Platform (Northbeam)"]).sum()
df_pivot = df_pivot.reset_index()
df_pivot = df_pivot.sort_values("Attributed Rev (1d)", ascending=False)

# Connect to an SQLite database
conn = sqlite3.connect('data/test.db')

# Save the dataframe as a new table in the database
df_pivot.to_sql('pivot_table', con=conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("done with pivot_table to SQLITE")