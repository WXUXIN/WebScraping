#This will not run on online IDE
import requests
from bs4 import BeautifulSoup
import csv
import requests
filename = 'agents.csv'

emails = []
namesList = []
finalList = []

targetUrl = "https://www.mummysmarket.com.sg/participating-brands"

# Loop through all pages
response = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': '9653182d-7af0-43fe-a907-33337d5c0d19',
        'url': targetUrl
    },
)

#show response content 
soup = BeautifulSoup(response.content, 'html5lib')

# Loop through potential tagss
table = list(soup.findAll('img', attrs = {'class':'itemimg'}))

for tag in table:
    src = tag['src']
    filename = src.split('/')[-1].split('.')[0:-1]
    finalList += [filename]

print(finalList)
with open('baby.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(finalList)


# filtedTable = list(filter(lambda x : x.text == "Email", table))
# returnTable = map(lambda y : y['href'], filtedTable)
# emails = emails + list(map(lambda z :z[7:] ,returnTable))

# #Find names of people
# names = soup.findAll('div', attrs = {'class': "content-wrap flex-grow-1"})

# names = list(map(lambda x : list(x.h5.text.split()), names))
# namesList += names
# Read the existing data from the Excel sheet

# with open(filename, 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Emails'])  # Write the header row
    
#     for email in emails:
#         writer.writerow([email]) 


#2339 : Page 51 Done
#22/06/2023 : Page 100 Done
# with open(filename, 'a', newline='') as f:
#     writer = csv.writer(f)
    
#     for email in emails:
#         writer.writerow([email])  # Append each email as a new row``


# max_name_length = max(map(lambda x : len(x), namesList)) 

# max_name_diff = max_name_length if max_name_length > 6 else 6

# # # with open('agents.csv', 'r', encoding='utf-8') as csvfile:
# # #     reader = csv.reader(csvfile)
# # #     existing_data = list(reader)

# # # for row in existing_data:
# # #     updated_row = names.pop(0) + row  # Insert names at the left side of each row
# # #     updated_data.append(updated_row)

# for i in range(len(namesList)):

#     gap_diff = max_name_diff - len(namesList[i])

#     if gap_diff > 0:
#         row = namesList[i] + (gap_diff) * [" "]  + [emails[i]]
#     else:
#         row = namesList[i] + [emails[i]]
    
#     finalList.append(row)

# # Write the updated data back to the Excel sheet
# with open('agents.csv', 'a', encoding='utf-8', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(finalList)