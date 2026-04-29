import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

data_files = os.listdir('./data/photo_scores/02')

full_data = pd.DataFrame()

# Combining all CSV files into one dataframe
for file in data_files:
    path = './data/photo_scores/02/' + file
    full_data = pd.concat([full_data, pd.read_csv(path)], ignore_index=True)

# Sorting based on dt
full_data = full_data.sort_values('dt', ascending=True)
times = list(set(full_data['dt'].array))
corr_KN_KS = []
corr_KN_SK = []
corr_KS_SK = []

for dt in times:
    subset = full_data[full_data['dt'] == dt]
    corr_KN_KS.append(subset['phot_KN'].corr(subset['phot_KN-in-SN']))
    corr_KN_SK.append(subset['phot_KN'].corr(subset['phot_super-KN']))
    corr_KS_SK.append(subset['phot_KN-in-SN'].corr(subset['phot_super-KN']))

plt.figure(figsize=(10,8))
plt.plot(times, corr_KN_KS, 'kx')
plt.axhline(y=np.mean(corr_KN_KS), color='black', label=f'Average Value: {np.mean(corr_KN_KS):.3f}')
plt.xlabel('Time (D)')
plt.ylabel('Pearson Correlation')
plt.legend()
plt.title('Correlation between phot_KN and phot_KN-in-SN over time')
plt.tight_layout()
plt.savefig('./out/KN_KS_Correlation.jpg')

plt.figure(figsize=(10,8))
plt.plot(times, corr_KN_SK, 'kx')
plt.axhline(y=np.mean(corr_KN_SK), color='black', label=f'Average Value: {np.mean(corr_KN_SK):.3f}')
plt.xlabel('Time (D)')
plt.ylabel('Pearson Correlation')
plt.legend()
plt.title('Correlation between phot_KN and phot_Super-KN over time')
plt.tight_layout()
plt.savefig('./out/KN_SK_Correlation.jpg')

plt.figure(figsize=(10,8))
plt.plot(times, corr_KS_SK, 'kx', label='Data')
plt.axhline(y=np.mean(corr_KS_SK), color='black', label=f'Average Value: {np.mean(corr_KS_SK):.3f}')
plt.xlabel('Time (D)')
plt.legend()
plt.ylabel('Pearson Correlation')
plt.title('Correlation between phot_KN-in-SN and phot_super-KN over time')
plt.tight_layout()
plt.savefig('./out/KS_SK_Correlation.jpg')

# Repeat for the 03-07 as well