
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox

import scipy.stats

from design_scheme import COLOR_NF, COLOR_FIC, COLOR_NEWS, COLOR_MAG, LINEWIDTH, FONT_PROP, COLOR_3

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
	"zipf_cdf",
	"zipf_clauset", 
	"H_0",
	"H_1",
	"H_2"]


def get_timeseries_combined_plot(ax, measure="H_1"):

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

	sns.lineplot(all_years, means, linewidth=LINEWIDTH, color=COLOR_3, ax=ax)

	for label in ax.get_xticklabels():
		label.set_fontproperties(FONT_PROP)

	for label in ax.get_yticklabels():
		label.set_fontproperties(FONT_PROP)


def plot_entropy_rising_icon_graph(ax, seed=3, y_min=1, im_count=10):

	np.random.seed(seed)

	icon_file_blue = "resources/001-newspaper-folded-blue.png"
	icon_file_grey = "resources/001-newspaper-folded-grey.png"

	im_blue = plt.imread(icon_file_blue)
	im_grey = plt.imread(icon_file_grey)	

	x,y = 0,0

	xs = np.random.random(size=im_count) * 7
	ys = np.random.random(size=im_count) * 6 + 2

	for i in range(im_count):
		x = xs[i]
		y = ys[i]

		bb = Bbox.from_bounds(x,y,1,1)  
		bb2 = TransformedBbox(bb,ax.transData)
		bbox_image = BboxImage(bb2,
	                            norm = None,
	                            origin=None,
	                            clip_on=False)

		if y > y_min:
			bbox_image.set_data(im_blue)
		else:
			bbox_image.set_data(im_grey)
		ax.add_artist(bbox_image)
	

	plt.axhline(y_min+1, xmax=0.8, color=COLOR_3, linestyle="dashed", linewidth=LINEWIDTH*2)

	xx = np.linspace(0, 8, 100)
	yy = [y_min+1]*100
	yy_2 = [10]*100

	plt.fill_between(xx, yy, yy_2, color=COLOR_3, alpha=0.1)

	plt.yticks([])
	plt.xticks([])

	plt.xlim(0,10)

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)

	ax.spines['left'].set_bounds(2, 10)

	plt.ylabel(r"$r_i$", fontproperties=FONT_PROP)

	plt.xlim(0,10)
	plt.ylim(0,10)


def combined_big_figure():

	import matplotlib.gridspec as gridspec

	fig = plt.figure(constrained_layout=True)
	
	KWARGS = {"hspace":0.1}
	gs = fig.add_gridspec(4, 6)

	ax1 = fig.add_subplot(gs[:2,:3])

	plot_entropy_rising_icon_graph(ax=ax1, seed=3, y_min=2, im_count=10)
	plt.title(r"low $\lambda$             ", fontproperties=FONT_PROP)


	
	ax2 = fig.add_subplot(gs[:2, 3:])

	plot_entropy_rising_icon_graph(ax=ax2, seed=3, y_min=5, im_count=30)
	plt.title(r"high $\lambda$             ", fontproperties=FONT_PROP)


	ax3 = fig.add_subplot(gs[2:, 0:-2])

	get_timeseries_combined_plot(ax=ax3)

	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))

	plt.ylabel("Word Entropy", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)


	ax3.spines['right'].set_visible(False)
	ax3.spines['top'].set_visible(False)



	ax4 = fig.add_subplot(gs[2, -2:])

	get_timeseries_combined_plot(measure="ttr", ax=ax4)
	
	ax4.yaxis.set_major_locator(ticker.MultipleLocator(0.01))
	plt.ylabel("TTR", fontproperties=FONT_PROP)
	plt.xticks([])

	ax4.spines['right'].set_visible(False)
	ax4.spines['top'].set_visible(False)

	ax5 = fig.add_subplot(gs[3, -2:])

	get_timeseries_combined_plot(measure="zipf_clauset", ax=ax5)
	
	ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.01))
	plt.ylabel("-1 x Zipf", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)

	ax5.invert_yaxis()

	ax5.spines['right'].set_visible(False)
	ax5.spines['top'].set_visible(False)

	ax5.xaxis.set_major_locator(ticker.MultipleLocator(100))
	ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.005))

	#plt.tight_layout()

	plt.savefig("images/within_patch_competition.tiff", format="tiff", dpi=300)


	plt.show()


