from src.datascience.config.configuration import ConfigManager
from src.datascience.components.data_validation import Datavalidation
from src.datascience import logger

stage_name='DATA VALIDATION STEP'
class DATA_VALIDATION_TRAINING_PIPELINE:
    def __init__(self):
        pass  
    def initiate_datavalidation(self):
       config=ConfigManager()
       get_data_ingestion_config=config.get_data_validation_config()
       dataingestion=Datavalidation(get_data_ingestion_config)
       dataingestion.validate_all_columns() 
    
