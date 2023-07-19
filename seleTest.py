from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re


# Initialize the Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open the URL
url = "https://www.startupsg.gov.sg/directory/startups/"
driver.get(url)

time.sleep(3)

# Fix issue with the whol

# Define a list to store the extracted data
companies = []

for page_number in range(1, 478):

    # We try for each page number, if the page number does not exist, or is there
    # is any other issue, we break the loop and just store the values we have

    try:

        print(f"Page No.{page_number}")

        try:
            dismiss_tag = driver.find_element(
                By.XPATH, '/html/body/div[1]/div/a')
            dismiss_tag.click()
        except:
            pass

        if (page_number <= 5):
            # Click on number tag for page number
            page_num_tag = driver.find_element(By.XPATH,
                                            f'//*[@id="app"]/div[14]/div/main/div/div/div/section/section/div[3]/ul/li[{page_number + 1}]/button')

        elif (page_number >= 474):
            add_number = page_number - 474
            page_num_tag = driver.find_element(By.XPATH,
                                            f'//*[@id="app"]/div[14]/div/main/div/div/div/section/section/div[3]/ul/li[{7 + add_number}]/button')

        else:
            page_num_tag = driver.find_element(
                By.XPATH, '//*[@id="app"]/div[14]/div/main/div/div/div/section/section/div[3]/ul/li[7]/button')

    # #474
    # //*[@id="app"]/div[14]/div/main/div/div/div/section/section/div[3]/ul/li[7]/button

    # #475
    # //*[@id="app"]/div[14]/div/main/div/div/div/section/section/div[3]/ul/li[8]/button

    # #476
    # //*[@id="app"]/div[14]/div/main/div/div/div/section/section/div[3]/ul/li[9]/button

    # #477
    # //*[@id="app"]/div[14]/div/main/div/div/div/section/section/div[3]/ul/li[10]/button

        # if (page_number <= 242):
        #     time.sleep(5)

        #     print("Before Click")
        #     page_num_tag.click()

        #     print("Clicked")
        #     # Wait for the new page to load (you can adjust the sleep duration as needed)
        #     time.sleep(5)

        #     driver.execute_script("window.scrollTo(0, 0);")

        #     print(f"Companies in page {page_number}: {len(tags)}")
        #     print("-----------------------------------------\n")

        #     # We want to continue at page 243, so if page number is less than 243, we skip
        #     continue

     
        if (page_number <= 242):
            time.sleep(5)

        else:
            time.sleep(3)

        page_num_tag.click()

        # Wait for the new page to load (you can adjust the sleep duration as needed)
        if (page_number <= 242):
            time.sleep(5)

        else:
            time.sleep(3)

        driver.execute_script("window.scrollTo(0, 0);")

        # Find all the tags with class 'entity__display-name'
        tags = driver.find_elements(By.CLASS_NAME, 'entity__display-name')

        print(f"Companies in page {page_number}: {len(tags)}")
        print("-----------------------------------------\n")

        # We want to continue at page 243, so if page number is less than 243, we skip
        if (page_number <= 242):
            continue


        # Loop through each tag and extract the company information
        for tag in tags:

            # Try except to skip over the tags that are not clickable
            # Or those tags with issues

            try:
                # Wait for the element to be visible and clickable
                time.sleep(5)

                # Click on the tag to open the company page
                tag.click()

                # Wait for the new page to load (you can adjust the sleep duration as needed)
                time.sleep(5)

                # Switch to the new page's window handle
                driver.switch_to.window(driver.window_handles[-1])

                # Extract the company name from the new page
                try:
                    company_name = driver.find_element(By.XPATH,
                                                './/*[@id="app"]/div[8]/div/main/div/div/section/div[1]/div/section/div/div/div[1]/header/div/div[2]/h1').text
                
                    company_name = re.sub(r"\bpte\.?\b|\bltd\.?\b|\.", "", company_name, flags=re.IGNORECASE).strip()

                except:
                    company_name = "N/A"

                try:
                    # Extract the email from the new page
                    email = driver.find_element(By.XPATH,
                                                '//*[@id="general"]/div/div/div/div[2]/div/div[2]/div/ul[1]/li[3]/a').text
                except:
                    email = "N/A"
                
                try:
                    # Extract the email from the new page
                    phone_num_li = driver.find_element(By.CLASS_NAME,
                                                'phone')
                    
                    phone_num = phone_num_li.find_element(By.TAG_NAME, 'span').text

                except:
                    phone_num = "N/A"

                # Store the information in an object

                company_info = {
                    "name": company_name,
                    "email": email,
                    "phone": phone_num
                }

                # Add the object to the main list
                companies.append(company_info)

                # Close the new page
                driver.close()

                # Switch back to the main page
                driver.switch_to.window(driver.window_handles[0])

            except:
                pass

    except:
        print("Error in page number: ", page_number)


# Create a DataFrame from the companies list
df = pd.DataFrame(companies)

# Export the DataFrame to an Excel file
df.to_excel("companies2.xlsx", index=False)

# Close the browser
driver.quit()
