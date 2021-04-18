"""
Compare m-ice simulated ice sheet profile with OIB measured profile
Start with helheim glacier
"""
from importlib import reload


import numpy as np
import pylab as plt

import get_terminus
reload(get_terminus)
from get_terminus import *

xmin = -4e3
xmax =  2e3

#plt.close('all')
fig_width_pt = 246.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inches
golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height =fig_width*golden_mean       # height in inches
fig_size = [fig_width*1.5,fig_height*1.5]

params = {
          'axes.labelsize': 10,
          'legend.fontsize': 10,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True,
          'figure.figsize': fig_size}
plt.rcParams.update(params)

plt.figure(3)
plt.clf()
# Track 1
sim_name_base = '../Data/sim_data/water_depth_700/bed_slope_-0.01_flux_6.0/glacier_cliff_'
track_name = '../Data/oib_data/jakobshavn/ILATM2_20110406_135040_smooth_nadir3seg_50pt.csv'
sim_name = sim_name_base+str(900).zfill(3)
sim_name_base = '../Data/sim_data/water_depth_700/buttressing_25kPa/glacier_cliff_'
sim_name = sim_name_base+str(210).zfill(3)
dist_sim,elev_sim = read_calving_front_sim(sim_name)
dist_track,elev_track = read_calving_front_oib(track_name)
ax1=plt.subplot(2,2,1)
plot_oib_sim(ax1,-dist_track+370,elev_track-35.5,dist_sim,elev_sim,r'{Jakobshavn 2011/04/06}',label=r'\textbf{A}',title2='25 kPa buttressing')

# Jakobshavn Track 3
sim_name_base = '../Data/sim_data/water_depth_700/bed_slope_-0.01_flux_6.0/glacier_cliff_'
track_name = '../Data/oib_data/jakobshavn/ILATM2_20150421_135359_smooth_nadir3seg_50pt.csv'
sim_name = sim_name_base+str(920).zfill(3)
dist_sim,elev_sim = read_calving_front_sim(sim_name)
dist_track,elev_track = read_calving_front_oib(track_name)
ax2=plt.subplot(2,2,2)
plot_oib_sim(ax2,-dist_track+100,elev_track-7,dist_sim,elev_sim,r'{Jakobshavn 2015/04/21}',label=r'\textbf{B}',title2='0 kPa buttressing')






# Helheim Track 1
sim_name_base = '../Data/sim_data/water_depth_700/bed_slope_0.0_flux_0.0/glacier_cliff_'
track_name = '../Data/oib_data/helheim/ILATM2_20100508_125016_smooth_nadir3seg_50pt.csv'
dist_track,elev_track = read_calving_front_oib(track_name)
sim_name = sim_name_base+str(700).zfill(3)
sim_name = sim_name_base+str(1750).zfill(3)
dist_sim,elev_sim = read_calving_front_sim(sim_name)
ax3=plt.subplot(2,2,3)
#plot_oib_sim(ax5,-dist_track+100,elev_track-25,dist_sim,elev_sim,'2010/05/08',label='a')
plot_oib_sim(ax3,-dist_track+100,elev_track-35,dist_sim,elev_sim,r'{Helheim 2010/05/08}',label=r'\textbf{C}',title2='0 kPa buttressing')

# Helheim Track 2
sim_name_base = '../Data/sim_data/water_depth_700/bed_slope_0.0_flux_0.0/glacier_cliff_'
track_name = '../Data/oib_data/helheim/ILATM2_20110419_162016_smooth_nadir3seg_50pt.csv'
dist_track,elev_track = read_calving_front_oib(track_name)
#sim_name = sim_name_base+str(720).zfill(3)
sim_name_base = '../Data/sim_data/water_depth_700/bed_slope_0.0_flux_0.0/glacier_cliff_'
sim_name = sim_name_base+str(1310).zfill(3)
#sim_name = sim_name_base+str(1830).zfill(3)
dist_sim,elev_sim = read_calving_front_sim(sim_name)
ax4=plt.subplot(2,2,4)
#plot_oib_sim(ax6,-dist_track+50,elev_track-15,dist_sim,elev_sim,'2011/04/19',label='b')
sim_name = sim_name_base+str(1830).zfill(3)
dist_sim,elev_sim = read_calving_front_sim(sim_name)
plot_oib_sim(ax4,-dist_track+50,elev_track-24,dist_sim,elev_sim,r'{Helheim 2011/04/19}',label=r'\textbf{D}',title2='0 kPa buttressing')

plt.show()
plt.savefig('../Figures/oib_sim_compare.pdf')
