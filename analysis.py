import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

full_data = pd.read_csv('.\data\S251112cm_candidates_2026-03-06_scores.csv')

# Before actually correlating, consider performing 2 correlations, one with all distance values, and others with only reasonable distance values
# Distance threshold (1e-5)
data_clean = full_data[full_data['dist'] > 1e-5]
relevant_data = data_clean[['2D', 'dist', 'phot_KN', 'phot_KN-in-SN', 'phot_super-KN', 'predet_KN', 'predet_KN-in-SN', 'predet_super-KN']]
relevant_data_unfiltered = full_data[['2D', 'dist', 'phot_KN', 'phot_KN-in-SN', 'phot_super-KN', 'predet_KN', 'predet_KN-in-SN', 'predet_super-KN']]

corr_matrix = relevant_data.corr()
corr_matrix_unfiltered = relevant_data_unfiltered.corr()

corr_matrix.to_csv('filtered_correlations.csv')
corr_matrix_unfiltered.to_csv('unfiltered_correlations.csv')