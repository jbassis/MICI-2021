"""
Try to identify terminus position of glaciers from input files
"""

import pylab as plt
from fenics import *

import numpy as np

from leopart import (
    particles,
    l2projection,
)

from geopy import distance
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter

import os.path
from os import path

def read_calving_front_sim(fname_base):
        fname_ext = '.npz'
        fname = fname_base+fname_ext
        print(fname)


        # Load particle data
        if path.exists(fname):
            tracer_data = np.load(fname)
        else:
            print('Cannot read file')


        t=tracer_data['t'].item()


        # Load mesh
        mesh_file = fname_base +'.xml'
        mesh = Mesh(mesh_file)

        # Make particle class
        n=len(tracer_data['xm'])
        xp =  np.vstack((tracer_data['xm'],tracer_data['zm'])).transpose().reshape(n,2)
        pstrain = tracer_data['strain']
        pepsII = tracer_data['epsII']
        ptemp = tracer_data['temp']
        p = particles(xp, [pstrain,ptemp,pepsII], mesh)

        # Interpolate particles to mesh
        Vdg = FunctionSpace(mesh, 'DG',1)
        strain = Function(Vdg)
        lstsq_strain = l2projection(p, Vdg, 1) # First variable???
        lstsq_strain.project_mpm(strain) # Projection is stored in phih0

        # Boundary mesh with portion above sea level marked
        bmesh = BoundaryMesh(mesh,'exterior',order=True)
        x = bmesh.coordinates()
        #ymax = np.max(x[x[:,0]==0,1])
        filter = (x[:,0]>1e-4) & (x[:,1]>0)
        xm = np.min(x[filter,0])
        id = np.argwhere(x[:,0]==xm).item()
        # Check if nodes increasing or decreasing
        if (x[id-1,0]>x[id,0]):
            # Decrease nodes
            inc = -1
            stop = 0
        else:
            # Increase nodes
            inc = 1
            stop = len(x)

        iold= id
        for i in range(id,stop,inc):
            if x[i,1]>0.0:
                slope = (x[i,1]-x[iold,1])/(x[i,0]-x[iold,0])
                #print(x[i,0],strain(x[i]),strain(x[i])>0.99,slope,slope<-pi/3)
                #print(-slope*180/pi)
                if strain(x[i])>0.1:
                    L=x[iold,0]
                    break
                elif np.abs(slope)>pi/6:
                    L=x[iold,0]
                    break

                iold = i
        print('Terminus position',L)
        # Extract profile centered on terminus
        filter = (x[:,1]>0.0) & (x[:,0]>10) & (x[:,0]<L+5*800)
        xp = x[filter,0]-L
        zp = x[filter,1]
        idx = np.argsort(xp)
        xp = xp[idx]
        zp = zp[idx]
        zp = gaussian_filter(zp, 1.5)

        #fname = fname_base + 'term_pos.npz'
        #print(fname)

        return xp,zp

def read_calving_front_oib(track_name):
    # Read csv file
    data = np.genfromtxt(track_name, delimiter=',')
    # There are four points per track, take the first point
    lat = (data[0:-4:4,1]+data[1:-3:4,1]+data[2:-2:4,1]+data[3:-1:4,1])/4
    long = (data[0:-4:4,2]+data[1:-3:4,2]+data[2:-2:4,2]+data[3:-1:4,2])/4


    dist = []
    #"""
    # Calculate distance between lat,long and initial point in meters
    pt0 = (lat[0],long[0])
    dist.append(0.0)
    for i in range(1,len(lat)):
        x ,y= lat[i],long[i]
        pt = (x,y)
        d = distance.distance(pt,pt0).km*1e3
        dist.append(d+dist[-1])
        pt0 = pt
    dist = np.array(dist) #-8e3
    #"""

    # Find elevation of the first track
    elev = (data[0:-4:4,3]+data[1:-3:4,3]+data[2:-2:4,3]+data[3:-1:4,3])/4

    #elev = data[3:-1:4,3]
    if elev[-1]>elev[0]:
        start = len(elev)-1
        end = 0
        inc = -1
    else:
        start = 0+1
        end = len(elev)
        inc = 1


    # Find calving front position??
    x = dist
    iold = start
    s = []
    for i in range(start,end,inc):
        if iold!=start:
            slope = (elev[i]-elev[iold])/(x[i]-x[iold])
            s.append(slope)
            if np.abs(slope)>pi/10 and elev[i]<150:
                L=x[i-1]
                print(L)
                break
        iold = i
    print(np.max(np.array(s)))

    elev = gaussian_filter(elev, 1)
    return dist-L,elev

def fit_oib_to_sim(track_name,sim_name,sign='neg'):
    # Read in track and sim files
    dist_track,elev_track = read_calving_front_oib(track_name)
    dist_sim,elev_sim = read_calving_front_sim(sim_name)

    if sign=='neg':
        dist_track = - dist_track

    # Linearly interpolate sim data
    f = interp1d(dist_sim, elev_sim, kind='cubic')

    filter = (dist_track>-1e3) & (dist_track<-20)
    #err = np.sqrt(sum((elev_track[filter] - f(dist_track[filter])**2)))/len(dist_track[filter])
    x_shift = np.linspace(-1e3,1e3,51)
    z_shift = np.linspace(-50,50,51)
    nx = len(x_shift)
    ny = len(z_shift)
    #X,Z = np.meshgrid(x_shift,z_shift)
    err = np.zeros((ny,nx))
    for i in range(len(z_shift)):
        z = z_shift[i]
        for j in range(len(x_shift)):
            x = x_shift[j]
            err[i,j] = np.sum((elev_track[filter]+z - f(dist_track[filter]+x))**2)

    #print(np.argmin(err))
    idi,idj=np.unravel_index(err.argmin(), err.shape)
    z = z_shift[idi]
    x = x_shift[idj]
    print(x,z)
    return dist_track+x,elev_track+z


def plot_oib_sim(ax,dist_track,elev_track,dist_sim,elev_sim,title,label=None,title2='Simulation'):
    xmin = -4e3/1e3
    xmax =  1e3/1e3
    offset = 25.0
    p1=ax.plot(dist_track/1e3,elev_track-offset)
    p2=ax.plot(dist_sim/1e3,elev_sim-offset)
    plt.xlim([xmin,xmax])
    plt.ylim([60-offset,205-offset])
    ax.text(0.92,184-offset,title,color=p1[0].get_color(),fontweight='bold',ha='right')
    ax.text(0.92,184-offset-20,title2,color=p2[0].get_color(),fontweight='bold',ha='right')
    plt.xlabel('Distance (km)')
    plt.ylabel('Elevation (m)')
    ax.text(-3.85,187-offset,label,fontweight='bold')
    plt.tight_layout()
