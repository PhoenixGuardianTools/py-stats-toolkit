import numpy as np
import pandas as pd
from ..core.AbstractClassBase import TimeSeriesModule
from ...utils.parallel import ParallelProcessor, BatchProcessor

class TimeSeriesAnalyzer(TimeSeriesModule):
    """Module pour l'analyse de séries temporelles."""
    
    def __init__(self, n_jobs: int = -1, batch_size: int = 1000):
        super().__init__()
        self.parallel_processor = ParallelProcessor(n_jobs=n_jobs)
        self.batch_processor = BatchProcessor(batch_size=batch_size)
    
    def process(self, data, timestamps=None, **kwargs):
        """
        Analyse une série temporelle.
        
        Args:
            data: Données d'entrée (numpy array ou pandas Series)
            timestamps: Timestamps pour les données
            **kwargs: Arguments additionnels
            
        Returns:
            DataFrame avec les analyses
        """
        self.validate_data(data)
        
        if timestamps is not None:
            self.set_timestamps(timestamps)
        
        if isinstance(data, pd.Series):
            series = data
        else:
            series = pd.Series(data, index=self.timestamps)
        
        # Calcul des statistiques de base
        stats = {
            'Moyenne': series.mean(),
            'Écart-type': series.std(),
            'Minimum': series.min(),
            'Maximum': series.max(),
            'Médiane': series.median()
        }
        
        # Détection des tendances
        if len(series) > 1:
            x = np.arange(len(series))
            slope, intercept = np.polyfit(x, series.values, 1)
            stats['Pente'] = slope
            stats['Intercept'] = intercept
        
        # Détection des cycles
        if len(series) > 2:
            fft = np.fft.fft(series.values)
            freqs = np.fft.fftfreq(len(series))
            main_freq_idx = np.argmax(np.abs(fft[1:len(fft)//2])) + 1
            stats['Fréquence Principale'] = freqs[main_freq_idx]
            stats['Période Principale'] = 1/freqs[main_freq_idx] if freqs[main_freq_idx] != 0 else np.inf
        
        self.result = pd.Series(stats)
        return self.result
    
    def get_trend(self, data=None):
        """
        Calcule la tendance linéaire.
        
        Args:
            data: Données optionnelles (utilise self.data si None)
            
        Returns:
            Tuple (pente, intercept)
        """
        if data is None:
            data = self.data
        
        if isinstance(data, pd.Series):
            series = data
        else:
            series = pd.Series(data)
        
        x = np.arange(len(series))
        return np.polyfit(x, series.values, 1)
    
    def get_seasonality(self, data=None, period=None):
        """
        Détecte la saisonnalité.
        
        Args:
            data: Données optionnelles
            period: Période attendue (optionnelle)
            
        Returns:
            Période détectée
        """
        if data is None:
            data = self.data
        
        if isinstance(data, pd.Series):
            series = data
        else:
            series = pd.Series(data)
        
        # Calcul de l'autocorrélation
        acf = pd.Series(series).autocorr()
        
        if period is not None:
            return period
        
        # Détection automatique de la période
        fft = np.fft.fft(series.values)
        freqs = np.fft.fftfreq(len(series))
        main_freq_idx = np.argmax(np.abs(fft[1:len(fft)//2])) + 1
        return 1/freqs[main_freq_idx] if freqs[main_freq_idx] != 0 else np.inf 