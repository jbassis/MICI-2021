"""
Plot composite rheology of ice
"""

import pylab as plt
import numpy as np

fig_width_pt = 246.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inches
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
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

secpera = 86400.0*365.24

# -20 C
Bdiff = 477185987.01732063
Bdisl = 644329.0831880621

# -10 C
#Bdisl = 449034.75838176935
#Bdiff = 163271051.69572762


tau_y = 0.75e6

epsII = np.logspace(-16,12,101)


visc = 0.5*(epsII**(2.0/3.0)/Bdisl + 1.0/Bdiff + epsII/tau_y)**(-1.0)
visc_disl = 0.5*Bdisl*epsII**(1/3-1)
visc_diff = 0.5*Bdiff

visc_plas = 0.5*tau_y/epsII
idx = np.where(visc_disl>visc_plas)[0][0]
eps_crit1 = epsII[idx]/secpera
idx = np.where(visc_diff>visc_disl)[0][0]
eps_crit2 = epsII[idx]/secpera


plt.clf()
plt.subplot(2,1,1)
plt.loglog(epsII/secpera,visc*secpera,'k')
plt.loglog(epsII/secpera,visc_disl*secpera,'--',c='#1f77b4')
plt.axvline(x=eps_crit1, color='gray', linestyle='--')
plt.axvline(x=eps_crit2, color='gray', linestyle='--')
plt.text(2*10**-16,10**20,'diffusion creep')
#plt.text(4*10**-12,10**20,'power-law creep')
plt.text(10**-6,10**20,'plastic')
plt.text(2*10**-5,10**12,"power-law creep",c='#1f77b4')
plt.text(0.25*10**-5,10**4.5,'composite rheology',c='k')

#plt.semilogx(epsII/secpera,2*visc_diff*epsII/1e6,'-.b')
#plt.semilogx(epsII/secpera,tau/1e6)
#plt.axhline(y=tau_y/1e6, color='gray', linestyle='--')
plt.xlim([10**-16,10**-1])
#plt.ylim([0,1])
#plt.xlabel(r'$\epsilon_e$ (s)')
plt.ylabel(r'$\eta$ (Pa$\cdot$s)')

plt.subplot(2,1,2)
plt.semilogx(epsII/secpera,2*visc*epsII/1e6,'k')
plt.semilogx(epsII/secpera,2*visc_disl*epsII/1e6,'--',c='#1f77b4')

#plt.semilogx(epsII/secpera,2*visc_diff*epsII/1e6,'-.b')
#plt.semilogx(epsII/secpera,tau/1e6)


plt.xlim([10**-16,10**-1])
plt.ylim([0,1])
plt.xlabel(r'$\epsilon_e$ (s$^{-1}$)')
plt.ylabel(r'$\tau_e$ (MPa)')
plt.text(2*10**-16,0.8,'diffusion creep')
plt.text(4*10**-12,0.8,'power-law creep')
plt.text(10**-6,0.8,'plastic')
plt.text(0.3*10**-11,0.45,"power-law creep",c='#1f77b4')
plt.text(10**-6,0.45,'composite rheology',c='k')

plt.axhline(y=tau_y/1e6, color='gray', linestyle='--')
plt.axvline(x=eps_crit1, color='gray', linestyle='--')
plt.axvline(x=eps_crit2, color='gray', linestyle='--')
#plt.text(1.5*10**(-11),0.5,'diffusion creep',fontsize=10,c='#1f77b4')
#plt.text(10**(-5),0.55,'composite rheology',fontsize=10,c='k')
plt.tight_layout()
plt.savefig('../Figures/rheology.pdf')
plt.show()
