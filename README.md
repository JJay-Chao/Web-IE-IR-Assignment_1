# Web-IE-IR-Assignment_1
QA System based on Elasticsearch &amp; Dcard

File introduction:

1. Dcard.py: Web crawler python code, crawling documents from Card API.

2. Web_Scraping.py: This program imports Dcard.py to implement the web crawling, and lists out all available topics on Dcard. Although you can crawl all kinds of documents from Dcard by this program, assignment 1 only allows user to crawl 健身 topic.
		    When run this program, follow the action mentioned here -> What kind of category would you like to load? 健身

3. Search_Engine.py: Elasticsearch program.

4. User_Interface.py: QA system user interface.



Directory introduction:

1. Database: Includes 健身.json

2. Elasticsearch: Directory and files of Elasticsearch.



******************************************Most Important Part*********************************************

How to run the QA system?

Answer: 1. Put those directories you have download at the same path with your python.
	2. Open your command line.
	3. Type in: python User_Interface.py
	

******************************************Most Important Part*********************************************



How to operate the User Interface?

1. Press the "Load Data!" button to load 健身.json into Elasticsearch database.
2. Type in your query in the message box in Chinese. Ex. 如何變壯
3. Press the "Go get it!" button to get to another page with documents and comments displayed.
4. Press Back to Home Page button to get back to home page when you are done or would like to ask other questions.
5. If you want to remove the data from Elasticsearch, please press "Delete Data!", and the search is over.
