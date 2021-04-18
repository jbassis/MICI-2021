import numpy as np
import pylab as plt

from importlib import reload


import matplotlib
matplotlib.style.use('seaborn-colorblind')

import matplotlib.gridspec as gridspec


import plot_cliff
reload(plot_cliff)
from plot_cliff import *
plt.close('all')

color = '#CC6677'
color2 = '#88CCEE'

fig=plt.figure(2)
width  = 6.0
height = width / 1.618*1.25
fig=plt.figure(num=2, figsize=(width, height), facecolor='w', edgecolor='k')
fig.set_size_inches(width,height,forward=True)
#ax10 = fig.add_axes([0.125, 0.2, 0.75, 0.75])

#ax10 =  fig.add_axes([snap_start+0.0125, snap_start_vert+0.3, snap_width*3-0.04-0.0175, 0.125])
#ax10.patch.set_alpha(0)

def plot_shit(ax,fname,style='-'):
    data1=np.load(fname)
    t = data1['t']
    yr = np.array((np.mod(t,365)),dtype=int)
    day = (t - yr)*365
    L = data1['L'][0]
    p1=ax.plot(day,(data1['L']-L)/1e3,'-',linewidth=2,linestyle=style)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.yaxis.set_label_position("left")
    ax.spines['left'].set_position(('outward', 0))
    plt.xlim([0,100])
    plt.ylim([-2,1.0])
    ax.set_yticks([-2,-1,0,1.0])
    ax.set_xticks([0,50,100])
    #ax.hlines(0,0,70,color='k',linestyle='--')



L = 9600
fname1 = '../data/cliff/water_depth_700/glacier_surf_slope_0.02_bed_slope_-0.02_flux_2.0_high_res_CFL/glacier_cliff_'+ 'term_pos.npz'
fname4 = '../data/buttressing/water_depth_700_buttressing_25.0kPa_removed_1.0day/glacier_surf_slope_0.02_bed_slope_-0.02_flux_2.0_high_res_T_-20.0_CFL/glacier_cliff_'+ 'term_pos.npz'
fname5 = '../data/buttressing/water_depth_700_buttressing_25.0kPa_removed_10.0day/glacier_surf_slope_0.02_bed_slope_-0.02_flux_2.0_high_res_T_-20.0_CFL/glacier_cliff_'+ 'term_pos.npz'
fname6 = '../data/buttressing/water_depth_700_buttressing_25.0kPa_removed_50.0day/glacier_surf_slope_0.02_bed_slope_-0.02_flux_2.0_high_res_T_-20.0_CFL/glacier_cliff_'+ 'term_pos.npz'
#fname4 = '../data/buttressing/water_depth_700_buttressing_50.0kPa_removed_1.0day/glacier_surf_slope_0.02_bed_slope_-0.02_flux_2.0_high_res_T_-20.0_CFL/glacier_cliff_'+ 'term_pos.npz'
fname2 = '../data/buttressing/water_depth_700_buttressing_50.0kPa_removed_10.0day/glacier_surf_slope_0.02_bed_slope_-0.02_flux_2.0_high_res_T_-20.0_CFL/glacier_cliff_'+ 'term_pos.npz'
fname3 = '../data/buttressing/water_depth_700_buttressing_50.0kPa_removed_50.0day/glacier_surf_slope_0.02_bed_slope_-0.02_flux_2.0_high_res_T_-20.0_CFL/glacier_cliff_'+ 'term_pos.npz'

plt.subplots_adjust(bottom=0.15,hspace=0.5,left=0.12,wspace=0.4)
ax1 = plt.subplot(3,2,1)
plot_shit(ax1,fname1)
#ax1.text(1,0.3,r'$\Delta t=0$ d')
plt.ylabel(r'$\Delta L$ (km)',labelpad=0)
#ax1.fill_between([0,1],-2,1,color='gray',alpha=0.25)
#plt.title('25 kPa buttressing',fontsize=10)
ax1.text(0,1.1,'A',fontweight='bold')


ax2 = plt.subplot(3,2,3)

ax2.fill_between([0,10],-2,1,color='gray',alpha=0.25)
plt.ylabel(r'$\Delta L$ (km)',labelpad=0)
ax2.text(10,0.5,r'$\Delta t = 10$ d, 50 kPa')
ax2.text(0,1.1,'C',fontweight='bold')
plot_shit(ax2,fname2)
#ax2.text(40,-1,'50 kPa')


ax3 = plt.subplot(3,2,5)
#ax3.text(2,0.75,r'$\Delta t=50$ d')
plot_shit(ax3,fname3)
plt.ylabel(r'$\Delta L$ (km)',labelpad=0)
ax3.fill_between([0,50],-2,1,color='gray',alpha=0.25)
plt.xlabel('Days',labelpad=0)
ax3.text(4,-0.75,r'$\Delta t = 50$ d')
ax3.text(4,-1.3,r'50 kPa')
ax3.text(0,1.1,'E',fontweight='bold')



ax4 = plt.subplot(3,2,2)
plot_shit(ax4,fname4)
ax4.text(1.3,0.28,r'$\Delta t = 1$ d, 25 kPa')

ax4.fill_between([0,1],-2,1,color='gray',alpha=0.25)
ax4.text(0,1.1,'B',fontweight='bold')

#plt.ylabel(r'$\Delta L$ (km)',labelpad=0)

#ax4.spines['left'].set_visible(False)
#ax4.spines['right'].set_visible(True)
#ax4.yaxis.set_label_position("right")
#ax4.spines['right'].set_position(('outward', 10))
#ax1.fill_between([0,1],-2,1,color='gray',alpha=0.25)
#plt.title('50 kPa buttressing',fontsize=10)

ax5 = plt.subplot(3,2,4)
ax5.fill_between([0,10],-2,1,color='gray',alpha=0.25)
ax5.text(10,0.5,r'$\Delta t = 10$ d, 25 kPa')
plot_shit(ax5,fname5)
ax5.text(0,1.1,'D',fontweight='bold')

#plt.ylabel(r'$\Delta L$ (km)',labelpad=0)

ax6 = plt.subplot(3,2,6)
#ax6.text(10,-1.5,r'$\Delta t=50$ d')
plot_shit(ax6,fname6)
ax6.fill_between([0,50],-2,1,color='gray',alpha=0.25)
#ax6.text(50,0.5,r'$\Delta t = 50$ d')
#ax6.text(1,0.4,r'$\Delta t = 50$ d')
ax6.text(0,1.1,'F',fontweight='bold')
ax6.text(4,-0.75,r'$\Delta t = 50$ d,')
ax6.text(4,-1.3,r'25 kPa')
#plt.ylabel(r'$\Delta L$ (km)',labelpad=0)
plt.xlabel('Days',labelpad=0)
plt.show()

plt.show()

#plt.savefig('Fig_buttressing_removal.pdf')
