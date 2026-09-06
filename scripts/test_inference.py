#!/usr/bin/env python3
"""
Tests the trained Isolation Forest Anomaly Detection model
by passing it normal and anomalous data and printing the predictions.
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root / "ai-engine"))
sys.path.append(str(project_root / "backend"))

from anomaly_detection.isolation_forest import IsolationForestDetector
from anomaly_detection.inference import InferenceEngine

def main():
    model_path = project_root / "ai-engine" / "models" / "anomaly_detection" / "IsolationForestDetector.model"
    
    if not model_path.exists():
        print(f"Error: Model not found at {model_path}")
        print("Please run scripts/train_anomaly_detector.py first.")
        sys.exit(1)
        
    print(f"Loading model from {model_path}...")
    detector = IsolationForestDetector()
    detector.load(model_path)
    
    engine = InferenceEngine(detector=detector)
    
    print("\n--- Generating Test Data ---")
    
    # 1. Generate normal data (similar to training: mean=0.5, scale=0.1)
    np.random.seed(99)
    normal_data = np.random.normal(loc=0.5, scale=0.1, size=(2, 38))
    
    # 2. Generate anomalous data (spike: mean=1.5, scale=0.2)
    anomalous_data = np.random.normal(loc=1.5, scale=0.2, size=(2, 38))
    
    # Combine them
    test_X = pd.DataFrame(np.vstack([normal_data, anomalous_data]))
    
    print("Running inference...")
    results = engine.predict(test_X)
    
    print("\n--- Inference Results ---")
    for i, res in enumerate(results):
        data_type = "Normal Sample" if i < 2 else "Anomalous Sample"
        print(f"Test case {i+1} ({data_type}):")
        print(f"  Prediction: {res['status']}")
        print(f"  Confidence: {res['confidence']:.2f}")
        print(f"  Score:      {res['anomaly_score']:.2f}")
        print("-" * 30)

if __name__ == "__main__":
    main()