def all_3_measures_combined_timeseries():

	
	import matplotlib.gridspec as gridspec

	fig = plt.figure(constrained_layout=True)
	



	KWARGS = {"hspace":0.1}
	gs = fig.add_gridspec(4, 8)

	ax3 = fig.add_subplot(gs[:, 0:-2])

	get_timeseries_combined_plot_with_conf_intervals(ax=ax3)

	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))

	plt.ylabel("Word Entropy", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)


	ax3.spines['right'].set_visible(False)
	ax3.spines['top'].set_visible(False)


	ax4 = fig.add_subplot(gs[2, -2:])

	get_timeseries_combined_plot_with_conf_intervals(measure="ttr", ax=ax4)
	
	ax4.yaxis.set_major_locator(ticker.MultipleLocator(0.01))
	plt.ylabel("TTR", fontproperties=FONT_PROP)
	plt.xticks([])

	ax4.spines['right'].set_visible(False)
	ax4.spines['top'].set_visible(False)

	ax5 = fig.add_subplot(gs[3, -2:])

	get_timeseries_combined_plot_with_conf_intervals(measure="zipf_clauset", ax=ax5)
	
	ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.01))
	plt.ylabel("-1 x Zipf", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)

	ax5.invert_yaxis()

	ax5.spines['right'].set_visible(False)
	ax5.spines['top'].set_visible(False)

	ax5.xaxis.set_major_locator(ticker.MultipleLocator(100))
	ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.005))

	#plt.tight_layout()

	plt.savefig("images/within_patch_competition.tiff", format="tiff", dpi=300)


	plt.show()


def get_timeseries_combined_plot_with_conf_intervals(ax, measure="H_1"):

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

	all_years = pd.Series(np.arange(1825,2010))

	df = df.sort_values("year")


	categories = ["news", "mag", "nf", "fic"]

	all_results = []
	all_sderrs = []

	for category in categories:
		this_df = df[(df['category'] == category)]
		this_results = []
		this_sderrs = []

		data_years = this_df["year"]
		data_values = this_df[measure]

		smoothed_years, smoothed_results, sderrs = get_centered_moving_average(data_years, data_values, plus_minus_years)

		for year in all_years:
			if year in smoothed_years:
				year_index = smoothed_years.index(year)
				result = smoothed_results[year_index]
				this_results.append(result)
				sderr = sderrs[year_index]
				this_sderrs.append(sderr)
			else:
				this_results.append(np.nan)
				this_sderrs.append(np.nan)


		all_results.append(this_results)
		all_sderrs.append(this_sderrs)


	means = []
	mean_sderrs = []

	# get means and sderrs
	for year in all_years:
		year_sum = 0
		year_count = 0
		var_sum = 0
		year_index = list(all_years).index(year)
		for cat_index in range(4):
			cat_result = all_results[cat_index][year_index]
			if np.isnan(cat_result):
				pass
			else:
				year_sum += cat_result
				year_count += 1
				var_sum += all_sderrs[cat_index][year_index]**2
		year_mean = year_sum/year_count
		year_sderr = (1/year_count) * np.sqrt(var_sum)
		means.append(year_mean)
		mean_sderrs.append(year_sderr)



	print(means, mean_sderrs)



	
	plt.plot(all_years, means, label=category, linewidth=LINEWIDTH)




	fill_low = np.array(means) - 1.96*np.array(mean_sderrs)
	fill_high = np.array(means) + 1.96*np.array(mean_sderrs)

	ax=plt.gca()
	ax.fill_between(all_years, fill_low, fill_high, alpha=0.1)



	for label in ax.get_xticklabels():
		label.set_fontproperties(FONT_PROP)

	for label in ax.get_yticklabels():
		label.set_fontproperties(FONT_PROP)




def plot_2_panel_timeseries():


	import matplotlib.ticker as ticker

	default_x_size = plt.rcParamsDefault["figure.figsize"][0]
	default_y_size = plt.rcParamsDefault["figure.figsize"][1]

	size_ratio = 1.5

	plt.rcParams["figure.figsize"] = default_x_size, default_y_size*1.5

	font_size = FONT_PROP.get_size() * size_ratio * 1.2

	FONT_PROP.set_size(font_size)

	plt.subplot(2, 1, 1)

	ax = plt.gca()
	get_timeseries_combined_plot_with_conf_intervals(ax=ax, measure="ttr")
	
	ax.yaxis.set_major_locator(ticker.MultipleLocator(0.01))
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
		

	#ax.legend().set_visible(False)

	plt.ylabel("Type Token Ratio", fontproperties=FONT_PROP)
	plt.xticks([])

	plt.subplot(2, 1, 2)

	ax = plt.gca()
	get_timeseries_combined_plot_with_conf_intervals(ax=ax, measure="zipf_clauset")
	ax.legend().set_visible(False)
	plt.ylabel("-1 x Zipf", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)

	ax.invert_yaxis()

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
	ax.yaxis.set_major_locator(ticker.MultipleLocator(0.005))
	
	plt.tight_layout()


	plt.savefig("images/timeseries_with_ci_2_panel_ttr_and_zipf.tiff", dpi=300, format="tiff")

	plt.show()

def plot_1_panel_timeseries_combined(measure="H_1"):

	font_size = FONT_PROP.get_size() * 1.2

	FONT_PROP.set_size(font_size)


	get_timeseries_combined_plot_with_conf_intervals(measure)
	

	plt.ylabel("Word Entropy", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)

	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	

	plt.ylabel("Word Entropy", fontproperties=FONT_PROP)


	plt.xlabel("Year", fontproperties=FONT_PROP)

	plt.tight_layout()
	plt.savefig("images/timeseries_combined_{}.tiff".format(measure), dpi=300, format="tiff")

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	plt.show()



if __name__=="__main__":

	plot_1_panel_timeseries_combined()
	#plot_2_panel_timeseries()