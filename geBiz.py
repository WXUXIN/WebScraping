# This will not run on online IDE
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
url = "https://www.gebiz.gov.sg/"
driver.get(url)

time.sleep(2)

search_tag = driver.find_element(
    By.XPATH, '//*[@id="contentForm:j_idt187_searchBar_BUTTON-GO"]')

search_tag.click()

main_window = driver.current_window_handle
# Fix issue with the whol

# Define a list to store the extracted data
companies = []

for page_number in range(1, 65):

    # We try for each page number, if the page number does not exist, or is there
    # is any other issue, we break the loop and just store the values we have

    try:
        time.sleep(2)

        print(f"Page No.{page_number}")
        driver.execute_script("window.scrollTo(0, 0);")

        tags = driver.find_elements(
            By.CLASS_NAME, 'commandLink_TITLE-BLUE')

        tags = [tag.get_attribute("href") for tag in tags]

        print(f"Companies in page {page_number}: {len(tags)}")
        print(tags)
        print("-----------------------------------------\n")


        # Loop through each tag and extract the company information
        for tag in tags:

            # Try except to skip over the tags that are not clickable
            # Or those tags with issues

            try:
                # Wait for the element to be visible and clickable
                # Click on the tag to open the company page
                driver.execute_script(f'window.open("{tag}");')

                # Wait for the new page to load (you can adjust the sleep duration as needed)
                time.sleep(5)

                # Switch to the new page's window handle
                driver.switch_to.window(driver.window_handles[-1])

                # //*[@id="contentForm:j_idt468:j_id23:j_idt469"]
                # //*[@id="contentForm:j_idt468:j_id23:j_idt469"]

                info_tag = driver.find_element(
                    By.ID, 'contentForm:j_idt449')
                # By.ID, 'contentForm:j_idt451:j_id23:j_idt452')

                try:
                    # Find all the span tags inside info_tag
                    span = info_tag.find_element(By.TAG_NAME, 'span')

                    # Find tag based on style

                    email = span.text.strip()
                except:
                    email = "N/A"

                try:
                    # Find all the span tags inside info_tag
                    name = info_tag.find_element(
                        By.CLASS_NAME, 'form2_ROW-TABLE').text.strip()

                except:
                    name: "N/A"

                print(f"Name: {name}")
                print(f"Email: {email}")

                # # Store the information in an object

                company_info = {
                    "name": name,
                    "email": email
                }

                # # Add the object to the main list
                companies.append(company_info)

                # Close the new page
                driver.close()

                # Switch back to the main page
                driver.switch_to.window(main_window)

            except Exception as e:
                print("Error in tag: ", tag, e)

        # After accessing all the comapnies in the page, click on the next page button
        if page_number < 64:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(2)
            
            next_button = driver.find_element(
                By.ID, f'contentForm:j_idt831:j_idt882_Next_{page_number + 1}')
            
            next_button.click()

    except Exception as e:
        print("Error in page number: ", page_number, "Error:", e)


# # Create a DataFrame from the companies list
df = pd.DataFrame(companies)

# Export the DataFrame to an Excel file
df.to_excel("geBiz.xlsx", index=False)

# Close the browser
driver.quit()
