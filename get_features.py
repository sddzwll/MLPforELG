#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 12:50:31 2022

@author: wll
"""

from astropy.io import fits
import numpy as np
import pandas as pd
import scipy.signal as signal

def load_xy_LAMOST(filename):
    '''
    get the wave, flux and redshift of LAMOST spectrum

    Parameters
    ----------
    filename : str or list 
        name of spectrum.

    Returns
    -------
    x : array
        wave of spectrum.
    y : array
        flux of spectrum.
    z : float
        redshift of spectrum.

    '''
    hdulist = fits.open(filename)
    z = float(hdulist[0].header['Z']) # LAMOST redshift
    y = hdulist[0].data[0]  # LAMOST flux
    x = hdulist[0].data[2]   # LAMOST wave
    return x, y, z

class normalization():
    def __init__(self,wave,flux):
        self.wave=wave
        self.flux=flux

    def mask_strong_line(self,wave1,flux1):
        '''
        mask the strong lines of spectrum 
        Parameters
        ----------
        wave1 : array
            restwave of spectrum.
        flux1 : array
            flux of spectrum.

        Returns
        -------
        wave and flux of spectrum after masking the strong lines.
        '''
        mask_band=np.loadtxt('mask_band.txt') ##the file of strong lines
        for i in range(len(mask_band)):

            n = np.where((wave1>=mask_band[i][0])&(wave1<=mask_band[i][1]))
            if len(n[0])==0 or len(n[0])==1:
                continue
            mask_wave = wave1[n]
            mask_flux = flux1[n]
            k = (mask_flux[-1]-mask_flux[0])/(mask_wave[-1]-mask_wave[0])
            y = k*(mask_wave-mask_wave[0])+mask_flux[0]
            flux1[n]=y
        return wave1,flux1

    def find_conti_spec(self,wave,flux):
        '''
        Fitting the stellar continua using median filtering
        Parameters
        ----------
        wave : array
            restwave of spectrum.
        flux : array
            flux of spectrum.

        Returns
        -------
        list
            the wave and flux of stellar continua.
        '''
        
        flux =signal.medfilt(flux,kernel_size=201)
        return [wave,flux]

    def normalize_spec(self):
        '''
        normalize the spectrum
        Returns
        -------
        wave_new : array
            the wave of normalized spectrum.
        flux_n : array
            the normalized flux.

        '''
        n = np.where((self.wave>=min(self.wave))&(self.wave<=max(self.wave)))
        wave0 = self.wave[n]
        flux0 = self.flux[n]
        wave1,flux1 = self.mask_strong_line(wave0,flux0)
        #plt.plot(self.wave,self.flux,'k-')
        wave3, flux_c = self.find_conti_spec(wave1,flux1)
        wave_new=wave3
        n=np.where(flux_c!=0)
        flux_c=flux_c[n]
        wave3=wave3[n]
        flux_c = np.interp(wave_new,wave3,flux_c)
        flux_c=flux_c[17:-17]
        wave_new=wave_new[17:-17]
        self.flux=self.flux[17:-17]
        flux_n = self.flux/flux_c
        return wave_new, flux_n

fp = open("spec_name.txt", 'r')
spec_list = list(fp)
fp.close()
spec_list = [x.strip() for x in spec_list]

line_flux_all = []
line_center1=[4862.68,4960.295,5008.24,6302.046] #the line center of H$\beta$, [OIII]4959,[OIII]5007, and [OI]
line_range1 = [6539, 6595] #the range of H$\alpha$, [NII]6548,and [NII]6584
line_range2 = [6708, 6742] #the range of [SII]6717,  [SII]6731
wave_new = np.arange(3800, 7000, 1)
count = 0
for spec in spec_list:
    try:       
        count = count+1
        print(count)
        wave, flux, z = load_xy_LAMOST(spec)
        restwave = wave / (1 + z)
        flatt = normalization(restwave, flux)
        x_flat, y_flat = flatt.normalize_spec()
        flux_line=[spec]
        flux_inter = np.interp(wave_new, x_flat, y_flat)
        for line_c in line_center1:
            nn = np.where((wave_new>=line_c-10-1) &(wave_new<=line_c+10+1))
            ff = flux_inter[nn]            
            flux_line.extend(ff)

        nn1 = np.where((wave_new>=line_range1[0]) &(wave_new<=line_range1[1]))
        ff1 = flux_inter[nn1]
        flux_line.extend(ff1)

        nn3 = np.where((wave_new>=line_range2[0]) &(wave_new<=line_range2[1]))
        ff3 = flux_inter[nn3]
        flux_line.extend(ff3)   
        line_flux_all.append(flux_line)
    except Exception as e:
        print(e)
        continue
df = pd.DataFrame(line_flux_all)
df.to_csv("spec_features.csv",index=0)