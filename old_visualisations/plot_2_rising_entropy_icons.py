


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



def get_entropy_rising_icon_graph(seed=3, y_min=1, im_count=10):

	np.random.seed(seed)

	ax = plt.gca()

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


def plot_rising_entropy():

	size_ratio = 2
	font_size = FONT_PROP.get_size() * size_ratio

	FONT_PROP.set_size(font_size)

	get_entropy_rising_icon_graph(seed=3, y_min=2, im_count=10)
	plt.title(r"low $\lambda$             ", fontproperties=FONT_PROP)


	plt.savefig("images/low_entropy_icons.tiff", format="tiff", dpi=300)

	
	plt.show()
	plt.close()

	get_entropy_rising_icon_graph(seed=3, y_min=5, im_count=30)
	plt.title(r"high $\lambda$             ", fontproperties=FONT_PROP)

	plt.savefig("images/high_entropy_icons.tiff", format="tiff", dpi=300)

	plt.show()
	plt.close()



plot_rising_entropy()