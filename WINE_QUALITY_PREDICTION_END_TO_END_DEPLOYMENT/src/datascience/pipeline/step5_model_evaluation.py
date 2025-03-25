from src.datascience.config.configuration import ConfigManager
from src.datascience.components.Model_evaluation import model_evaluation
from src.datascience import logger
from pathlib import Path

stage_name='MODEL EVALUATION STEP'
class MODEEL_EVALUATION_PIPELINE:
    def __init__(self):
        pass  
    def initiate_model_evaluation(self):
        confif_manager=ConfigManager()
        config=confif_manager.get_model_evaluation_config()
        model_eval=model_evaluation(config)    
        model_eval.log_into_mlflow()


