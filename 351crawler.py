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
    URL = "http://wikicfp.com/cfp/call?conference=computer%20science"
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
    r = requests.get(URL + "&page=2")
    """
    time.sleep(6)
    r2 = requests.get(URL + "&page=2")
    time.sleep(6)
    r3 = requests.get(URL + "&page=3")
    time.sleep(6)
    r4 = requests.get(URL + "&page=4")
    time.sleep(6)
    r5 = requests.get(URL + "&page=5")
    """
    # Parse the requests
    p = r.text
    soup = BeautifulSoup(p, "html.parser")
    table = list(soup.findAll('table')[5])
    events = []
    i = 2
    while i <= 80:
        events.append(table[i])
        i = i + 2

    """
    # Make the database and table
    conn = sqlite3.connect("Info.db")
    c = conn.cursor()

    c.execute('CREATE TABLE (Responses) ((Event) (STRING))')
    c.execute("ALTER TABLE (Responses) ADD COLUMN '(When)' (STRING)")
    c.execute("ALTER TABLE (Responses) ADD COLUMN '(Where)' (STRING)")
    c.execute("ALTER TABLE (Responses) ADD COLUMN '(Deadline_Info)' (STRING)")
    """

    # Populate the DB table
    j = 0
    while j < 40:
        name = events[j].get_text().split("\n")
        event = name[1] + name[2]
        # c.execute("INSERT INTO Responses (Event) VALUES (?)", event)
        j = j + 1
        data = events[j].get_text().split("\n")
        when = data[1]
        where = data[2]
        deadline = data[3]
        # c.execute("INSERT INTO Responses (When) VALUES (?)", when)
        # c.execute("INSERT INTO Responses (Where) VALUES (?)", where)
        # c.execute("INSERT INTO Responses (Deadline_Info) VALUES (?)", deadline)
        j = j + 1

    if all_flag:
        # In progress, only used print for testing
        print("all")

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
