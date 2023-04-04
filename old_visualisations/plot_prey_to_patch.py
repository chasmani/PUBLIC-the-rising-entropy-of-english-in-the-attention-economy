


import matplotlib.pyplot as plt
import numpy as np

from design_scheme import LINEWIDTH, COLOR_MAG, COLOR_FIC, COLOR_4, COLOR_BLACK, FONT_PROP

LINEWIDTH=LINEWIDTH*2

def plot_discrete_info_curve(prevalence=1, handling_time=1, q=1, n=3, color="red", size_ratio=1):

	current_time = 0
	current_u = 0

	r = q/handling_time

	for i in range(n):

		encounter_time = current_time + 1/prevalence
		finish_time = encounter_time + handling_time

		tt_wait = np.linspace(current_time, encounter_time, 100)
		uu_wait = [current_u] * 100

		plt.plot(tt_wait, uu_wait, color=color, linewidth=LINEWIDTH*size_ratio)

		tt_handle = np.linspace(encounter_time, finish_time, 100)
		uu_handle = current_u + (tt_handle - encounter_time)*r

		plt.plot(tt_handle, uu_handle, color=color, linewidth=LINEWIDTH*size_ratio)

		current_time = finish_time
		current_u += q

	encounter_time = current_time + 1/prevalence
	finish_time = encounter_time + handling_time

	tt_wait = np.linspace(current_time, encounter_time, 100)
	uu_wait = [current_u] * 100	

	plt.plot(tt_wait, uu_wait, color=color, linewidth=LINEWIDTH, label="cumulative utility")


def plot_expected_patch_utility(prevalence=1, handling_time=1, q=1, n=3, color="red", size_ratio=1):

	R = q/(1/prevalence + handling_time)

	tt_max = (1/prevalence + handling_time)*n

	tt = np.linspace(0, tt_max, 100)
	uu = R*tt
	plt.plot(tt, uu, color=color, linestyle="dashed", linewidth=LINEWIDTH*size_ratio, label="patch utility rate")


def plot_a_book_and_twitter():

	plot_one_big_fig(title="A book", prevalence=0.8, handling_time=2, q=2, n=1, color=COLOR_FIC)
	plot_one_big_fig(title="Twitter", prevalence=3, handling_time=0.3, q=0.5, n=4, color=COLOR_MAG)


def plot_entropy_rising(ax):


	AXES_COLOR = "lightgray"

	plt.xticks([])
	plt.yticks([])

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)


	plot_discrete_info_curve(prevalence=1, handling_time=2, q=1, n=1, color="silver")
	plot_expected_patch_utility(prevalence=1, handling_time=2, q=1, n=1, color="silver")

	plot_discrete_info_curve(prevalence=1, handling_time=1, q=1, n=1, color=COLOR_FIC)
	plot_expected_patch_utility(prevalence=1, handling_time=1, q=1, n=1, color=COLOR_FIC)

	plt.arrow(3, 1.1, -0.9, 0,  head_width=0.05, linewidth=LINEWIDTH)


	plt.xlim(left=0)
	plt.ylim(bottom=0)


def plot_media_category_differences(ax):


	AXES_COLOR = "lightgray"


	plt.xticks([])
	plt.yticks([])

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)



	plot_discrete_info_curve(prevalence=1, handling_time=5, q=3, n=1, color=COLOR_FIC)
	#plot_expected_patch_utility(prevalence=1, handling_time=5, q=3, n=1, color=COLOR_FIC)

	plot_discrete_info_curve(prevalence=1, handling_time=1, q=1, n=3, color=COLOR_MAG)

	plot_expected_patch_utility(prevalence=1, handling_time=1, q=1, n=3, color="silver")


	plt.xlim(left=0, right=8)
	plt.ylim(bottom=0)


def plot_rise_short_form_media(ax, prevalence=2, xlim_right=7):


	AXES_COLOR = "lightgray"
	plt.xticks([])
	plt.yticks([])

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	plot_discrete_info_curve(prevalence=prevalence, handling_time=5, q=3, n=1, color=COLOR_FIC)
	plot_expected_patch_utility(prevalence=prevalence, handling_time=5, q=3, n=1, color=COLOR_FIC)

	plot_discrete_info_curve(prevalence=prevalence, handling_time=0.7, q=1, n=3, color=COLOR_MAG)
	plot_expected_patch_utility(prevalence=prevalence, handling_time=0.7, q=1, n=3, color=COLOR_MAG)

	plt.xlim(left=0, right=xlim_right)
	plt.ylim(bottom=0)



	#plot_one_big_fig(title="A book", prevalence=0.8, handling_time=2, q=2, n=1, color=COLOR_FIC)
	#plot_one_big_fig(title="Twitter", prevalence=3, handling_time=0.3, q=0.5, n=4, color=COLOR_MAG)


