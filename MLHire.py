from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open the URL
url = "https://www.linkedin.com/hiring/jobs/3656353456/applicants/15438649816/detail/?r=UNRATED%2CGOOD_FIT%2CMAYBE"
driver.get(url)

driver.find_element(By.XPATH,
                    '/html/body/div[1]/main/div/p/a').click()

time.sleep(3)

driver.find_element(By.XPATH,
                    '//*[@id="email-address"]').send_keys('wangxuxin1@gmail.com')

driver.find_element(By.XPATH,
                    '//*[@id="password"]').send_keys('91862453%Wa')