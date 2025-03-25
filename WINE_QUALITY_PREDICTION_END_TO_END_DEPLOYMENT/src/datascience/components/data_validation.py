import os
import pandas as pd
from src.datascience import logger
from src.datascience.entity.config_entity import Datavalidationconfig

class Datavalidation:
    def __init__(self,config:Datavalidationconfig):
        self.config=config

    def validate_all_columns(self):
      try:
        validation_status=None  
        data=pd.read_csv(self.config.unzip_data_dir)
        all_col=data.columns
        all_dtypes=data.dtypes.to_dict()
        all_schema=self.config.all_schema

        for col in all_col:
           if col not in all_schema or all_dtypes[col] not in all_schema.values():
              validation_status=False
              with open(self.config.STATUS_FILE,'w') as f:
                 f.write(f'validation status: {validation_status}')

           else:
              validation_status=True
              with open(self.config.STATUS_FILE,'w') as f:
                 f.write(f'validation status: {validation_status}')                   

      except Exception as e:
         raise e  
