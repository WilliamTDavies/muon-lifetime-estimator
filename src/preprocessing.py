import pandas as pd
from pathlib import Path

def get_data():
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = ROOT_DIR / "data" / "raw" / "lifetimeOut.txt"
    df = pd.read_csv(DATA_DIR, sep="\t")
    return df


#df = get_data()
#print(df.head())
#print(f"\n\n {df.shape}")


import matplotlib.pyplot as plt

# Define boxplot statistics
box1 = {
    'med': 1.2251485,
    'q1': 0.81667675,
    'q3': 1.77195825,
    'whislo': 0.279201,  # min
    'whishi': 2.698333,  # max
    'fliers': []
}

box2 = {
    'med': 1.267314,
    'q1': 1.03020875,
    'q3': 2.12351525,
    'whislo': 0.677699,
    'whishi': 2.916017,
    'fliers': []
}

# Create plot
fig, ax = plt.subplots()

ax.bxp([box1, box2], showfliers=False)

# Optional labels
ax.set_xticklabels(['Baseline', 'Heatwave'])
ax.set_ylabel('UHII (°C)')
ax.set_title('Box and Whisker Plot')

plt.show()