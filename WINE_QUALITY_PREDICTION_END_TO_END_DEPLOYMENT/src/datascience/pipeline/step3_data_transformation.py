from src.datascience.config.configuration import ConfigManager
from src.datascience.components.data_transfomation import Datatransformation
from src.datascience import logger
from pathlib import Path

stage_name='DATA VALIDATION STEP'
class DATA_TRANSFORMATION_TRAINING_PIPELINE:
    def __init__(self):
        pass  
    def initiate_datatransformation(self):
      try:
        with open(Path('artifacts/data_validation/status.txt'),'r') as f:
           status=f.read().split()[-1]   
           if status=='True':
                confif_manager=ConfigManager()
                config=confif_manager.get_data_transformation_config()
                data_transformation=Datatransformation(config)    
                data_transformation.perform_train_test_split()
           else:
              raise Exception('your data schema is not valid')
      except Exception as e:
         print(e)