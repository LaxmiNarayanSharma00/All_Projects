import pandas as pd
import os
from src.datascience import logger
from sklearn.linear_model import ElasticNet
import joblib
from src.datascience.entity.config_entity import Datatrainer_config

class MODEL_TRAINER:
    def __init__(self,config:Datatrainer_config):
        self.config=config

    def model_training(self):
        train_data=pd.read_csv(self.config.train_data)
        test_data=pd.read_csv(self.config.test_data)

        x_train=train_data.drop(columns=self.config.target_col)
        x_test=test_data.drop(columns=self.config.target_col)

        y_train=train_data[[self.config.target_col]]
        y_test=test_data[[self.config.target_col]]

        model=ElasticNet(l1_ratio=self.config.l1_ratio,alpha=self.config.alpha,random_state=42)
        model.fit(x_train,y_train)

        joblib.dump(model,os.path.join(self.config.root_dir,self.config.model_name))


        
