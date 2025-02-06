from bs4 import BeautifulSoup
import requests
import json
import os
import re

def isValidDate(date_string):
    pattern = r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2}, \d{4}$"
    return bool(re.match(pattern, date_string))

def extractBookData(soup):
    jsonData = {}
    span_items = soup.find('div', attrs={'class': 'bookinfo_sectionwrap'}).find_all('span', attrs={'dir': 'ltr'})
    jsonData["published"] = "Jan 1, 0001" # use dfault date 
    for span in span_items:
        text = span.get_text()
        if(isValidDate(text)):
            jsonData["published"] = text
            break
    

    labels = soup.find_all('td', attrs={'class': 'metadata_label'})
    values = soup.find_all('td', attrs={'class': 'metadata_value'})

    for i, label in enumerate(labels):
        # print(label.get_text(),":", values[i].get_text())
        if("isbn" == label.get_text().lower()):
            isbns = values[i].get_text().split(',')
            for isbn in isbns:
                isbn = isbn.strip()
                if(10 == len(isbn)):
                    jsonData["isbn_10"] = isbn
                if(13 == len(isbn)):
                    jsonData["isbn_13"] = isbn
        elif("subjects" == label.get_text().lower()):
            subjects = values[i].get_text().replace("\xa0›\xa0",'/').split('/')
            jsonData[label.get_text().lower()] = subjects
        elif("export citation" == label.get_text().lower()):
            citations = values[i].get_text().replace("\xa0",'/').split('/')
            jsonData[label.get_text().lower()] = citations
        else:
            jsonData[label.get_text().lower()] = values[i].get_text()

    jsonData["img_url"] = soup.find('img', attrs={'title': 'Front Cover'})['src']

    return jsonData

def getBookLinks(url):
    # Fetch the HTML content from a website
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # with open("page.html", "w") as f:
    #     f.write(requests.get(url).text)

    # Extract data from the parsed HTML
    # Example: Find all the links on the page

    books = soup.find_all("a", attrs={'class': "gb-bookshelf-hover-card hover-card-attach-point"})
    links = []
    for book in books:
        # print(book.get_text())
        # print(book.get("href"))
        links.append(book.get("href"))
    return links


for i in range(2300, 3800, 100):
    print("Batch", i,"/3800")
    url = f"https://books.google.com/books?lr=&uid=117522004192189783614&as_coll=1001&sa=N&start={i}&num=100"

    links = getBookLinks(url)

    for link in links:
        # Fetch the HTML content from a website
        response = requests.get(link)
        html_content = response.content

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')


        book_data = extractBookData(soup)

        # Define the file path
        file_path = "books_data_interesting.json"

        # Check if the file exists and has valid JSON
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    if not isinstance(data, list):  # Ensure it's a list
                        data = []
                except json.JSONDecodeError:
                    data = []  # If JSON is invalid, reset to an empty list
        else:
            data = []  # Initialize with an empty list if file doesn't exist

        # Append new data
        data.append(book_data)

        # Write back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        # print("Data successfully appended to JSON file!")
    print("Batch Data Appended to JSON")
