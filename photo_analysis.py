import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

data_files = os.listdir('./data/photo_scores/02')

full_data = pd.DataFrame()

# Init Offset
init_data = pd.read_csv('data\photo_scores\inits\S251112cm_candidates_2026-03-02_scores_tpost-tinit.csv')

# Combining all CSV files into one dataframe
for file in data_files:
    path = './data/photo_scores/02/' + file
    full_data = pd.concat([full_data, pd.read_csv(path)], ignore_index=True)

# Check whether the values are placeholder or actual reuslts
# Check if the dt is smaller than the tinit dt file
names = set(init_data['name'].array)
for name in names:
    dt_init = init_data[init_data['name'] == name]['dt'].array[0]
    full_data = full_data[(full_data['name'] == name) & (full_data['dt'] >= dt_init)]
    # Need offset or not?

full_data = full_data.dropna(axis=0)
clean_data = full_data[full_data['dt'] >= 0]

# Initializing the lists
bin_size = 100
times = []
corr_KN_KS = []
corr_KN_SK = []
corr_KS_SK = []

def get_correlation_data():
    clean_data.sort_values('dt')
    rows_count = clean_data.shape[0]
    for i in range(0, rows_count, bin_size):
        subset = clean_data.iloc[i:i+bin_size]
        times.append(subset['dt'].mean())
        corr_KN_KS.append(subset['phot_KN'].corr(subset['phot_KN-in-SN'], method='spearman'))
        corr_KN_SK.append(subset['phot_KN'].corr(subset['phot_super-KN'], method='spearman'))
        corr_KS_SK.append(subset['phot_KN-in-SN'].corr(subset['phot_super-KN'], method='spearman'))

def plot():
    plt.figure(figsize=(10,8))
    plt.plot(times, corr_KN_KS, 'kx')
    plt.axhline(y=np.mean(corr_KN_KS), color='black', label=f'Average Value: {np.mean(corr_KN_KS):.3f}')
    plt.xlabel('Time (D)')
    plt.ylabel('Pearson Correlation')
    plt.legend()
    plt.title('Correlation between phot_KN and phot_KN-in-SN over time')
    plt.tight_layout()
    plt.savefig('./out/figs/KN_KS_Correlation.jpg')

    plt.figure(figsize=(10,8))
    plt.plot(times, corr_KN_SK, 'kx')
    plt.axhline(y=np.mean(corr_KN_SK), color='black', label=f'Average Value: {np.mean(corr_KN_SK):.3f}')
    plt.xlabel('Time (D)')
    plt.ylabel('Pearson Correlation')
    plt.legend()
    plt.title('Correlation between phot_KN and phot_Super-KN over time')
    plt.tight_layout()
    plt.savefig('./out/figs/KN_SK_Correlation.jpg')

    plt.figure(figsize=(10,8))
    plt.plot(times, corr_KS_SK, 'kx', label='Data')
    plt.axhline(y=np.mean(corr_KS_SK), color='black', label=f'Average Value: {np.mean(corr_KS_SK):.3f}')
    plt.xlabel('Time (D)')
    plt.legend()
    plt.ylabel('Pearson Correlation')
    plt.title('Correlation between phot_KN-in-SN and phot_super-KN over time')
    plt.tight_layout()
    plt.savefig('./out/figs/KS_SK_Correlation.jpg')

get_correlation_data()
plot()

# Repeat for the 03-07 as well