def get_geometry_plot(ax):

	plt.ylabel("Utility", fontproperties=FONT_PROP)

	xtick_marks = ['']*30
	xtick_marks[10] = r"$\frac{1}{\lambda_p}$"
	xtick_marks[20] = r"$\frac{1}{\lambda_p} + \bar{t}_p$"
	#xtick_marks[20] = r"$t_h"


	ytick_marks = ['']*22
	ytick_marks[10] = r"$\bar{u}_p$"

	plt.xticks(np.arange(0,3,0.1), xtick_marks)
	plt.yticks(np.arange(0,2.2,0.1), ytick_marks)
	
	ax.tick_params(axis=u'both', which=u'both',length=0)

	plt.ylim(0,2.2)
	plt.xlim(0,4.5)
	plt.xlabel("Time", fontproperties=FONT_PROP)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	prevalence=1
	handling_time=1 
	q=1
	n=2
	color=COLOR_FIC

	plt.axvline(x=2, ymax=1/2.2, color="lightgray", linewidth=LINEWIDTH)
	plt.axhline(y=1, xmax=2/4.5, color="lightgray", linewidth=LINEWIDTH)

	plot_discrete_info_curve(prevalence=prevalence, handling_time=handling_time, q=q, n=n, color=color, size_ratio=1)
	plot_expected_patch_utility(prevalence=prevalence, handling_time=handling_time, q=q, n=n, color=color, size_ratio=1)

	for label in ax.get_xticklabels():
		label.set_fontproperties(FONT_PROP)

	for label in ax.get_yticklabels():
		label.set_fontproperties(FONT_PROP)


	plt.annotate(r"$\bar{r}_p$", (1.6,0.4), fontproperties=FONT_PROP)
	plt.annotate(r"$R_{patch}$", (0.9,0.7), fontproperties=FONT_PROP)


def plot_geometry():

	default_x_size = plt.rcParamsDefault["figure.figsize"][0]
	default_y_size = plt.rcParamsDefault["figure.figsize"][1]

	size_ratio = 1.5

	plt.rcParams["figure.figsize"] = default_x_size*1.5, default_y_size*1.5

	font_size = FONT_PROP.get_size()

	FONT_PROP.set_size(font_size*1.5)


	# 1a - MVT basic
	ax = plt.subplot(1, 1, 1)
	get_geometry_plot(ax)

	plt.tight_layout()

	plt.savefig("images/patch_choice_geometry.tiff", dpi=300, format="tiff")


def plot_viability_short_form():

		# Low prevalance
	plot_rise_short_form_media(prevalence=0.4, xlim_right=8)
	# High prevalence
	plot_rise_short_form_media(prevalence=2, xlim_right=8)


def plot_patch_geometry():

	fig_width, fig_height = plt.gcf().get_size_inches()

	import matplotlib.gridspec as gridspec

	fig = plt.figure(figsize=(fig_width*2, fig_height), constrained_layout=True)
	
	gs = fig.add_gridspec(2, 4)

	ax1 = fig.add_subplot(gs[:2,:2])

	get_geometry_plot(ax=ax1)

	ax2 = fig.add_subplot(gs[0,2])

	plot_entropy_rising(ax2)

	ax3 = fig.add_subplot(gs[0,3])

	plot_media_category_differences(ax3)

	ax4 = fig.add_subplot(gs[1,2])

	plot_rise_short_form_media(ax=ax4, prevalence=0.4, xlim_right=8)

	ax5 = fig.add_subplot(gs[1,3])

	plot_rise_short_form_media(ax=ax5, prevalence=2, xlim_right=8)
	 

	plt.tight_layout()
	plt.savefig("images/patch_geometry.png", dpi=300)

	plt.show()


