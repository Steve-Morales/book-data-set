# Info
This dataset was compiled from Google Books (https://books.google.com/). The script uses BeautifulSoup4 in Python to exract the data. 

Steps:
- start with url at [https://books.google.com/books?lr=&num=100&uid=117522004192189783614&as_coll=1019&sa=N&start=0](https://books.google.com/books?lr=&num=100&uid=117522004192189783614&as_coll=1019&sa=N&start=0)<br />**Note: notice the `num=100` and `start=0` which sets the number of books to view at a time and index in he list**

- retrieve the links to each book's data for the current list of books
- for each link
    - extract the data from the book
    - append to JSON file

# Setup
Using Python 3.11

```shell
python -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate # start virtual enviornment
pip install requests
pip install beautifulsoup4
python3 scraper.py
```

# Methods
```py
"""
@param  bs4.BeautifulSoup   entire parsed document in html format containing the book information
@return Dictionary          keys and values making up the metadata of a book
"""
def extractBookData(soup)

"""
@param  str         url containing a list of books
@return List<str>   list of urls to a book's metadata
"""
def getBookLinks(url)
```

# Main (Body)
A simple for-loop which iterates to get ~2100 books and append it to a JSON file as a grows