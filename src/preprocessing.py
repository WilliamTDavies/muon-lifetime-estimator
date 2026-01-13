import pandas as pd
from pathlib import Path
import numpy as np

def get_data():
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = ROOT_DIR / "data" / "raw" / "muonData.csv"
    df = pd.read_csv(DATA_DIR, sep=",")
    return df

def remove_anom_pmt(df):
    indices_to_drop = df[df["channel_numb"] == "6234.4"].index # Remove the previously found anomalous PMT
    df.drop(indices_to_drop, inplace=True)
    return df

def format_data(df):
    day_secs = 86400 # Number of seconds in a Julian day
    start_day = df.at[0, "julian_day"]
    df["julian_day"] = df["julian_day"] - start_day
    df["start_decay"] = (df["julian_day"] + df["start_decay"]) * day_secs
    df["end_decay"] = (df["julian_day"] + df["end_decay"]) * day_secs
    df["decay_time"] = (df["end_decay"] - df["start_decay"]) * 10e5 # Convert pulse width to microseconds
    return df

def average_decay_by_event(df, event_tol=1e-6):
    '''
    Parameters:
    df : pandas.DataFrame
        Input dataframe containing detector records.
    event_tol : float
        Maximum time difference for detections to be considered part of the same physical event.
    '''
    # Assign event IDs via time clustering
    df = df.sort_values("start_decay").reset_index(drop=True).copy()
    event_ids = np.zeros(len(df), dtype=int)
    current_event = 0

    for i in range(1, len(df)):
        if abs(df.loc[i, "start_decay"] - df.loc[i - 1, "start_decay"]) > event_tol:
            current_event += 1
        event_ids[i] = current_event
        
    df["event_id"] = event_ids

    # Clean and average within each event
    records = []
    for event_id, group in df.groupby("event_id"):
        values = group["decay_time"].values
        med = np.median(values)
        dists = np.abs(values - med)
        idx = np.argsort(dists)[:2]
        avg = values[idx].mean()

        records.append({
            "event_id": event_id,
            "decay_time": avg
        })
    return pd.DataFrame(records).set_index("event_id")

def save_data(df):
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = ROOT_DIR / "data" / "processed" / "finalData.csv"
    df.to_csv(DATA_DIR)