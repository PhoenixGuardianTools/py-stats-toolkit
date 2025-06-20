'''
=====================================================================
File : test_descriptives.py
=====================================================================
version : 1.0.0
release : 15/06/2025
author : Phoenix Project
contact : contact@phonxproject.onmicrosoft.fr
license : MIT
=====================================================================
Copyright (c) 2025, Phoenix Project
All rights reserved.

Description du module test_descriptives.py

tags : module, stats
=====================================================================
Ce module Description du module test_descriptives.py

tags : module, stats
=====================================================================
'''

# Imports spécifiques au module
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

# Imports de la base
from py_stats_toolkit.Abstracts.AbstractClassBase import StatisticalModule

class TestMoyenneGlissante(StatisticalModule):
    """
    Classe TestMoyenneGlissante
    
    Attributes:
        data, parameters, results
    """
    
    def __init__(self):
        """
        Initialise TestMoyenneGlissante.
        """
        super().__init__()
        pass
    
    def configure(self, **kwargs) -> None:
        """
        Configure les paramètres de TestMoyenneGlissante.
        
        Args:
            **kwargs: Paramètres de configuration
        """
        pass
    
    def process(self, data: Union[pd.DataFrame, pd.Series], **kwargs) -> Dict[str, Any]:
        """
        Exécute le flux de travail d'analyse.
        
        Args:
            data (Union[pd.DataFrame, pd.Series]): Données à analyser
            **kwargs: Arguments additionnels
            
        Returns:
            Dict[str, Any]: Résultats de l'analyse
        """
        pass 

import unittest
import numpy as np
import pandas as pd
from py_stats_toolkit.stats.descriptives.basic_stats import BasicStatistics

class TestMoyenneGlissante(unittest.TestCase):
    def setUp(self):
        self.stats = BasicStatistics()
        
        # Données de test pour la moyenne glissante
        self.data = pd.DataFrame({
            'valeur': np.random.normal(0, 1, 100)
        })
    
    def test_moyenne_glissante(self):
        """Test de la moyenne glissante."""
        result = self.stats.process(
            self.data,
            method="moyenne_glissante",
            window=5,
            value_col='valeur'
        )
        
        self.assertIn('Méthode', result)
        self.assertIn('Résultats', result)
        self.assertEqual(result['Méthode'], 'Moyenne glissante')
        self.assertEqual(len(result['Résultats']), 96)  # 100 - 5 + 1
    
    def test_invalid_method(self):
        """Test avec une méthode invalide."""
        with self.assertRaises(ValueError):
            self.stats.process(
                self.data,
                method="invalid_method",
                window=5,
                value_col='valeur'
            )
    
    def test_invalid_data_type(self):
        """Test avec un type de données invalide."""
        with self.assertRaises(TypeError):
            self.stats.process(
                "invalid_data",
                method="moyenne_glissante",
                window=5,
                value_col='valeur'
            )
    
    def test_missing_columns(self):
        """Test avec des colonnes manquantes."""
        with self.assertRaises(ValueError):
            self.stats.process(
                self.data,
                method="moyenne_glissante",
                window=5,
                value_col='invalid_col'
            )

