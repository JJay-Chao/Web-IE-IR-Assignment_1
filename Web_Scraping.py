import requests
import logging
import json

import Dcard

API_ROOT = 'http://dcard.tw/_api'
FORUMS = 'forums'
POSTS = 'posts'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


D = Dcard.Dcard(API_ROOT, FORUMS, POSTS, headers)
Forums = D.All_Forums()
for key in Forums.keys():
    print(key)
forum_name = input('What kind of category would you like to load? ')
D.Dcard_Scraping(Forums, forum_name, pages=80)
