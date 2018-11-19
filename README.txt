Starbuck Beagley & Oscar Chacon (Bitbros)
CSCI-351
Project 3: 351crawler README

To Run: 
	1) Run the runme.sh with arg "dbmake"
		-This fetches the first five pages from the WikiCFP, parses the info,
		makes a database, and stores all the parsed info inside.
		-The program waits 6 seconds inbetween fetching another request to WikiCFP
		so it will take ~30 seconds to completely finish. This was in accordance 
		with WikiCFP's guidelines.
		*NOTE*: If you re-run dbmake, it will override the database's info.
	
	2) Now that the database is populated:
		-Run with arg "all" to print out every entrys' information
		-Run with args "search" followed by the year "YYYY" and month "MM" to query by.
		This will return all events that start in that specified year and month.
		*NOTE*: If you want to look up the events with an "N/A" for its "when",
		the year is "0000" and the month is "00".
		If no events are found, corresponding message will display.
		*NOTE*: If you didn't previously run this with arg "dbmake", then the database
		will be empty.

Writeup:
	We decided to write this in python because there were useful third party libraries
	that made this project a lot easier, namely requests and BeautifulSoup. We gave no
	leeway with incorrectly inputting an argument, which if incorrect, will immedietly
	spit out the usage and exit. Since this program essensially has 3 main functions,
	we separated it accordingly (dbmake, all, search). The main challenge for us was 
	successfully isolating the text from the html responses. BeautifulSoup made handling
	the text trivial, however finding it took a while. The parsing itself turned out 
	well, as it grabbed all the info correctly with very minimal manipulation when printing
	to make it look appealing. For testing, we originally only fetched one page to try
	and parse that info and put that in the database. Once we had all the features 
	working with the one page's worth of information, we simply added the other 4 pages
	and made sure it still worked.