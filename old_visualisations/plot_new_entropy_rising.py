
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



def get_timeseries_with_window_and_ci(measure="H_1", annotate=True, categories = ["nf", "fic", "news", "mag"], ax=None):


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

		ax.plot(smoothed_years, smoothed_results, label=category, linewidth=LINEWIDTH, **this_style)

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


def plot_coha_timeseries(measure="H_1", measure_name="Word Entropy", invert_axis=False, ax=None):


	default_x_size = plt.rcParamsDefault["figure.figsize"][0]
	default_y_size = plt.rcParamsDefault["figure.figsize"][1]

	size_ratio = 1.5

	plt.rcParams["figure.figsize"] = default_x_size*1.5, default_y_size*1.5



	get_timeseries_with_window_and_ci(measure, ax=ax)	

	plt.ylabel(measure_name, fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)


	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))

	if invert_axis:
		ax.invert_yaxis()

	plt.tight_layout()



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

		if y > (y_min+0.5):
			alpha=0.7
		else:
			alpha=0.2

		bb = Bbox.from_bounds(x,y,1,1)  
		bb2 = TransformedBbox(bb,ax.transData)
		bbox_image = BboxImage(bb2,
	                            norm = None,
	                            origin=None,
	                            clip_on=False,
	                            alpha=alpha)

		
		bbox_image.set_data(im_blue)
		
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




def combined_big_figure_just_word_entropy():

	
	import matplotlib.gridspec as gridspec



	#fig = plt.figure(figsize=(8,8), constrained_layout=True)

	# Width is 6.4, keep this width so its consistent 
	fig = plt.figure(figsize=(6.4,6.4), constrained_layout=True)
	
	KWARGS = {"hspace":0.1}
	gs = fig.add_gridspec(6, 6)

	#fig = plt.figure(figsize=(6.4,4.8), constrained_layout=True)

	ax1 = fig.add_subplot(gs[:2,:3])

	plot_entropy_rising_icon_graph(ax=ax1, seed=3, y_min=2, im_count=10)
	plt.title(r"low competition          ", fontproperties=FONT_PROP)


	
	ax2 = fig.add_subplot(gs[:2, 3:])

	plot_entropy_rising_icon_graph(ax=ax2, seed=3, y_min=5, im_count=30)
	plt.title(r"  high competition         ", fontproperties=FONT_PROP)


	ax3 = fig.add_subplot(gs[2:, 0:])

	plot_coha_timeseries(ax=ax3)


	import matplotlib.ticker as ticker

	ax = plt.gca()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))

	plt.ylabel("Word Entropy", fontproperties=FONT_PROP)
	plt.xlabel("Year", fontproperties=FONT_PROP)


	ax3.spines['right'].set_visible(False)
	ax3.spines['top'].set_visible(False)


	plt.tight_layout()

	plt.savefig("images/within_patch_competition_word_entropy.tiff", format="tiff", dpi=300)


	plt.show()


def plot_competitive_conditions_individual():

	pass




if __name__=="__main__":
	combined_big_figure_just_word_entropy()