"""
Starbuck Beagley & Oscar Chacon
CSCI-351

Project 3: Simple HTTP Crawler
"""

import sys
import socket
import math


def main():
    """
    Main function
    """

    args = sys.argv
    args_len = len(args)
    all_flag = False
    search_flag = False
    year = ""
    month = ""

    if args_len == 1:
        if args[1] == "dbmake|all":
            all_flag = True
        else:
            usage()
            exit(0)
    elif args_len == 3:
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


def usage():
    """
    Displays usage information
    :return: None
    """

    print("Usage: 351crawler.py <dbmake|search> <optional-argument-1> <optional-argument-2>")
    print("\tdbmake (Required) (1)Fetches the first five pages from the WikiCFP")
    print("\t(2)Parses the Event, When, Where, and Deadline info (3)Stores it in a database.")
    print("\tall (Required) Prints out all the event, when, where, and deadline info you've fetched.")
    print("\tsearch (Required) Takes two args for <year> and <month>. Looks update the events that match.")


if __name__ == "__main__":
    main()
