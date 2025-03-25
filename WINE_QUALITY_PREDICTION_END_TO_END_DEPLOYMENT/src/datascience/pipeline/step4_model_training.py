from src.datascience.config.configuration import ConfigManager
from src.datascience.components.model_trainer import MODEL_TRAINER
from src.datascience import logger
from pathlib import Path

stage_name='MODEL TRAINING STEP'
class MODEEL_TRAINING_PIPELINE:
    def __init__(self):
        pass  
    def initiate_model_training(self):
        confif_manager=ConfigManager()
        config=confif_manager.get_data_trainer_config()
        model_trainer=MODEL_TRAINER(config)    
        model_trainer.model_training()

