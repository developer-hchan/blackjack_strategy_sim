# pip install --upgrade setuptools[core]

from setuptools import setup, find_packages

setup( 
    
    name='blackjack_strategy_sim', 
    version='1.0',
    packages=find_packages()
    
    )