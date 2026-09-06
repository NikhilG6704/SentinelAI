#!/usr/bin/env python3
"""
Trains the initial Isolation Forest Anomaly Detection model using the
processed SMD dataset, logging the results to MLflow.
"""
import sys
from pathlib import Path
import pandas as pd

# Add the backend and ai-engine dirs to sys.path so we can import internal modules
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root / "ai-engine"))
sys.path.append(str(project_root / "backend"))

from anomaly_detection.isolation_forest import IsolationForestDetector
from anomaly_detection.trainer import AnomalyTrainer

def main():
    dataset_path = project_root / "datasets" / "processed" / "smd" / "machine-1-1.csv"
    
    if not dataset_path.exists():
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please run scripts/fetch_smd_dataset.py first.")
        sys.exit(1)
        
    print(f"Loading dataset from {dataset_path} ...")
    df = pd.read_csv(dataset_path)
    
    # Drop timestamp for training
    if "timestamp" in df.columns:
        X = df.drop(columns=["timestamp"])
    else:
        X = df
        
    print(f"Dataset loaded. Shape: {X.shape}")
    
    detector = IsolationForestDetector(n_estimators=100, contamination=0.01)
    
    model_dir = project_root / "ai-engine" / "models" / "anomaly_detection"
    
    trainer = AnomalyTrainer(
        detector=detector,
        model_dir=model_dir
    )
    
    print("Starting training via AnomalyTrainer...")
    result = trainer.train(
        X=X,
        dataset_version="machine-1-1-synthetic",
        feature_version="v1",
        hyperparameters={"n_estimators": 100, "contamination": 0.01}
    )
    
    print("\n--- Training Complete ---")
    print(f"Model Name: {result['model_name']}")
    print(f"Training Time: {result['training_time_seconds']:.2f} seconds")
    print(f"Model saved to: {result['model_path']}")
    print(f"MLflow Run ID: {result['run_id']}")

if __name__ == "__main__":
    main()
