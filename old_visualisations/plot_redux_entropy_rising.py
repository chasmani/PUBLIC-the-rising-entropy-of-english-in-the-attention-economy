

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

text_comp_headers = [
	"comp_ratio"
	]


def get_coha_timeseries_plot(measure="H_1"):

	if measure == "comp_ratio":
		input_filename = "../data/results/results_comp_ratios_coha.csv"
		measures_names = metadata_headers + text_comp_headers
		df = pd.read_csv(input_filename, delimiter=";", names=measures_names)
	else:
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

	categories = ["nf", "fic", "news", "mag"]
	

	smoothing_factor = 0.1

	j = 0

	COHA_CATEGORY_LABELS = {
		"nf":"Non-Fiction",
		"fic":"Fiction",
		"news":"News",
		"mag":"Magazines"
	}

	all_years = pd.Series(np.arange(1800,2010))


	df["date"] = pd.to_datetime(df["year"], format='%Y')

	df = df.sort_values("year")

	for category in categories:
		#plt.subplot(2, 2, j+1)
		j+=1

		this_df = df[(df['category'] == category)]
		
		df_smoothed = this_df.set_index("date").ewm(alpha=0.05).mean()

		print(df_smoothed)

		ax = sns.lineplot(x="date", y=measure, data=df_smoothed, label=COHA_CATEGORY_LABELS[category], linewidth=LINEWIDTH)

		#print(df_smoothed['year'].sort_values())



	ax.lines[0].set_color(COLOR_NF) # nf
	l = ax.lines[0]
	y = l.get_data() 
	ax.annotate("Non-fiction", xy=(1, y[-1][-1]), xycoords=('axes fraction', 'data'), 
		ha='left', va='center', color=l.get_color(), fontproperties=FONT_PROP)

	ax.lines[1].set_color(COLOR_FIC) # fic
	l = ax.lines[1]
	y = l.get_data() 
	ax.annotate("Fiction", xy=(1, y[-1][-1]), xycoords=('axes fraction', 'data'), 
		ha='left', va='center', color=l.get_color(), fontproperties=FONT_PROP)
	
	ax.lines[2].set_color(COLOR_NEWS) # news
	l = ax.lines[2]
	y = l.get_data() 
	ax.annotate("News", xy=(1, y[-1][-1]), xycoords=('axes fraction', 'data'), 
		ha='left', va='center', color=l.get_color(), fontproperties=FONT_PROP)
	
	ax.lines[3].set_color(COLOR_MAG) # mag
	l = ax.lines[3]
	y = l.get_data() 
	ax.annotate("Magazines", xy=(1, y[-1][-1]), xycoords=('axes fraction', 'data'), 
		ha='left', va='center', color=l.get_color(), fontproperties=FONT_PROP)

	#ax.lines[3].set_linestyle("--")
	ax.lines[2].set_linestyle(":")
	ax.lines[1].set_linestyle("-.")

	ax.get_legend().remove()

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	for label in ax.get_xticklabels():
		label.set_fontproperties(FONT_PROP)

	for label in ax.get_yticklabels():
		label.set_fontproperties(FONT_PROP)












def plot_4_panel_timeseries():


	plt.figure(figsize=(10,8))


	plt.subplot(2, 2, 1)

	get_coha_timeseries_plot(measure="H_1")
	ax = plt.gca()
	#ax.legend().set_visible(False)

	plt.ylabel("Unigram Word Entropy")
	plt.xlabel("Year")

	plt.subplot(2, 2, 2)

	get_coha_timeseries_plot(measure="ttr")
	ax = plt.gca()
	ax.legend().set_visible(False)
	plt.ylabel("Type Token Ratio")
	plt.xlabel("Year")

	plt.subplot(2, 2, 3)

	get_coha_timeseries_plot(measure="zipf_clauset")
	ax = plt.gca()
	ax.legend().set_visible(False)

	ax.invert_yaxis()
	plt.ylabel("- 1 x Zipf Exponent")
	plt.xlabel("Year")


	plt.subplot(2, 2, 4)

	get_coha_timeseries_plot(measure="comp_ratio")
	ax = plt.gca()
	ax.legend().set_visible(False)

	plt.ylabel("Compression Ratio")
	plt.xlabel("Year")




	plt.tight_layout()


	plt.savefig("images/timeseries_4_panel.png")

	plt.show()




