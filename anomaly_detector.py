# Detecção Anômala com ML (Isolation Forest)

from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(contamination=contamination)

    def treinar(self, dados):
        X = np.array(dados).reshape(-1, 1)
        self.model.fit(X)

    def detectar(self, dados):
        X = np.array(dados).reshape(-1, 1)
        return self.model.predict(X)
