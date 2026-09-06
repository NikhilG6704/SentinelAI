#!/usr/bin/env python3
"""
Downloads a subset of the Server Machine Dataset (SMD) and processes it
into a format suitable for the SentinelAI AnomalyTrainer.
"""
import os
import requests
import pandas as pd
from pathlib import Path

# We'll use a single machine's training data for the cold start.
# This URL points to the raw text file in the official NetManAIOps repo.
SMD_URL = "https://raw.githubusercontent.com/NetManAIOps/SMD/master/ServerMachineDataset/train/machine-1-1.txt"

import numpy as np

# SMD has 38 metric dimensions. We'll map a few to realistic IT operations names
# and leave the rest as generic sensor names.
COLUMNS = [
    "cpu_utilization", "memory_utilization", "network_tx", "network_rx",
    "disk_io_read", "disk_io_write", "http_latency", "error_rate"
] + [f"sensor_{i}" for i in range(8, 38)]

def generate_synthetic_smd(output_dir: Path):
    print("Generating synthetic SMD dataset for bootstrapping...")
    
    num_samples = 5000
    num_features = 38
    
    # Generate normal data (mostly random noise around a mean)
    np.random.seed(42)
    data = np.random.normal(loc=0.5, scale=0.1, size=(num_samples, num_features))
    
    # Inject some anomalies
    anomaly_indices = np.random.choice(num_samples, size=50, replace=False)
    for idx in anomaly_indices:
        data[idx] = np.random.normal(loc=0.9, scale=0.2, size=num_features)
            
    df = pd.DataFrame(data, columns=COLUMNS)
    
    # In a real environment, we'd have a timestamp. The SMD data is collected
    # every 1 minute. We'll generate dummy timestamps.
    start_time = pd.Timestamp("2023-01-01 00:00:00")
    df["timestamp"] = [start_time + pd.Timedelta(minutes=i) for i in range(len(df))]
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "machine-1-1.csv"
    
    # Reorder to put timestamp first
    cols = ["timestamp"] + COLUMNS
    df = df[cols]
    
    df.to_csv(output_path, index=False)
    print(f"Successfully processed {len(df)} synthetic samples.")
    print(f"Saved dataset to {output_path}")

if __name__ == "__main__":
    # Ensure this runs relative to the project root
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "datasets" / "processed" / "smd"
    
    generate_synthetic_smd(output_dir)