class TestDescriptives(unittest.TestCase):
    """
    Tests pour le module de statistiques descriptives.
    """
    
    def setUp(self):
        """
        Configuration initiale pour les tests.
        """
        self.data = pd.DataFrame({
            'x': np.random.normal(0, 1, 100),
            'y': np.random.normal(0, 1, 100)
        })
        self.descriptives = StatisticalModule()
    
    @pytest.fixture
    def sample_data(self):
        """Données d'exemple pour les tests."""
        np.random.seed(42)
        n = 100
        normal_data = np.random.normal(0, 1, n)
        skewed_data = np.random.exponential(1, n)
        
        return pd.DataFrame({
            'normal': normal_data,
            'skewed': skewed_data
        })
    
    def test_central_tendency(self, sample_data):
        """Test des mesures de tendance centrale."""
        stats = DescriptiveStatistics()
        
        # Test moyenne
        mean = stats.mean(sample_data['normal'])
        assert abs(mean - np.mean(sample_data['normal'])) < 1e-10
        
        # Test médiane
        median = stats.median(sample_data['normal'])
        assert abs(median - np.median(sample_data['normal'])) < 1e-10
        
        # Test mode
        mode = stats.mode(sample_data['normal'])
        assert isinstance(mode, (int, float))
        
        # Test moyenne tronquée
        trimmed_mean = stats.trimmed_mean(sample_data['normal'], proportion=0.1)
        assert abs(trimmed_mean - np.mean(sample_data['normal'])) < 1
        
    def test_dispersion(self, sample_data):
        """Test des mesures de dispersion."""
        stats = DescriptiveStatistics()
        
        # Test variance
        var = stats.variance(sample_data['normal'])
        assert abs(var - np.var(sample_data['normal'])) < 1e-10
        
        # Test écart-type
        std = stats.standard_deviation(sample_data['normal'])
        assert abs(std - np.std(sample_data['normal'])) < 1e-10
        
        # Test écart interquartile
        iqr = stats.interquartile_range(sample_data['normal'])
        q75, q25 = np.percentile(sample_data['normal'], [75, 25])
        assert abs(iqr - (q75 - q25)) < 1e-10
        
        # Test coefficient de variation
        cv = stats.coefficient_of_variation(sample_data['normal'])
        assert cv > 0
        
    def test_shape(self, sample_data):
        """Test des mesures de forme."""
        stats = DescriptiveStatistics()
        
        # Test asymétrie
        skewness = stats.skewness(sample_data['normal'])
        assert abs(skewness) < 0.5  # Proche de 0 pour une normale
        
        skewness_skewed = stats.skewness(sample_data['skewed'])
        assert skewness_skewed > 0  # Positif pour une distribution asymétrique
        
        # Test aplatissement
        kurtosis = stats.kurtosis(sample_data['normal'])
        assert abs(kurtosis) < 0.5  # Proche de 0 pour une normale
        
        # Test test de normalité
        is_normal = stats.is_normal(sample_data['normal'])
        assert isinstance(is_normal, bool)
        
    def test_quantiles(self, sample_data):
        """Test des quantiles."""
        stats = DescriptiveStatistics()
        
        # Test quartiles
        q1, q2, q3 = stats.quartiles(sample_data['normal'])
        assert q1 < q2 < q3
        
        # Test percentiles
        p90 = stats.percentile(sample_data['normal'], 90)
        assert p90 > np.median(sample_data['normal'])
        
        # Test déciles
        deciles = stats.deciles(sample_data['normal'])
        assert len(deciles) == 9
        assert all(deciles[i] < deciles[i+1] for i in range(len(deciles)-1))
        
    def test_summary(self, sample_data):
        """Test du résumé statistique."""
        stats = DescriptiveStatistics()
        
        # Test résumé complet
        summary = stats.summary(sample_data['normal'])
        assert isinstance(summary, dict)
        assert all(key in summary for key in ['mean', 'std', 'min', 'max', 'quartiles'])
        
        # Test résumé par colonne
        summary_df = stats.summary_by_column(sample_data)
        assert isinstance(summary_df, pd.DataFrame)
        assert all(col in summary_df.columns for col in ['mean', 'std', 'min', 'max'])
        
    def test_data_validation(self, sample_data):
        """Test de la validation des données."""
        stats = DescriptiveStatistics()
        
        # Test avec données manquantes
        data_with_nan = sample_data.copy()
        data_with_nan.iloc[0, 0] = np.nan
        
        with pytest.raises(ValueError):
            stats.mean(data_with_nan['normal'])
            
        # Test avec données non numériques
        data_with_str = sample_data.copy()
        data_with_str.iloc[0, 0] = 'a'
        
        with pytest.raises(ValueError):
            stats.mean(data_with_str['normal'])
            
        # Test avec données vides
        with pytest.raises(ValueError):
            stats.mean(pd.Series([]))
            
    def test_outliers(self, sample_data):
        """Test de la détection des outliers."""
        stats = DescriptiveStatistics()
        
        # Test détection par IQR
        outliers = stats.detect_outliers_iqr(sample_data['normal'])
        assert isinstance(outliers, pd.Series)
        assert outliers.dtype == bool
        
        # Test détection par Z-score
        outliers = stats.detect_outliers_zscore(sample_data['normal'])
        assert isinstance(outliers, pd.Series)
        assert outliers.dtype == bool
        
        # Test détection par MAD
        outliers = stats.detect_outliers_mad(sample_data['normal'])
        assert isinstance(outliers, pd.Series)
        assert outliers.dtype == bool

if __name__ == '__main__':
    unittest.main() 