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

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# Add Labels and everything else
axes[0].plot(times, corr_KN_KS, 'kx')
axes[0].set_title('Phot_KN and Phot_KN-in-SN over time')

axes[1].plot(times, corr_KN_SK, 'kx')
axes[1].set_title('Phot_KN and Phot_super-KN over time')

axes[2].plot(times, corr_KS_SK, 'kx')
axes[2].set_title('Phot_KN-in-SN and Phot_super-KN over time')

plt.tight_layout()
plt.show()

# Repeat for the 03-07 as well