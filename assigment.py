import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import date

# Define the URL to scrape
url = "https://www.theverge.com"

# Send a GET request to the URL and get its HTML content
response = requests.get(url)
content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# Find all the articles on the page
articles = soup.find_all("div", {"class": "c-entry-box--compact__body"})

# Initialize an empty list to store the data
data = []

# Loop through each article and extract the relevant information
for i, article in enumerate(articles):
    headline = article.find("h2").text.strip()
    url = article.find("a")["href"]
    author = article.find("span", {"class": "c-byline__item"}).text.strip()
    date_str = article.find("time")["datetime"].split("T")[0]
    date = date.fromisoformat(date_str)
    data.append({"id": i, "url": url, "headline": headline, "author": author, "date": date})

# Create a pandas DataFrame from the data list
df = pd.DataFrame(data)

# Define the filename for the CSV file
filename_csv = date.today().strftime("%d%m%Y") + "_verge.csv"

# Save the DataFrame to the CSV file
df.to_csv(filename_csv, index=False)

# Create an SQLite connection and cursor
conn = sqlite3.connect("theverge.db")
c = conn.cursor()

# Create the table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS articles 
             (id INTEGER PRIMARY KEY, url TEXT, headline TEXT, author TEXT, date TEXT)''')

# Insert the data into the table
for row in data:
    c.execute("INSERT OR IGNORE INTO articles (id, url, headline, author, date) VALUES (?, ?, ?, ?, ?)", 
              (row["id"], row["url"], row["headline"], row["author"], row["date"]))

# Commit the changes and close the connection
conn.commit()
conn.close()
