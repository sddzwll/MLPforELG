# MLPforELG
MLP classifiers for automatic classifying the emission-line galaxies

(1)de-redshift a spectrum to the rest frame, normalize and re-sample the spectrum with an interval of 1 \AA.
(2)select nine emission lines: H$\beta$, [OIII]$\lambda$$\lambda$4959,5007, [OI], H$\alpha$, [NII]$\lambda$$\lambda$6548,6584 and [SII]$\lambda$$\lambda$6717,6731
(3)construct the feature space: get the flux pixels around the line center $\pm$10 \AA , and combine the fluxes of the nine emission lines, and then obtain 180 flux pixels to form our feature space.
(4)load one of our constructed MLP classifiers:
