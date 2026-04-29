import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# data_files = os.listdir('./data/photo_scores/02')
data_files = os.listdir('./data/photo_scores/07')

# init_data = pd.read_csv('data\photo_scores\inits\S251112cm_candidates_2026-03-02_scores_tpost-tinit.csv')
init_data = pd.read_csv('data\photo_scores\inits\S251112cm_candidates_2026-03-07_scores_tpost-tinit.csv')

full_data = pd.DataFrame()

# Combining all CSV files into one dataframe
for file in data_files:
    # path = './data/photo_scores/02/' + file
    path = './data/photo_scores/07/' + file
    full_data = pd.concat([full_data, pd.read_csv(path)], ignore_index=True)

clean_data = pd.DataFrame()

names = set(init_data['name'].array)
for name in names:
    dt_init = init_data[init_data['name'] == name]['dt'].array[0]
    clean_data = pd.concat([clean_data, full_data[(full_data['dt'] >= dt_init) & (full_data['name'] == name)]])

# Sorting based on dt
times = list(set(clean_data['dt'].array))
corr_KN_KS = {}
corr_KN_SK = {}
corr_KS_SK = {}

def get_correlation_data():
    times_removed = []
    for dt in times:
        subset = clean_data[clean_data['dt'] == dt]
        corr_KN_KS_val = subset['phot_KN'].corr(subset['phot_KN-in-SN'], method='spearman')
        corr_KN_SK_val = subset['phot_KN'].corr(subset['phot_super-KN'], method='spearman')
        corr_KS_SK_val = subset['phot_KN-in-SN'].corr(subset['phot_super-KN'], method='spearman')

        # Some times don't have enough data to actually run the Spearman, so they are removed
        if pd.isna(corr_KN_KS_val) or pd.isna(corr_KN_SK_val) or pd.isna(corr_KS_SK_val):
            times_removed.append(dt)
        else:
            corr_KN_SK[dt] = corr_KN_SK_val
            corr_KN_KS[dt] = corr_KN_KS_val
            corr_KS_SK[dt] = corr_KS_SK_val

def plot():
    plt.figure(figsize=(10,8))
    plt.plot(corr_KN_KS.keys(), corr_KN_KS.values(), 'kx')

    final_corr = corr_KN_KS[100.0]
    plt.axhline(y=final_corr, color='blue', linestyle='--', label=f'Final Correlation: {final_corr:.3f}')

    plt.xlabel('Time (D)')
    plt.ylabel('Spearman Correlation')
    plt.legend()
    plt.title('Correlation between phot_KN and phot_KN-in-SN over time')
    plt.tight_layout()
    # plt.savefig('./out/figs/02/KN_KS_Correlation.jpg')
    plt.savefig('./out/figs/07/KN_KS_Correlation.jpg')

    plt.figure(figsize=(10,8))
    plt.plot(corr_KN_SK.keys(), corr_KN_SK.values(), 'kx')

    final_corr = corr_KN_SK[100.0]
    plt.axhline(y=final_corr, color='blue', linestyle='--', label=f'Final Correlation: {final_corr:.3f}')

    plt.xlabel('Time (D)')
    plt.ylabel('Spearman Correlation')
    plt.legend()
    plt.title('Correlation between phot_KN and phot_Super-KN over time')
    plt.tight_layout()
    # plt.savefig('./out/figs/02/KN_SK_Correlation.jpg')
    plt.savefig('./out/figs/07/KN_SK_Correlation.jpg')

    plt.figure(figsize=(10,8))
    plt.plot(corr_KS_SK.keys(), corr_KS_SK.values(), 'kx')

    final_corr = corr_KS_SK[100.0]
    plt.axhline(y=final_corr, color='blue', linestyle='--', label=f'Final Correlation: {final_corr:.3f}')

    plt.xlabel('Time (D)')
    plt.legend()
    plt.ylabel('Spearman Correlation')
    plt.title('Correlation between phot_KN-in-SN and phot_super-KN over time')
    plt.tight_layout()
    # plt.savefig('./out/figs/02/KS_SK_Correlation.jpg')
    plt.savefig('./out/figs/07/KS_SK_Correlation.jpg')

get_correlation_data()
plot()