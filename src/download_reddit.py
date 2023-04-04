
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json

import time

from reddit_credentials import USERNAME, PASSWORD, APP_CLIENT_ID, APP_SECRET

def download_reddit():
	"""
	Get the front page, and simply keep scrolling down as far as possible. 
	Infinite scroll gives a lot fo content. 
	Then save the page in the browser, and use the html files in "measure_reddit.py"
	"""
	driver = webdriver.Firefox()
	driver.get("https://www.reddit.com")

	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)


def download_reddit_json():
	"""
	Download the front page, and get the json file. 
	"""

	r = requests.get("https://www.reddit.com/.json?limit=100", headers = {'User-agent': 'polite-scraper'})
	text = r.text

	output_filename = "test_json_1.text"

	with open(output_filename, "w", encoding='utf-8') as f:
		f.write(text)


def parse_json():
	
	input_filename = "test_json_1.text"
	json_text = open(input_filename, "r").read()
	print(json_text)


	json_data = json.loads(json_text)
	print(json_data)

	print(json.dumps(json_data, indent=4, sort_keys=True))

	posts = json_data["data"]["children"]
	for post in posts:
		print("\n\n New POST")
		print(post["data"]["title"])
		print(post["data"]["selftext"])
		print(post["data"]["id"])

	print(json_data["data"]["children"][0]["data"]["title"])


def download_json_from_reddit_without_oauth(after=None):
	"""
	Download the front page, and get the json file. 
	"""

	if after is None:
		request_url = "https://www.reddit.com/.json?limit=100"
	else:
		request_url = "https://www.reddit.com/.json?limit=100&after={}".format(after)

	headers = {"User-Agent": "FriendlyResearch/0.1"}

	r = requests.get(request_url, headers = headers)

	json_text = r.text
	print(r.text)
	json_data = json.loads(json_text)

	return json_data

def get_oauth_token():

	# NOTE: YOU NEED TO REGISTER AN APP WITH REDDIT AS A PERSONAL SCRIPT
	# THE SAVE YOUR REDDIT USERNAME, PASSWORD, APP CLIENT ID AND APP SECRET
	# SAVE THAT IN A FILE CALLED "reddit_auth.py" in the same directory as this script

	import requests
	import requests.auth
	client_auth = requests.auth.HTTPBasicAuth(APP_CLIENT_ID, APP_SECRET)
	post_data = {"grant_type": "password", "username": USERNAME, "password": PASSWORD}
	headers = {"User-Agent": "FriendlyResearch/0.1"}
	response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
	r = response.json()

	access_token = r["access_token"]
	return access_token

def download_json_from_reddit(after=None, access_token=None):
	"""
	Download the front page, and get the json file. 
	"""

	if after is None:
		request_url = "https://oauth.reddit.com/.json?limit=100"
	else:
		request_url = "https://oauth.reddit.com/.json?limit=100&after={}".format(after)

	headers = {"Authorization": "bearer {}".format(access_token), "User-Agent": "FriendlyResearch/0.1"}

	r = requests.get(request_url, headers = headers)

	json_text = r.text
	print(r.text)
	json_data = json.loads(json_text)

	return json_data

def download_reddit():

	output_filename = "../data/corpora/reddit/reddit_json_{}.json"

	access_token = get_oauth_token()

	after = None
	for i in range(1):
		print("working on after ", after)
		json_data = download_json_from_reddit(after, access_token)
		with open(output_filename.format(i), 'w') as f:
			json.dump(json_data, f)
		after = json_data["data"]["after"]
		time.sleep(5)
				

if __name__=="__main__":
	download_reddit()