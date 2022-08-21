# MLPforELG
MLP classifiers for automatic classifying the emission-line galaxies
(1)two constructed models
--MLPonMainsample.pickle: this model is trained based on Main sample
--MLPonPart_out.pickle: If one does not want to classify the spectra in (-0.08, 0.08) on both sides of three division curves, this model can be used.
(2)we give an example LAMOST spectrum to carry out get_features.py: spec-56648-VB003N26V2_sp05-235.fits.gz(the spectral name in spec_name.txt )
(3)get_features.py: construct the feature space 
--de-redshift a spectrum to the rest frame, normalize and re-sample the spectrum with an interval of 1 \AA.
--select nine emission lines: H$\beta$, [OIII]$\lambda$$\lambda$4959,5007, [OI], H$\alpha$, [NII]$\lambda$$\lambda$6548,6584 and [SII]$\lambda$$\lambda$6717,6731
--get the flux pixels around the line center $\pm$10 \AA , and combine the fluxes of the nine emission lines, and then obtain 180 flux pixels to form our feature space.
(4)predictbyMLP.py
load one of our constructed MLP classifiers to predict the catagory of input spectrum.
