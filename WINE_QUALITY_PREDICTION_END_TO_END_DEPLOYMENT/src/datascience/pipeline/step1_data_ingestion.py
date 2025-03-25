from src.datascience.config.configuration import ConfigManager
from src.datascience.components.data_ingestion import Dataingestion
from src.datascience import logger


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    def initiate_data_ingestion(self):
        
            config=ConfigManager()
            get_data_ingestion_config=config.get_data_ingestion_config()
            dataingestion=Dataingestion(get_data_ingestion_config)
            dataingestion.download_file()
            dataingestion.extract_zip_file()
        
