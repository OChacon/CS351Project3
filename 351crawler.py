"""
Starbuck Beagley & Oscar Chacon
CSCI-351

Project 3: Simple HTTP Crawler
"""

import sys
import time
import requests
import sqlite3
from bs4 import BeautifulSoup


def main():
    """
    Main function
    """

    args = sys.argv
    args_len = len(args)
    url = "http://wikicfp.com/cfp/call?conference=computer%20science"
    all_flag = False
    search_flag = False
    year = ""
    month = ""

    # Get the args, figure out if all, search, or neither
    if args_len == 2:
        if args[1] == "dbmake|all":
            all_flag = True
        else:
            usage()
            exit(0)
    elif args_len == 4:
        if args[1] == "dbmake|search":
            search_flag = True
            year = args[2]
            month = args[3]
        else:
            usage()
            exit(0)
    else:
        usage()
        exit(0)

    # If it's all or search, get the requests for the first 5 pages
    r = requests.get(url)
    time.sleep(6)
    r2 = requests.get(url + "&page=2")
    time.sleep(6)
    r3 = requests.get(url + "&page=3")
    time.sleep(6)
    r4 = requests.get(url + "&page=4")
    time.sleep(6)
    r5 = requests.get(url + "&page=5")

    # Parse the requests
    p = r.text
    p2 = r2.text
    p3 = r3.text
    p4 = r4.text
    p5 = r5.text

    soup = BeautifulSoup(p, "html.parser")
    soup2 = BeautifulSoup(p2, "html.parser")
    soup3 = BeautifulSoup(p3, "html.parser")
    soup4 = BeautifulSoup(p4, "html.parser")
    soup5 = BeautifulSoup(p5, "html.parser")

    table = list(soup.findAll('table')[5])
    table2 = list(soup2.findAll('table')[5])
    table3 = list(soup3.findAll('table')[5])
    table4 = list(soup4.findAll('table')[5])
    table5 = list(soup5.findAll('table')[5])

    events = []
    i = 2
    while i <= 80:
        events.append(table[i])
        i = i + 2

    i = 2
    while i <= 80:
        events.append(table2[i])
        i = i + 2

    i = 2
    while i <= 80:
        events.append(table3[i])
        i = i + 2

    i = 2
    while i <= 80:
        events.append(table4[i])
        i = i + 2
    i = 2

    while i <= 80:
        events.append(table5[i])
        i = i + 2

    # Make the database and table
    conn = sqlite3.connect("D:\\Users\Oscar\Sqlite\sqlite-tools-win32-x86-3250300\Info.db")
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS Responses')
    c.execute('CREATE TABLE Responses (Event STRING)')
    c.execute("ALTER TABLE Responses ADD COLUMN 'When' STRING")
    c.execute("ALTER TABLE Responses ADD COLUMN 'Where' STRING")
    c.execute("ALTER TABLE Responses ADD COLUMN 'Deadline_Info' STRING")

    # Populate the DB table
    j = 0
    while j < 200:
        name = events[j].get_text().split("\n")
        event = name[1] + " " + name[2]
        j = j + 1
        data = events[j].get_text().split("\n")
        when = data[1]
        where = data[2]
        deadline = data[3]
        c.execute("INSERT INTO Responses VALUES (?, ?, ?, ?)", (event, when, where, deadline))
        j = j + 1

    if all_flag:
        # Fetch all the data from the db, print it all out
        c.execute("SELECT * FROM Responses")
        all_data = c.fetchall()
        c.close()
        for row in all_data:
            print("Event: " + row[0])
            print("When: " + row[1])
            print("Where: " + row[2])
            print("Deadline Info: " + row[3] + '\n')

    if search_flag:
        # In progress, only used print for testing
        print("search")


def usage():
    """
    Displays usage information
    :return: None
    """

    print("Usage: 351crawler.py <dbmake|search> <optional-argument-1> <optional-argument-2>")
    print("\tdbmake (Required) (1)Fetches the first five pages from the WikiCFP")
    print("\t(2)Parses the Event, When, Where, and Deadline info (3)Stores it in a database.")
    print("\tall (Required) Prints out all the event, when, where, and deadline info you've fetched.")
    print("\tsearch (Required) Takes two args for <year> and <month>. Queries the events that match.")


if __name__ == "__main__":
    main()