def plot_coha_timeseries_multiple():


	get_coha_timeseries_plot("ttr")	

	plt.ylabel("Type Token Ratio")
	plt.xlabel("Year")
	ax = plt.gca()
	ax.legend().set_visible(False)

	plt.savefig("images/coha-trend-ttr.png")
	
	plt.show()


	get_coha_timeseries_plot("zipf_clauset")	

	plt.ylabel("-1 * Zipf exponent")
	plt.xlabel("Year")
	ax = plt.gca()
	ax.legend().set_visible(False)

	ax.invert_yaxis()


	plt.savefig("images/coha-trend-zipf.png")
	
	plt.show()


def plot_fiction_scripts_vs_non_scripts(measure="H_1"):


	if measure == "comp_ratio":
		input_filename = "../data/results/results_comp_ratios_coha.csv"
		measures_names = metadata_headers + text_comp_headers
		df = pd.read_csv(input_filename, delimiter=";", names=measures_names)
	else:
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


def timeseries_with_sderrs(measure="H_1", category="fic"):

	plus_minus_years = 3

	if measure == "comp_ratio":
		input_filename = "../data/results/results_comp_ratios_coha.csv"
		measures_names = metadata_headers + text_comp_headers
		df = pd.read_csv(input_filename, delimiter=";", names=measures_names)
	else:
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

	this_df = df[(df['category'] == category)]
		
	data_years = this_df["year"]
	data_values = this_df[measure]

	smoothed_years, smoothed_results, sderrs = get_centered_moving_average(data_years, data_values, plus_minus_years)

	plt.plot(smoothed_years, smoothed_results)

	fill_low = np.array(smoothed_results) - 1.96*np.array(sderrs)
	fill_high = np.array(smoothed_results) + 1.96*np.array(sderrs)

	ax=plt.gca()
	ax.fill_between(smoothed_years, fill_low, fill_high)

	plt.show()


def plot_fiction_non_scripts_window(measure, color):

	plus_minus_years = 5

	if measure == "comp_ratio":
		input_filename = "../data/results/results_comp_ratios_coha.csv"
		measures_names = metadata_headers + text_comp_headers
		df = pd.read_csv(input_filename, delimiter=";", names=measures_names)
	else:
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

	
	this_df = df[(df['script'] == False)]

	data_years = this_df["year"]
	data_values = this_df[measure]

	smoothed_years, smoothed_results, sderrs = get_centered_moving_average(data_years, data_values, plus_minus_years)

	plt.plot(smoothed_years, smoothed_results, linewidth=LINEWIDTH, color=color)

	fill_low = np.array(smoothed_results) - 1.96*np.array(sderrs)
	fill_high = np.array(smoothed_results) + 1.96*np.array(sderrs)

	ax=plt.gca()
	ax.fill_between(smoothed_years, fill_low, fill_high, color=color, alpha=0.15)





def get_timeseries_with_window_and_ci(measure="H_1", annotate=True, categories = ["nf", "fic", "news", "mag"]):


	print(FONT_PROP)

	plus_minus_years = 5

	if measure == "comp_ratio":
		input_filename = "../data/results/results_comp_ratios_coha.csv"
		measures_names = metadata_headers + text_comp_headers
		df = pd.read_csv(input_filename, delimiter=";", names=measures_names)
	else:
		input_filename = "../data/results/results_word_measures_coha_14_june_2021.csv"
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

    
	












def plot_2_panel_timeseries():


	default_x_size = plt.rcParamsDefault["figure.figsize"][0]
	default_y_size = plt.rcParamsDefault["figure.figsize"][1]

	size_ratio = 1.5

	plt.rcParams["figure.figsize"] = default_x_size, default_y_size*1.5

	font_size = FONT_PROP.get_size()

	FONT_PROP.set_size(font_size)

	plt.subplot(2, 1, 1)

	get_timeseries_with_window_and_ci(measure="ttr", annotate=False)
	ax = plt.gca()
	#ax.legend().set_visible(False)

	plt.ylabel("Type Token Ratio", fontproperties=FONT_PROP)
	plt.xticks([])

	plt.subplot(2, 1, 2)

	get_timeseries_with_window_and_ci(measure="zipf_clauset", annotate=False)
	ax = plt.gca()
	ax.legend().set_visible(False)
	plt.ylabel("-1 x Zipf", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)

	ax.invert_yaxis()

	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
	ax.yaxis.set_major_locator(ticker.MultipleLocator(0.01))
	
	plt.tight_layout()


	plt.savefig("images/timeseries_with_ci_2_panel_ttr_and_zipf.tiff", dpi=300, format="tiff")

	plt.show()


