

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

import scipy.stats

from design_scheme import COLOR_NF, COLOR_FIC, COLOR_NEWS, COLOR_MAG, LINEWIDTH, FONT_PROP

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utilities.timeseries_measures import get_centered_moving_average


metadata_headers = [
		"source",
		"sample_id", 
		"category", 
		"year", 
		"author", 
		"title", 
		"measure_type",
		"length"]

word_measures_headers = [
	"word_count", 
	"avg_word_length", 
	"ttr",
	"zipf_fs",
	"zipf_clauset",
	"H_0",
	"H_1",
	"H_2"]


def plot_fiction_scripts_vs_non_scripts(measure="H_1"):


	input_filename = "../data/results/results_word_measures_coha.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)


	min_year = 1820
	max_year = 2010
	df = df[(~df['year'].isna())]	
	df = df[((df['year'] > min_year) & (df['year'] < max_year))]	

	source = "COHA"
	N = 2000
	df = df[(df['length'] == float(N)) & (df['source'] == source)]


	sources_names = ["source","sample_id", "category_source", "year_source","characters","script"]

	scripts_filename = "../data/results/plays.csv"
	coha_scripts = pd.read_csv(scripts_filename, delimiter=";", names=sources_names)

	print(coha_scripts)


	df = df.merge(coha_scripts, on="sample_id")

	df = df[(df['category'] == "fic")]
	
	script_df = df[["year", "sample_id", "script", "H_1"]]
	script_df.to_csv("../data/results/scripts_and_h1.csv")

	print(df)

	for script in [False, True]:
		this_df = df[(df['script'] == script)]
		df_means = this_df.groupby('year').mean().reset_index()
		df_smoothed = df_means.ewm(alpha=0.1, ignore_na=True, min_periods=10).mean()
		df_smoothed = df_means.ewm(span=10, ignore_na=True, min_periods=10).mean()
		
		ax = sns.lineplot(x="year", y=measure, data=df_smoothed, label=script, linewidth=LINEWIDTH)

	
	df_means = df.groupby('year').mean().reset_index()
	df_smoothed = df_means.ewm(alpha=0.1).mean()
	ax = sns.lineplot(x="year", y=measure, data=df_smoothed, label="both", linewidth=LINEWIDTH)


	plt.show()


def is_it_a_script(text):
	print(text)
	if "script" in text.lower() or "magazine" in text.lower():
		return True
	else:
		return False


def get_timeseries_with_window_and_ci(measure="H_1", annotate=True, categories = ["nf", "fic", "news", "mag"]):


	plus_minus_years = 5

	input_filename = "../data/results/results_word_measures_coha.csv"
	measures_names = metadata_headers + word_measures_headers
	df = pd.read_csv(input_filename, delimiter=";", names=measures_names)


	min_year = 1810
	max_year = 2010
	df = df[(~df['year'].isna())]	
	df = df[((df['year'] > min_year) & (df['year'] < max_year))]	


	source = "COHA"
	N = 2000
	df = df[(df['length'] == float(N)) & (df['source'] == source)]


	smoothing_factor = 0.5

	j = 0

	COHA_CATEGORY_LABELS = {
		"nf":"Non-Fiction",
		"fic":"Fiction",
		"news":"News",
		"mag":"Magazines"
	}

	COHA_CATEGORY_STYLES = {
		"nf":{"color":COLOR_NF},
		"fic":{"color":COLOR_FIC, "linestyle":":"},
		"news":{"color":COLOR_NEWS},
		"mag":{"color":COLOR_MAG, "linestyle":"-."}
	}

	all_years = pd.Series(np.arange(1800,2010))

	df["date"] = pd.to_datetime(df["year"], format='%Y')

	df = df.sort_values("year")

	for category in categories:

		this_style = COHA_CATEGORY_STYLES[category]

		this_df = df[(df['category'] == category)]
			

		data_years = this_df["year"]
		data_values = this_df[measure]

		smoothed_years, smoothed_results, sderrs = get_centered_moving_average(data_years, data_values, plus_minus_years)

		plt.plot(smoothed_years, smoothed_results, label=category, linewidth=LINEWIDTH, **this_style)

		fill_low = np.array(smoothed_results) - 1.96*np.array(sderrs)
		fill_high = np.array(smoothed_results) + 1.96*np.array(sderrs)

		ax=plt.gca()
		ax.fill_between(smoothed_years, fill_low, fill_high, **this_style, alpha=0.1)


	for j in range(len(ax.lines)):
		l = ax.lines[j]
		y = l.get_data()	
		if annotate:
			annotation = COHA_CATEGORY_LABELS[categories[j]]
			ax.annotate(annotation, xy=(1, y[-1][-1]), xycoords=('axes fraction', 'data'), 
			ha='left', va='center', color=l.get_color(), fontproperties=FONT_PROP)

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	for label in ax.get_xticklabels():
		label.set_fontproperties(FONT_PROP)

	for label in ax.get_yticklabels():
		label.set_fontproperties(FONT_PROP)


