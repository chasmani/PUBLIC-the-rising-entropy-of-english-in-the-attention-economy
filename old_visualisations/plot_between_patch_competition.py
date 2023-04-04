
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox

from design_scheme import COLOR_NF, COLOR_FIC, COLOR_NEWS, COLOR_MAG, COLOR_SOCIAL, LINEWIDTH, FONT_PROP, BOLD_FONT_PROP, COLOR_3


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


def combined_snapshots(measure="H_1", ax=None):


	measure_type = "word_measures"
	headers = metadata_headers + word_measures_headers

	
	input_filename = "../data/results/results_{}_coca.csv".format(measure_type)
	df_coca = pd.read_csv(input_filename, delimiter=";", names=headers)

	input_filename = "../data/results/results_{}_coha.csv".format(measure_type)
	df_coha = pd.read_csv(input_filename, delimiter=";", names=headers)

	input_filename = "../data/results/results_{}_bnc.csv".format(measure_type)
	df_bnc = pd.read_csv(input_filename, delimiter=";", names=headers)

	input_filename = "../data/results/results_{}_twitter.csv".format(measure_type)
	df_twitter = pd.read_csv(input_filename, delimiter=";", names=headers)

	input_filename = "../data/results/results_{}_facebook.csv".format(measure_type)
	df_facebook = pd.read_csv(input_filename, delimiter=";", names=headers)

	# Recent COHA
	df_coha = df_coha[(df_coha['year'] > 1999)]
	# Rmeove an outlier in COHA
	df_coha = df_coha[(df_coha['H_1'] > 6)]
	



	# Combine all into one df
	df = pd.concat([df_coca, df_coha, df_bnc, df_twitter, df_facebook])

	df.replace(to_replace="Twitter Kaggle Sentiment", value="Twitter", inplace=True)
	df.replace(to_replace="random_concat", value="", inplace=True)


	df["source category"] = df["source"] + " " + df["category"]

	source_cats_order = [
		"COHA nf",
		"COHA fic",
		"COHA news",
		"COHA mag", 
		"",
		"COCA acad",
		"COCA fic",
		"COCA news",		
		"COCA mag",
		"",
		"BNC ACPROSE",
		"BNC FICTION",
		"BNC NEWS",		
		"",
		"Twitter ",
		"Facebook ",
	]

	N = 2000

	df = df[(df['length'] == float(N))]	
	
	ax.yaxis.grid(True) # Show the vertical gridlines

	ax = sns.boxplot(data=df, y=measure, x="source category", orient="v", ax=ax, order=source_cats_order, linewidth=1)

	#sns.pointplot(data=df, x=measure, y="source category", join=False, ci="sd")

	ax.artists[source_cats_order.index("BNC FICTION")-2].set_facecolor(COLOR_FIC)
	ax.artists[source_cats_order.index("COCA fic")-1].set_facecolor(COLOR_FIC)
	ax.artists[source_cats_order.index("COHA fic")].set_facecolor(COLOR_FIC)

	ax.artists[source_cats_order.index("BNC ACPROSE")-2].set_facecolor(COLOR_NF)
	ax.artists[source_cats_order.index("COCA acad")-1].set_facecolor(COLOR_NF)
	ax.artists[source_cats_order.index("COHA nf")].set_facecolor(COLOR_NF)

	ax.artists[source_cats_order.index("BNC NEWS")-2].set_facecolor(COLOR_NEWS)
	ax.artists[source_cats_order.index("COCA news")-1].set_facecolor(COLOR_NEWS)
	ax.artists[source_cats_order.index("COHA news")].set_facecolor(COLOR_NEWS)


	ax.artists[source_cats_order.index("COCA mag")-1].set_facecolor(COLOR_MAG)
	ax.artists[source_cats_order.index("COHA mag")].set_facecolor(COLOR_MAG)


	try:
		ax.artists[source_cats_order.index("Twitter ")-3].set_facecolor(COLOR_SOCIAL)
		ax.artists[source_cats_order.index("Facebook ")-3].set_facecolor(COLOR_SOCIAL)
	except:
		pass

	
	category_ticks = ["Non-Fic", "Fiction", "News", "Mag", "", 
		"Non-Fic", "Fiction", "News", "Mag", "",
		"Non-Fic", "Fiction", "News", "", 
		"Twitter", "Facebook"]
	

	plt.xticks(range(len(category_ticks)), category_ticks, rotation=45, ha='right')

	for label in ax.get_xticklabels():
		label.set_fontproperties(FONT_PROP)

	for label in ax.get_yticklabels():
		label.set_fontproperties(FONT_PROP)


	plt.ylabel("Word Entropy", fontproperties=FONT_PROP)



