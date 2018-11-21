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
    If the args are correct:
    1) Takes the first 5 pages from WikiCFP
    2) Parses the Event, When, Where, and Deadline Info
    3) Stores the info in a database that is created in the same directory
    4) Prints out all events or events within the given year and month
    """

    args = sys.argv
    args_len = len(args)
    url = "http://wikicfp.com/cfp/call?conference=computer%20science"
    all_flag = False
    search_flag = False
    make_flag = False
    year = ""
    month = ""

    # Get the args, figure out if dbmake, all, search, or none of them
    if args_len == 2:
        if args[1] == "dbmake":
            make_flag = True
        elif args[1] == "all":
            all_flag = True
        else:
            print("Invalid command\n")
            usage()
            exit(0)
    elif args_len == 4:
        if args[1] == "search":
            search_flag = True
            year = args[2]
            month = args[3]
            if len(year) == 4 and len(month) == 2:
                try:
                    float(year)
                    float(month)
                except ValueError:
                    print("Date must be numeric\n")
                    usage()
                    exit(0)
            else:
                print("Date must be in YYYY MM format\n")
                usage()
                exit(0)
        else:
            print("Invalid command\n")
            usage()
            exit(0)
    else:
        usage()
        exit(0)

    if make_flag:
        # If it's dbmake, get the requests for the first 5 pages
        r = requests.get(url)
        print("Getting page 1")
        time.sleep(6)
        r2 = requests.get(url + "&page=2")
        print("Getting page 2")
        time.sleep(6)
        r3 = requests.get(url + "&page=3")
        print("Getting page 3")
        time.sleep(6)
        r4 = requests.get(url + "&page=4")
        print("Getting page 4")
        time.sleep(6)
        r5 = requests.get(url + "&page=5")
        print("Getting page 5")

        # See if requests were successful
        if r.status_code != 200 \
                or r2.status_code != 200 \
                or r3.status_code != 200 \
                or r4.status_code != 200 \
                or r5.status_code != 200:
            print("Could not successfully retrieve one or more pages from WikiCFP.")
            exit(0)

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

        # Get the right table where the info is at
        table = list(soup.findAll('table')[5])
        table2 = list(soup2.findAll('table')[5])
        table3 = list(soup3.findAll('table')[5])
        table4 = list(soup4.findAll('table')[5])
        table5 = list(soup5.findAll('table')[5])

        # Combine all 5 pages into 1 events list
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
        conn = sqlite3.connect(".\Info.db")
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS Responses')
        c.execute('CREATE TABLE Responses (Event STRING)')
        c.execute("ALTER TABLE Responses ADD COLUMN 'When' STRING")
        c.execute("ALTER TABLE Responses ADD COLUMN 'Where' STRING")
        c.execute("ALTER TABLE Responses ADD COLUMN 'Deadline_Info' STRING")
        c.execute("ALTER TABLE Responses ADD COLUMN 'Year' STRING")
        c.execute("ALTER TABLE Responses ADD COLUMN 'Month' STRING")
        conn.commit()

        # Populate the DB table
        j = 0
        while j < len(events):
            name = events[j].get_text().split("\n")
            event = "(" + name[1] + ") " + name[2]
            j = j + 1
            data = events[j].get_text().split("\n")
            when = data[1]
            where = data[2]
            deadline = data[3]

            # Parse the When to get the year and month
            y, m = parse(when)

            # Store all the info in the DB
            c.execute("INSERT INTO Responses VALUES (?, ?, ?, ?, ?, ?)", (event, when, where, deadline, y, m))
            j = j + 1

        # Finally close the connection
        conn.commit()
        c.close()
        print("Database successfully created and populated.")

    elif all_flag:
        # Fetch all the data from the db, print it all out
        conn = sqlite3.connect(".\Info.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM Responses")
        except sqlite3.OperationalError:
            print("No database exists")
            exit(0)
        all_data = c.fetchall()
        c.close()
        for row in all_data:
            print("Event: " + row[0])
            print("When: " + row[1])
            print("Where: " + row[2])
            print("Deadline Info: " + row[3] + '\n')

    elif search_flag:
        # Fetch the queried data from the db, print it all out
        conn = sqlite3.connect(".\Info.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM Responses WHERE Year=? AND Month=?", (year, month))
        except sqlite3.OperationalError:
            print("No database exists")
            exit(0)
        when_data = c.fetchall()
        c.close()
        if len(when_data) == 0:
            # If there's no event during that specific year and month, print this
            print("There are no events during this year and month.")

        else:
            # Print out all the matching events
            for row in when_data:
                print("Event: " + row[0])
                print("When: " + row[1])
                print("Where: " + row[2])
                print("Deadline Info: " + row[3] + '\n')


def parse(when):
    """
    Takes the when info, extracts the year and month of the starting date of the event
    :param when: the info
    :return: Tuple: the year and the month
    """

    if when == "N/A":
        # If there isn't a specific date, 0 out the year and month
        return "0000", "00"
    else:
        # Convert the month to it's corresponding 2 digit number representation
        m = ""
        dates = when.split(" ")
        y = dates[2]
        if dates[0] == "Jan":
            m = "01"
        elif dates[0] == "Feb":
            m = "02"
        elif dates[0] == "Mar":
            m = "03"
        elif dates[0] == "Apr":
            m = "04"
        elif dates[0] == "May":
            m = "05"
        elif dates[0] == "Jun":
            m = "06"
        elif dates[0] == "Jul":
            m = "07"
        elif dates[0] == "Aug":
            m = "08"
        elif dates[0] == "Sep":
            m = "09"
        elif dates[0] == "Oct":
            m = "10"
        elif dates[0] == "Nov":
            m = "11"
        elif dates[0] == "Dec":
            m = "12"

        return y, m


def usage():
    """
    Displays usage information
    :return: None
    """

    print("Usage: 351crawler.py <dbmake|all|search> <optional-argument-1> <optional-argument-2>")
    print("\tdbmake (Required) (1)Fetches the first five pages from the WikiCFP")
    print("\t\t\t\t\t  (2)Parses the Event, When, Where, and Deadline info ")
    print("\t\t\t\t\t  (3)Stores it in a database.")
    print("\tall (Required)    Prints out all the event, when, where, and deadline info you've fetched.")
    print("\tsearch (Required) Takes two args for <year> and <month>. Queries the events that match.")
    print("\t\t\t\t\t  The format of year is YYYY and the month is MM.")


if __name__ == "__main__":
    main()