def get_geometry_plot_book():

	plt.ylabel("Utility", fontproperties=FONT_PROP)

	xtick_marks = ['']*30
	#xtick_marks[10] = r"$\frac{1}{\lambda_p}$"
	#xtick_marks[20] = r"$\frac{1}{\lambda_p} + \bar{t}_p$"
	#xtick_marks[20] = r"$t_h"


	ytick_marks = ['']*22
	#ytick_marks[10] = r"$\bar{u}_p$"

	plt.xticks(np.arange(0,3,0.1), xtick_marks)
	plt.yticks(np.arange(0,2.2,0.1), ytick_marks)
	
	ax = plt.gca()

	ax.tick_params(axis=u'both', which=u'both',length=0)

	plt.ylim(0,2.2)
	plt.xlim(0,4.5)
	plt.xlabel("Time", fontproperties=FONT_PROP)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	prevalence=1.25
	handling_time=3.2
	q=2
	n=1
	color=COLOR_FIC


	#plt.axvline(x=2, ymax=1/2.2, color="lightgray", linewidth=LINEWIDTH)
	#plt.axhline(y=1, xmax=2/4.5, color="lightgray", linewidth=LINEWIDTH)

	plot_discrete_info_curve(prevalence=prevalence, handling_time=handling_time, q=q, n=n, color=color, size_ratio=1)
	plot_expected_patch_utility(prevalence=prevalence, handling_time=handling_time, q=q, n=n, color=color, size_ratio=1)

	for label in ax.get_xticklabels():
		label.set_fontproperties(FONT_PROP)

	for label in ax.get_yticklabels():
		label.set_fontproperties(FONT_PROP)

	plt.title("A Book")

	#plt.annotate(r"$\bar{r}_p$", (1.6,0.4), fontproperties=FONT_PROP)
	#plt.annotate(r"$R_{patch}$", (1.3,1.5), fontproperties=FONT_PROP)


def get_geometry_plot_twitter():

	plt.ylabel("Utility", fontproperties=FONT_PROP)

	xtick_marks = ['']*30
	#xtick_marks[10] = r"$\frac{1}{\lambda_p}$"
	#xtick_marks[20] = r"$\frac{1}{\lambda_p} + \bar{t}_p$"
	#xtick_marks[20] = r"$t_h"


	ytick_marks = ['']*22
	#ytick_marks[10] = r"$\bar{u}_p$"

	plt.xticks(np.arange(0,3,0.1), xtick_marks)
	plt.yticks(np.arange(0,2.2,0.1), ytick_marks)
	
	ax = plt.gca()

	ax.tick_params(axis=u'both', which=u'both',length=0)

	plt.ylim(0,2.2)
	plt.xlim(0,4.5)
	plt.xlabel("Time", fontproperties=FONT_PROP)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)


	prevalence=1.25
	handling_time=0.2
	q=0.5
	n=4
	color=COLOR_MAG


	#plt.axvline(x=2, ymax=1/2.2, color="lightgray", linewidth=LINEWIDTH)
	#plt.axhline(y=1, xmax=2/4.5, color="lightgray", linewidth=LINEWIDTH)

	plot_discrete_info_curve(prevalence=prevalence, handling_time=handling_time, q=q, n=n, color=color, size_ratio=1)
	plot_expected_patch_utility(prevalence=prevalence, handling_time=handling_time, q=q, n=n, color=color, size_ratio=1)

	for label in ax.get_xticklabels():
		label.set_fontproperties(FONT_PROP)

	for label in ax.get_yticklabels():
		label.set_fontproperties(FONT_PROP)


	plt.title("The News")


	#plt.annotate(r"$\bar{r}_p$", (1.6,0.4), fontproperties=FONT_PROP)
	#plt.annotate(r"$R_{patch}$", (0.9,0.7), fontproperties=FONT_PROP)
	#plt.annotate(r"$R_{patch}$", (1.3,1.5), fontproperties=FONT_PROP)




def plot_book_vs_twitter():


	fig = plt.figure(figsize=(6.4,4.8), constrained_layout=True)
	
	plt.subplot(2, 2, 2)

	get_geometry_plot_book()

	plt.legend(prop={'size': 8})

	plt.subplot(2, 2, 4)


	get_geometry_plot_twitter()

	plt.legend(prop={'size': 8})

	plt.tight_layout()

	plt.savefig("images/book_vs_twitter.tiff", format="tiff", dpi=300)
	
	plt.show()




if __name__=="__main__":
	plot_patch_geometry()