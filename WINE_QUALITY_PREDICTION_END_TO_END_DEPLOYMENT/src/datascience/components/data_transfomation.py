import pandas as pd
import os
from src.datascience import logger
from sklearn.model_selection import train_test_split
from src.datascience.entity.config_entity import Datatransformation_config

class Datatransformation:
    def __init__(self,config:Datatransformation_config):
        self.config=config

    def perform_train_test_split(self):
        data=pd.read_csv(self.config.data_path)
        train,test=train_test_split(data)
        
        train.to_csv(os.path.join(self.config.root_dir,'train.csv'),index=False)
        test.to_csv(os.path.join(self.config.root_dir,'test.csv'),index=False)

        logger.info(f'splitting the data into train and test and data saved in directory {self.config.root_dir}')
        logger.info(train.shape)
        logger.info(test.shape)


