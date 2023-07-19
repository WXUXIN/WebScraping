from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time 

# Initialize the Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Initialize the wait
wait = WebDriverWait(driver, 10)

# Open the URL
main_url = "https://www.raise.sg/directory/directories/default.html?pbs=QnVzaW5lc3MgU3VwcG9ydCBBY3Rpdml0aWVzIChlZzogR2VuZXJhbCBDb25zdWx0YW5jeSwgRXZlbnQgTWd0KQ%3D%3D&bs=MTY%3D"
driver.get(main_url)

# Define a list to store the extracted data
companies = []

wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'groupCheckbox')))

driver.find_element(By.CLASS_NAME, 'filter-checkbox').click()

checkBoxes = driver.find_elements(By.CLASS_NAME, 'groupCheckbox')

for checkBox in checkBoxes:
    label = checkBox.find_element(By.TAG_NAME, 'label')
    
    # Scroll to the checkbox
    driver.execute_script("arguments[0].scrollIntoView();", label)
    
    time.sleep(1)

    # Click the checkbox
    driver.execute_script("arguments[0].click();", label)

search_btn = driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div/div[3]/div/div/a[1]')
driver.execute_script("arguments[0].scrollIntoView();", search_btn)

time.sleep(3)

# Click the search button
driver.execute_script("arguments[0].click();", search_btn)

# # Store the current window handle
main_window = driver.current_window_handle

try:
    for page_number in range(1, 20):

        try:
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pagenav')))
            print(f"Page No.{page_number}")

            if (page_number <= 6):
                page_num_tag = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[3]/div[4]/ul/li[{page_number}]/a')
            
            elif (page_number > 6 and page_number <= 16):
                page_num_tag = driver.find_element(By.XPATH, '//*[@id="contents"]/div[3]/div[4]/ul/li[7]/a')
            else:
                page_num_tag = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[3]/div[4]/ul/li[{page_number - 16 + 7}]/a')
                
            page_num_tag.click()
            driver.execute_script("window.scrollTo(0, 0);")
            
            # Wait for the elements to be present and store them in tags variable
            tags = driver.find_elements(By.CLASS_NAME, "intro-image")

            # This will get a list of all 'a' tags enclosed by the 'div' tags
            links = [tag.find_element(By.TAG_NAME, "a") for tag in tags]

            # This will extract the href attribute from each 'a' tag
            hrefs = [link.get_attribute("href") for link in links]

            print(f"Companies in page {page_number}: {len(tags)}")
            print("-----------------------------------------\n")

            # Loop through each tag and extract the company information
            for url in hrefs:
                print("Opening company page")
                
                # Open a new tab
                # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
                driver.execute_script(f'window.open("{url}");')

                time.sleep(3)
                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])
                
                # Load the URL in the new tab
                # driver.get(url)

                try:
                    # Extract the company name from the new page
                    try:
                        company_name = wait.until(EC.presence_of_element_located((By.XPATH, 
                            '//*[@id="main-content"]/div/div[2]/div[2]/div/div[1]/div[2]/h3/span'))).text
                        company_name = re.sub(r"\bpte\.?\b|\bltd\.?\b|\.", "", company_name, flags=re.IGNORECASE).strip()

                    except:
                        company_name = "N/A"

                    try:
                        # Extract the email from the new page
                        email = wait.until(EC.presence_of_element_located((By.XPATH, 
                            '//*[@id="main-content"]/div/div[2]/div[3]/div/div[2]/a'))).text
                    except:
                        email = "N/A"

                    # Store the information in an object
                    company_info = {
                        "name": company_name,
                        "email": email
                    }

                    # Add the object to the main list
                    companies.append(company_info)

                except Exception as e:
                    print("Error in company: ", e)
                    
                # Close the current tab
                driver.close()
                
                # Switch back to the main tab
                driver.switch_to.window(main_window)
            
        except Exception as e:
            print("Error in page number: ", page_number, e)
            
except Exception as e:
    pass

# Create a DataFrame from the companies list
df = pd.DataFrame(companies)

# Export the DataFrame to an Excel file
df.to_excel("SOCIALe2.xlsx", index=False)

print(companies)
# Close the browser
driver.quit()
