
from bs4 import BeautifulSoup
import csv
import random
import json
import re
import langdetect
import nltk

import pandas as pd
pd.set_option('display.max_columns', None)

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utilities.text_measures import measure_text_word_measures
from utilities.general_utilities import append_to_csv


def remove_apostrophes_and_whitespace(text):

	text = re.sub(r"\s{1,}", " ", text)
	text = re.sub(r"\s\'|\'", "", text)
	return text

def remove_urls(text):
	# Quite greedy - don't care too much about false positives
	# Any word with a fullstop within it, and at least one character either side
	text = re.sub(r"\S+\.\S+", "", text)
	return text


def remove_hashtags_and_usernames(text):
	
	text = re.sub(r"\@\S+", "", text)
	text = re.sub(r"\#\S+", "", text)
	return text


def clean_reddit_text(text):

	# Remove commas and extra whitespace
	text = remove_apostrophes_and_whitespace(text)

	text = remove_urls(text)
	
	text = remove_hashtags_and_usernames(text)

	tokens = nltk.tokenize.word_tokenize(text)

	words = [word.lower() for word in tokens if word.isalpha()]

	return words


def measure_reddit():

	text_samples = extract_all_posts()
	print(len(text_samples))

	results_filename = 	"../data/results/results_word_measures_reddit.csv"

	sample_id = 0


	for text_sample in text_samples:
		print(text_sample)
		sample_id += 1
		metadata = ["Reddit", sample_id, "homepage", 2023, None, None, "word_measures", 2000]
		
		text_sample_string = " ".join(text_sample)

		word_measures = measure_text_word_measures(text_sample_string, 2000)

		csv_list = metadata + word_measures

		append_to_csv(csv_list, results_filename)
		print(csv_list)
	print(sample_id)


def extract_all_posts():

	n_posts = 100
	all_post_strings = []
	for i in range(n_posts):

		input_filename = "../data/corpora/reddit/reddit_json_{}.json".format(i)
		json_text = open(input_filename, "r").read()
		json_data = json.loads(json_text)

		posts = json_data["data"]["children"]
		for post in posts:
			post_string = post["data"]["title"]
			post_text = post["data"]["selftext"]
			if post_text != "":
				post_string += " " + post_text

			try:
				# Exception if post text is all emojis etc
				if langdetect.detect(post_string) == "en":

					all_post_strings.append(post_string)
			except:
				pass

	combined_text_samples = []

	this_combined_post_words = []

	for text_sample in all_post_strings:

		this_combined_post_words += clean_reddit_text(text_sample)

		if len(this_combined_post_words) > 2000:
			combined_text_samples.append(this_combined_post_words)
			this_combined_post_words = []

	return combined_text_samples




if __name__=="__main__":
	measure_reddit()