def plot_deconstructed_timeseries():


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


	#plt.savefig("images/timeseries_with_ci_{}.tiff".format(measure), dpi=300, format="tiff")

	civil_war = [1861, 1865]
	ww1 = [1914, 1918]
	ww2 = [1939, 1945]
	great_depression = [1929, 1931]

	depression = [1920, 1921]
	long_depression = [1873, 1879]

	neg_growth_years = [
		1929, 1930, 1931, 1932, 1933]

	for year in neg_growth_years:
		plt.axvspan(year, year+1, ymin=0, ymax=0.9, color=COLOR_NEWS, alpha=0.3, lw=0)


	print(FONT_PROP)



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

	#readership_2005_index = 1.22
	#df["Readership Per Person Index"] = df["Readership Per Person"]/readership_2005_index*100
	#ax2.plot(df["Year"], df["Readership Per Person Index"])	

	




	#ax2.plot(df["Year"], df["Readership per person"])
	
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


def correlation_circulation_and_entropy():

	df_circ = pd.read_csv("../data/markets/magazine_readership.csv", delimiter=";", header=0)
	

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


	all_years = pd.Series(np.arange(1800,2010))

	df = df.sort_values("year")

	category = "mag"
	measure = "H_1"
		
	this_df = df[(df['category'] == category)]
			

	data_years = this_df["year"]
	data_values = this_df[measure]
	plus_minus_years = 5

	smoothed_years, smoothed_results, sderrs = get_centered_moving_average(data_years, data_values, plus_minus_years)

	allowed_years = list(np.arange(1920, 2010, 5))

	years = []
	word_entropies = []
	circulations = []
	
	for year_index in range(len(smoothed_years)):
		year = smoothed_years[year_index]
		if year in allowed_years:
			years.append(year)
			word_entropies.append(smoothed_results[year_index])

			sub_circ_df = df_circ[(df_circ['Year']==year)]
			circ = sub_circ_df.iloc[0]['Monthly Circulation']
			circulations.append(circ)
			
	word_entropy_changes = [(j/i-1)*50 for i, j in zip(word_entropies[:-1], word_entropies[1:])]
	circulation_changes = [(j/i-1) for i, j in zip(circulations[:-1], circulations[1:])]


	#plt.scatter(word_entropies, circulations, )


	plt.plot(years[1:], word_entropy_changes)
	plt.plot(years[1:], circulation_changes)
	plt.show()

	plt.scatter(word_entropy_changes, circulation_changes)

	r = scipy.stats.pearsonr(word_entropies, circulations)
	print(r)

	r = scipy.stats.linregress(word_entropy_changes, circulation_changes)
	print(r)


def get_timeseries_combined_plot(measure="H_1"):

	plus_minus_years = 4

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

	all_years = pd.Series(np.arange(1825,2010))

	df = df.sort_values("year")


	categories = ["news", "mag", "nf", "fic"]

	all_results = []

	for category in categories:
		this_df = df[(df['category'] == category)]
		this_results = []

		data_years = this_df["year"]
		data_values = this_df[measure]

		smoothed_years, smoothed_results, sderrs = get_centered_moving_average(data_years, data_values, plus_minus_years)

		for year in all_years:
			if year in smoothed_years:
				year_index = smoothed_years.index(year)
				result = smoothed_results[year_index]
				this_results.append(result)
			else:
				this_results.append(np.nan)

		all_results.append(this_results)


	all_results_array = np.array(all_results)

	print(all_results_array)


	means = np.nanmean(all_results_array, axis=0)

	plt.plot(all_years, means)

	ax = plt.gca()


	for label in ax.get_xticklabels():
		label.set_fontproperties(FONT_PROP)

	for label in ax.get_yticklabels():
		label.set_fontproperties(FONT_PROP)





def timeseries_combined(measure="H_1"):


	get_timeseries_combined_plot(measure)

	

	plt.ylabel("Word Entropy", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)

	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))

	plt.ylabel("Word Entropy", fontproperties=FONT_PROP)


	plt.xlabel("Year", fontproperties=FONT_PROP)

	plt.tight_layout()
	plt.savefig("images/timeseries_combined_{}.tiff".format(measure), dpi=300, format="tiff")

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	plt.show()


	plt.show()


if __name__=="__main__":
	timeseries_combined()
