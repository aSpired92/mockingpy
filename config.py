import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))

DYNAMIC_NAME = 'dynamic'
DYNAMIC_DIR = os.path.join(MAIN_DIR, DYNAMIC_NAME)

MODELS_NAME = 'models.py'
MODELS_DIR = os.path.join(DYNAMIC_DIR, MODELS_NAME)
