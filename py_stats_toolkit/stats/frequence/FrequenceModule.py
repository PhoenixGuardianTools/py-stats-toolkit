'''
=====================================================================
File : FrequenceModule.py
=====================================================================
version : 1.0.0
release : 15/06/2025
author : Phoenix Project
contact : contact@phonxproject.onmicrosoft.fr
license : MIT
=====================================================================
Copyright (c) 2025, Phoenix Project
All rights reserved.

Description du module FrequenceModule.py

tags : module, stats
=====================================================================
Ce module Description du module FrequenceModule.py

tags : module, stats
=====================================================================
'''

# Imports spécifiques au module
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

# Imports de la base
from capsules.BaseCapsule import BaseCapsule

class FrequenceModule(BaseCapsule):
    """
    Classe FrequenceModule
    
    Attributes:
        data, parameters, results
    """
    
    def __init__(self):
        """
        Initialise FrequenceModule.
        """
        super().__init__()
        pass
    
    def configure(self, **kwargs) -> None:
        """
        Configure les paramètres de FrequenceModule.
        
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

import numpy as np
import pandas as pd
from core.AbstractClassBase import StatisticalModule
from utils.parallel import ParallelProcessor

class FrequenceModule(StatisticalModule):
    """Module pour l'analyse de fréquence."""
    
    def __init__(self, n_jobs: int = -1):
        super().__init__()
        self.parallel_processor = ParallelProcessor(n_jobs=n_jobs)
    
    def process(self, data, normalize=False, **kwargs):
        """
        Calcule les fréquences des valeurs.
        
        Args:
            data: Données d'entrée (numpy array ou pandas Series)
            normalize: Si True, retourne les fréquences relatives
            **kwargs: Arguments additionnels
            
        Returns:
            DataFrame avec les fréquences
        """
        self.validate_data(data)
        
        if isinstance(data, pd.Series):
            series = data
        else:
            series = pd.Series(data)
        
        # Calcul des fréquences
        freq = series.value_counts(normalize=normalize)
        cum_freq = freq.cumsum()
        
        # Création du DataFrame de résultats
        self.result = pd.DataFrame({
            'Fréquence': freq,
            'Fréquence Cumulée': cum_freq
        })
        
        if normalize:
            self.result.columns = ['Fréquence Relative', 'Fréquence Relative Cumulée']
        
        return self.result
    
    def get_frequence_absolue(self):
        """Retourne les fréquences absolues."""
        if self.result is None:
            raise ValueError("Exécutez d'abord process()")
        return self.result['Fréquence']
    
    def get_frequence_cumulee(self):
        """Retourne les fréquences cumulées."""
        if self.result is None:
            raise ValueError("Exécutez d'abord process()")
        return self.result['Fréquence Cumulée']
    
    def get_frequence_relative(self):
        """Retourne les fréquences relatives."""
        if self.result is None:
            raise ValueError("Exécutez d'abord process()")
        return self.process(self.data, normalize=True)['Fréquence Relative'] 