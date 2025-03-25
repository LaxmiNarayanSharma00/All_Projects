import os
from src.datascience import logger
import urllib.request as request
import zipfile
from src.datascience.entity.config_entity import DataIngestionConfig
class Dataingestion:
    def __init__(self,config:DataIngestionConfig):
        self.config=config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename,headers=request.urlretrieve(
                url=self.config.source_url,
                filename=self.config.local_data_file

            )   
            logger.info(f'{filename} downloded with info {headers}')
        
        else:
            logger.info(f'file already exists')

    def extract_zip_file(self):
        unzip_path=self.config.unzip_dir
        os.makedirs(unzip_path,exist_ok=True)

        with zipfile.ZipFile(self.config.local_data_file,'r') as zip_file:
            zip_file.extractall(unzip_path)
