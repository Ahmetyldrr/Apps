"""
Simple Modules Package - Basit Modüller Paketi
Bu paket futbol veri sistemi için basit modülleri içerir
"""

__version__ = "1.0.0"
__author__ = "Futbol Veri Sistemi"

# Modülleri dışa aktar
from .database import DatabaseConnection
from .api_fetcher import APIFetcher
from .data_processor import DataProcessor
from .database_writer import DatabaseWriter
from .main_coordinator import MainCoordinator

__all__ = [
    'DatabaseConnection',
    'APIFetcher', 
    'DataProcessor',
    'DatabaseWriter',
    'MainCoordinator'
]