def plot_timeseries_with_magazine_circulation():


	default_x_size = plt.rcParamsDefault["figure.figsize"][0]
	default_y_size = plt.rcParamsDefault["figure.figsize"][1]

	size_ratio = 1.5

	plt.rcParams["figure.figsize"] = default_x_size*1.5, default_y_size*1.5

	font_size = FONT_PROP.get_size()

	FONT_PROP.set_size(20)

	measure = "H_1"

	get_timeseries_with_window_and_ci(measure, annotate=False, categories=["mag"])	

	plt.ylabel("Word Entropy", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)


	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))

	# Depression
	neg_growth_years = [
		1929, 1930, 1931, 1932, 1933]

	for year in neg_growth_years:
		plt.axvspan(year, year+1, ymin=0, ymax=0.9, color=COLOR_NEWS, alpha=0.3, lw=0)



	ax.annotate("The Great Depression", xy=(1933, 0.92), xycoords=('data', 'axes fraction'), 
		ha='right', va='center', color=COLOR_NEWS, fontproperties=FONT_PROP)

	
	# Ten cent magazine
	plt.axvspan(1893, 1894, ymin=0, ymax=0.7, color=COLOR_NEWS, alpha=0.3, lw=0)
	ax.annotate("10 cent magazines", xy=(1894, 0.72), xycoords=('data', 'axes fraction'), 
		ha='right', va='center', color=COLOR_NEWS, fontproperties=FONT_PROP)


	# Audit Bureau of Circulations
	plt.axvspan(1914, 1915, ymin=0, ymax=0.8, color=COLOR_NEWS, alpha=0.3, lw=0)
	ax.annotate("Audit Bureau of Circulations", xy=(1915, 0.82), xycoords=('data', 'axes fraction'), 
		ha='right', va='center', color=COLOR_NEWS, fontproperties=FONT_PROP)


	df = pd.read_csv("../data/markets/magazine_readership.csv", delimiter=";", header=0)
	
	ax1 = plt.gca()
	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis


	monthly_circ_2005_index = 362
	df["Monthly Circulation Index"] = df["Monthly Circulation"]/monthly_circ_2005_index*100
	ax2.plot(df["Year"], df["Monthly Circulation Index"], label="US Magazine Circulation")

	ax2.set_ylim([10, 300])
	ax2.set_yscale('log')

	ax2.set_ylabel('US Monthly Circulation (Millions)', fontproperties=FONT_PROP)

	ax1.spines['top'].set_visible(False)
	ax2.spines['top'].set_visible(False)

	for label in ax2.get_yticklabels():
		label.set_fontproperties(FONT_PROP)

	plt.tight_layout()

	plt.savefig("images/magazine_history.png", dpi=300)

	plt.show()


def plot_coha_timeseries(measure="H_1", measure_name="Word Entropy", invert_axis=False):


	default_x_size = plt.rcParamsDefault["figure.figsize"][0]
	default_y_size = plt.rcParamsDefault["figure.figsize"][1]

	size_ratio = 1.5

	plt.rcParams["figure.figsize"] = default_x_size*1.5, default_y_size*1.5


	FONT_PROP.set_size(20)

	get_timeseries_with_window_and_ci(measure)	

	plt.ylabel(measure_name, fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)


	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))

	if invert_axis:
		ax.invert_yaxis()

	plt.tight_layout()
	plt.savefig("images/timeseries_with_ci_{}.tiff".format(measure), format="tiff", dpi=300)

	plt.show()


def plot_timeseries_figures_for_all_measures():

	plot_coha_timeseries(measure="H_1", measure_name="Word Entropy", invert_axis=False)
	plot_coha_timeseries(measure="ttr", measure_name="Type Token Ratio", invert_axis=False)
	plot_coha_timeseries(measure="zipf_clauset", measure_name="-1 x Zipf Exponent", invert_axis=True)


if __name__=="__main__":
	plot_timeseries_with_magazine_circulation()