def plot_patch_choice_low_prev(ax, seed=11, im_count=10):

	np.random.seed(seed)

	icon_file_book = "resources/005-open-book-blue.png"
	icon_file_news = "resources/001-newspaper-folded-blue.png"
	icon_file_twitter = "resources/003-twitter.png"

	im_book = plt.imread(icon_file_book)
	im_news = plt.imread(icon_file_news)	
	im_twitter = plt.imread(icon_file_twitter)

	x,y = 0,0

	xs = np.random.random(size=im_count) * 6 + 1
	ys = np.random.random(size=im_count) * 6 + 1

	lamb=0.1

	R_inv_min = 3

	for i in range(im_count):
		x = xs[i]
		y = ys[i]

		r_inv = 1/(lamb*x) + 1/y
		if r_inv < R_inv_min+0.1:
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


		if x > 5:
			bbox_image.set_data(im_book)
		else:
			bbox_image.set_data(im_news)
		ax.add_artist(bbox_image)

	# Twitter
	for i in range(5):
		x = np.random.random() * 2 + 0.5
		y = np.random.random() * 4 + 6

		r_inv = 1/(lamb*x) + 1/y
		if r_inv < R_inv_min+0.1:
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

		bbox_image.set_data(im_twitter)
		ax.add_artist(bbox_image)
	
	
	xx = np.linspace(3.37,10, 100)
	yy = [1/(R_inv_min - 1/(lamb*x)) for x in xx]
	yy_2 = [10]*100
	plt.fill_between(xx, yy, yy_2, color=COLOR_3, alpha=0.1)


	plt.plot(xx,yy, color=COLOR_3, linewidth=LINEWIDTH*2, linestyle="dashed")


	plt.yticks([])
	plt.xticks([])
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)


	plt.ylabel(r"$\bar{r}_p$", fontproperties=FONT_PROP)
	plt.xlabel(r"$\bar{u}_p$", fontproperties=FONT_PROP)


	plt.xlim(0,10)
	plt.ylim(0,10)

	plt.title(r"low competition", fontproperties=FONT_PROP)


def plot_patch_choice_high_prev(ax, seed=3, im_count=20, lamb=2):

	np.random.seed(seed)

	icon_file_book = "resources/005-open-book-blue.png"
	icon_file_news = "resources/001-newspaper-folded-blue.png"
	icon_file_twitter = "resources/003-twitter.png"


	im_book = plt.imread(icon_file_book)
	im_news = plt.imread(icon_file_news)
	im_twitter = plt.imread(icon_file_twitter)	

	x,y = 0,0

	xs = np.random.random(size=im_count) * 8
	ys = np.random.random(size=im_count) * 6


	R_inv_min = 0.5


	for i in range(im_count):
		x = xs[i]
		y = ys[i]

		if x > 5:
			y -= 1


		r_inv = 1/(lamb*x) + 1/y
		if r_inv < R_inv_min+0.1:
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

		if x > 5:
			bbox_image.set_data(im_book)
		else:
			bbox_image.set_data(im_news)
		ax.add_artist(bbox_image)

	# Twitter
	for i in range(5):
		x = np.random.random() * 2 + 0.5
		y = np.random.random() * 4 + 6

		r_inv = 1/(lamb*x) + 1/y
		if r_inv < R_inv_min+0.1:
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

		bbox_image.set_data(im_twitter)
		ax.add_artist(bbox_image)
	

	xx = np.linspace(1,10, 100)
	yy = [1/(R_inv_min - 1/(lamb*x)) for x in xx]
	yy_2 = [10]*100
	plt.fill_between(xx, yy, yy_2, color=COLOR_3, alpha=0.1)


	plt.plot(xx,yy, color=COLOR_3, linewidth=LINEWIDTH*2, linestyle="dashed")



	plt.yticks([])
	plt.xticks([])
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)


	plt.ylabel(r"$\bar{r}_p$", fontproperties=FONT_PROP)
	plt.xlabel(r"$\bar{u}_p$", fontproperties=FONT_PROP)


	plt.xlim(0,10)
	plt.ylim(0,10)

	plt.title(r"high competition", fontproperties=FONT_PROP)




def combined_big_figure():

	import matplotlib.gridspec as gridspec

	fig = plt.figure(figsize=(6.4,4.8), constrained_layout=True)
	
	
	gs = fig.add_gridspec(4, 6)

	#fig = plt.figure(figsize=(6.4,4.8), constrained_layout=True)

	ax1 = fig.add_subplot(gs[:2, :1])

	plot_patch_choice_low_prev(ax=ax1)

	ax2 = fig.add_subplot(gs[:2, 5:])

	plot_patch_choice_high_prev(ax=ax2)

	ax3 = fig.add_subplot(gs[2:, :])

	combined_snapshots(ax=ax3)


	ax3.set_xlabel(r"                                              BNC                            COCA                           COHA                             ", fontproperties=BOLD_FONT_PROP)

	ax3.spines['right'].set_visible(False)
	ax3.spines['top'].set_visible(False)

	ax3.invert_xaxis()

	#plt.tight_layout()

	plt.savefig("images/between_patch_competition.tiff", format="tiff", dpi=300)


	plt.show()



if __name__=="__main__":
	combined_big_figure()