from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from anomaly_detection.base_detector import BaseDetector
from utils.logger import logger


class Autoencoder(nn.Module):
    """
    Simple fully-connected Autoencoder.
    """

    def __init__(
        self,
        input_dim: int,
        latent_dim: int = 16,
    ) -> None:
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),

            nn.Linear(64, 32),
            nn.ReLU(),

            nn.Linear(32, latent_dim),
        )

        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.ReLU(),

            nn.Linear(32, 64),
            nn.ReLU(),

            nn.Linear(64, input_dim),
        )

    def forward(self, x):
        latent = self.encoder(x)
        reconstructed = self.decoder(latent)
        return reconstructed


class AutoencoderDetector(BaseDetector):

    def __init__(
        self,
        latent_dim: int = 16,
        learning_rate: float = 1e-3,
        epochs: int = 30,
        batch_size: int = 128,
        threshold: float | None = None,
        random_seed: int = 42,
    ) -> None:

        self.latent_dim = latent_dim
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size

        self.threshold = threshold

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        torch.manual_seed(random_seed)
        np.random.seed(random_seed)

        self.model = None
        self.loss_fn = nn.MSELoss()

        self.is_trained = False

    @staticmethod
    def _to_numpy(X):

        if isinstance(X, pd.DataFrame):
            return X.to_numpy(dtype=np.float32)

        return np.asarray(X, dtype=np.float32)

    def train(self, X):

        logger.info("Training Autoencoder...")

        X = self._to_numpy(X)

        input_dim = X.shape[1]

        self.model = Autoencoder(
            input_dim=input_dim,
            latent_dim=self.latent_dim,
        ).to(self.device)

        optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=self.learning_rate,
        )

        dataset = TensorDataset(
            torch.tensor(X)
        )

        loader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            shuffle=True,
        )

        self.model.train()

        for epoch in range(self.epochs):

            epoch_loss = 0.0

            for (batch,) in loader:

                batch = batch.to(self.device)

                optimizer.zero_grad()

                reconstructed = self.model(batch)

                loss = self.loss_fn(
                    reconstructed,
                    batch,
                )

                loss.backward()

                optimizer.step()

                epoch_loss += loss.item()

            logger.info(
                f"Epoch {epoch+1}/{self.epochs} "
                f"Loss={epoch_loss/len(loader):.6f}"
            )

        scores = self.anomaly_score(X)

        if self.threshold is None:
            self.threshold = np.percentile(
                scores,
                95,
            )

        self.is_trained = True

        logger.success("Autoencoder training completed.")

    def anomaly_score(self, X):

        if self.model is None:
            raise RuntimeError("Model not trained.")

        X = self._to_numpy(X)

        self.model.eval()

        with torch.no_grad():

            tensor = torch.tensor(
                X,
                device=self.device,
            )

            reconstructed = self.model(tensor)

            errors = torch.mean(
                (tensor - reconstructed) ** 2,
                dim=1,
            )

        return errors.cpu().numpy()

    def predict(self, X):

        scores = self.anomaly_score(X)

        return (
            scores > self.threshold
        ).astype(int)

    def save(self, path):

        if self.model is None:
            raise RuntimeError("Model not trained.")

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        torch.save(
            {
                "state_dict": self.model.state_dict(),
                "threshold": self.threshold,
                "latent_dim": self.latent_dim,
            },
            path,
        )

        logger.success(f"Saved model to {path}")

    def load(self, path):

        checkpoint = torch.load(
            path,
            map_location=self.device,
            weights_only=False,
        )

        latent_dim = checkpoint["latent_dim"]

        state_dict = checkpoint["state_dict"]

        input_dim = (
            state_dict["encoder.0.weight"]
            .shape[1]
        )

        self.model = Autoencoder(
            input_dim=input_dim,
            latent_dim=latent_dim,
        ).to(self.device)

        self.model.load_state_dict(
            state_dict
        )

        self.threshold = checkpoint["threshold"]

        self.is_trained = True

        logger.success(f"Loaded model from {path}")