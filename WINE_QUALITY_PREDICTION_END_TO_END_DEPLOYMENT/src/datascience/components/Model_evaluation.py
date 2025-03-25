import pandas as pd
import numpy as np
import mlflow,os
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
import joblib
from urllib.parse import urlparse
from  src.datascience.entity.config_entity import model_evaluation_config
from src.datascience.utils.common import save_json
from pathlib import Path

os.environ['MLFLOW_TRACKING_URI']='https://researchanalystforapurpose:8e0daaa2b9f63126713e4d435ab226f1e1a19c0c@dagshub.com/researchanalystforapurpose/FACIAL_BIOMETRIC_ATTENDENCE_SYSTEM.mlflow'
os.environ['MLFLOW_TRACKING_USERNAME']='researchanalystforapurpose'
os.environ['MLFLOW_TRACKING_PASSWORD']='8e0daaa2b9f63126713e4d435ab226f1e1a19c0c '

class model_evaluation:
    def __init__(self,config=model_evaluation_config):
        self.config=config

    def eval_metrcis(self,actual,pred):
        r2=r2_score(actual,pred)
        mae=mean_absolute_error(actual,pred)
        root_mean_squared_error=np.sqrt(mean_squared_error(actual,pred))

        return r2,mae,root_mean_squared_error    
    
    def log_into_mlflow(self):
        test_data=pd.read_csv(self.config.test_data_path)

        model=joblib.load(self.config.model_path)
        
        test_x=test_data.drop(columns=self.config.target_column)
        
        test_y=test_data[[self.config.target_column]]
        
    
        mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
        tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme

        mlflow.set_experiment("MY_ELASTIC_NET_EXPERIMENT")
        

        if mlflow.active_run():
            mlflow.end_run()



        with mlflow.start_run():
            pred=model.predict(test_x)
            (r2,mae,rmse)=self.eval_metrcis(test_y,pred)
           
            scores={'rmse':rmse,'mae':mae,'r2_score':r2}
            save_json(path=Path(self.config.metric_file_path),data=scores)

            mlflow.log_params(self.config.all_params)
            mlflow.log_metric('rmse',rmse)
            mlflow.log_metric('r2_score',r2)
            mlflow.log_metric('mae',mae)
       

            if tracking_url_type_store!= 'file':
                mlflow.sklearn.log_model(model,'model',registered_model_name='ELASTIC_NET')

            else:
                mlflow.sklearn.log_model(model,'model')    