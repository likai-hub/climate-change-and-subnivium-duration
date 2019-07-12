The subnivium is an important seasonal refugium at the interface between snowpack and ground that protects diverse species from extreme winter temperatures. This repository includes the code for data calcualtions and analysis in our project which aims to characterize changing pattern of subnivium conditions at the global scale, quantify effects of climate change, and make predictions for the changes in subnivium duration in the 21st century. We inferred global patterns in subnivium duration using the past and future duration of frozen ground with snow cover (Dsc) and without snow cover (Dfwos) derived from remotely sensed datasets and climate projections. Here we present the code for the main procedures of data processing described in the Methods section in our manuscript (Zhu et al., (2019) Climate change causes functionally colder winters for snow cover-dependent organisms. Nature Climate Change, In revision).

(1) Determining_frozen_season_start.py:
The script is to determine the start of the frozen season from the NASA MEaSUREs Global Record of Daily Landscape  Freeze/Thaw Status dataset.
(2) Determining_frozen_season_end.py:
The script is to determine the end of the frozen season from the NASA MEaSUREs Global Record of Daily Landscape  Freeze/Thaw Status dataset.
(3) Determining_frozen_season_length.py:
The script is to determine the length of the frozen season from the above identified start and end of the frozen season.
(4) interpolating_cloud_pixels_within_snow_cover_dataset.py:
The script is to estimate the snow cover status for cloud-contaminated pixels in snow-cover product. 
(5) Dsc_Dfwos_calculation.py:
The script is to calculate the duration of frozen ground with snow cover (Dsc) and without snow cover (Dfwos) by combining snow cover status, ground freeze/thaw status, and the range of the frozens season.
(6) TDiff_for_Dsc_Dfwos_Fig_1.py:
The script is to calculate the differences in the average Tdiff for the period of Dsc and Dfwos.  Tdiff is computed from weather station data by subtracting air temperatures from ground temperatures. 
(7) preprocessing_snow_depth_data_from_stations.py:
The script is to process snow depth data from multiple sources in order to select the stations with more than 20 years of continuous measurements from 1982-2013.
(8) correlation_Dsc_mean_snow_depth.py: 
The script is to calculate the correlation between Dsc and mean snow depth of the period DSc for multiple selected stations.
(9) accuracy_assessment_dsc.R; accuracy_assessment_dfwos.R:
The R scripts are to make scatterplots showing the correlation between station-based Dsc/Dfwos and remote sensing-based Dsc/Dfwos
(10) summarizing_Dsc_Dfwos_by_latitudes.py;summarizing_Dsc_Dfwos_by_dem.py;summarizing_Dsc_Dfwos_by_landcover.py:
These scripts are to summarize the past, current, and future Dsc and Dfwos by latitude, elevation, and land-cover type.
(11) Dsc_prediction_2014_2100.R; Dfwos_prediction_2014-2100.R:
These R scripts are to make predictions of Dsc and Dfwos from CMIP5 climate projections from 33 GCMs.
(12) trend_analysis_Dfwos_1982-2014.R;trend_analysis_Dsc_1982-2014.R:
These R scripts are to make global trend analysis for Dsc and Dfwos from 1982-2014 using linear regression models with autocorrlated errors.
(13) temperature_precipitation_effects_on_Dsc.R; temperature_precipitation_effects_on_Dfwos.R:
These R scripts are to disentangle the effect of winter temperatures and precipitation on Dsc and Dfwos based on linear regression models with autocorrlated errors.
(14) Dsc_difference_between_past_and_current_periods_SFig.5.R; Dfwos_difference_between_past_and_current_periods_SFig.5.R:
These scripts are used to calcuate the global pattern of the differences in average Dsc and Dfwos between the past (1982-1986) and current (2010-2014) periods. 
(15) Dsc_difference_between_past_and_future_periods_Fig.6.R; Dfwos_difference_between_past_and_future_periods_Fig.6.R:
These scripts are used to calcuate the global pattern of the differences in average Dsc and Dfwos between the current(1982-2014) and current (2071-2100) periods.
(16) Dsc_Dfwos_by_latitude_elevation_land_cover_Fig.2.R:
The script is to use to make bar plots shown in Fig. 2 in the manuscript. 

