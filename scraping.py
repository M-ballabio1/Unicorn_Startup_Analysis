import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a GET request to the URL
url = 'https://www.holoniq.com/healthtech-unicorns'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table element with class 'grid-table'
table = soup.find('div', class_='grid-table')

# Find all rows in the table except the header row
rows = table.find_all('div', class_='table-row')[1:]

# Create empty lists to store the data
company = []
country = []
industry = []
last_round = []
type_ = []
valuation = []

# Loop through each row and extract the data
for row in rows:
    cols = row.find_all('div', class_='table-col')
    company.append(cols[0].find('a').text)
    country.append(cols[1].text)
    industry.append(cols[2].text)
    last_round.append(cols[3].text)
    type_.append(cols[4].text)
    valuation.append(cols[5].text)

# Create a DataFrame to store the data
df = pd.DataFrame({
    'company': company,
    'country': country,
    'industry': industry,
    'last round': last_round,
    'type': type_,
    'valuation': valuation
})

# Save the DataFrame as an Excel file
df.to_excel('healthtech_unicorns.xlsx', index=False)