
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import nltk
import os
import csv

import pandas as pd
pd.set_option('display.max_columns', 100)



def collate_facebook_minimaxir():

	in_file_directory = "../data/corpora/facebook_minimaxir/raw/"
	out_file_path = "../data/corpora/facebook_minimaxir/collated/facebook_statuses.csv"

	# Get text sample files
	files = os.listdir(in_file_directory)
	csv_files = [f for f in files if ".csv" in f]	
	
	total_file_count = len(csv_files)
	counter = 0

	df_list = []

	for csv_file in csv_files:
		in_file_path = in_file_directory + csv_file
		df = pd.read_csv(in_file_path, header=0)
		df["account"] = csv_file.replace("_facebook_statuses.csv","")
		df_list.append(df)

	df = pd.concat(df_list, axis=0, ignore_index=True)
	df = df.sort_values(by="status_published")
	df.to_csv(out_file_path, header=True)

if __name__=="__main__":
	collate_facebook_minimaxir()
	