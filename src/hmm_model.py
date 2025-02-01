# models/hmm_model.py
"""
This module contains functions to build and configure the Hidden Markov Model (HMM)
for regime detection using the hmmlearn library.
"""

from hmmlearn.hmm import GaussianHMM

def build_hmm_model(n_components=3, covariance_type='full', n_iter=1000, random_state=42):
    """
    Builds and returns a GaussianHMM model configured for regime detection.
    
    Parameters:
        n_components (int): Number of regimes (states) for the HMM.
        covariance_type (str): Type of covariance parameters.
        n_iter (int): Maximum number of iterations for training.
        random_state (int): Seed for the random number generator.
        
    Returns:
        GaussianHMM: Configured HMM model.
    """
    model = GaussianHMM(n_components=n_components, 
                        covariance_type=covariance_type, 
                        n_iter=n_iter, 
                        random_state=random_state)
    return model
