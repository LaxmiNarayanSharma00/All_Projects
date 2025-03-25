from src.datascience import logger
from src.datascience.pipeline.step1_data_ingestion import DataIngestionTrainingPipeline
from src.datascience.pipeline.step2_data_validation import DATA_VALIDATION_TRAINING_PIPELINE
from src.datascience.pipeline.step3_data_transformation import DATA_TRANSFORMATION_TRAINING_PIPELINE
from src.datascience.pipeline.step4_model_training import MODEEL_TRAINING_PIPELINE
from src.datascience.pipeline.step5_model_evaluation import MODEEL_EVALUATION_PIPELINE
logger.info('weelcome to my logger')

STAGE_NAME='DATA_INGESTION_STAGE'

# if __name__=='__main__':
try:
          logger.info(f'<<<<<<<<<<<< stage {STAGE_NAME} started<<<<<<<<<')
          obj=DataIngestionTrainingPipeline()
          obj.initiate_data_ingestion()
          logger.info(f'>>>>>>>>>>stage {STAGE_NAME}  completed >>>>>>>>>>>>>')
except Exception as e:
           logger.exception(e)    
           raise e


STAGE_NAME='DATA_VALIDATION_STAGE'

# if __name__=='__main__':
try:
          logger.info(f'<<<<<<<<<<<< stage {STAGE_NAME} started<<<<<<<<<')
          obj=DATA_VALIDATION_TRAINING_PIPELINE()
          obj.initiate_datavalidation()
          logger.info(f'>>>>>>>>>>stage {STAGE_NAME}  completed >>>>>>>>>>>>>')
except Exception as e:
           logger.exception(e)    
           raise e

STAGE_NAME='DATA_TRANSFORMATION_STAGE'
try:
          logger.info(f'<<<<<<<<<<<< stage {STAGE_NAME} started<<<<<<<<<')
          obj=DATA_TRANSFORMATION_TRAINING_PIPELINE()
          obj.initiate_datatransformation()
          logger.info(f'>>>>>>>>>>stage {STAGE_NAME}  completed >>>>>>>>>>>>>')
except Exception as e:
           logger.exception(e)    
           raise e

STAGE_NAME='MODEL TRAINING STAGE'
try:
          logger.info(f'<<<<<<<<<<<< stage {STAGE_NAME} started<<<<<<<<<')
          obj=MODEEL_TRAINING_PIPELINE()
          obj.initiate_model_training()
          logger.info(f'>>>>>>>>>>stage {STAGE_NAME}  completed >>>>>>>>>>>>>')
except Exception as e:
           logger.exception(e)    
           raise e


STAGE_NAME='MODEL EVALUATION STAGE'
try:
          logger.info(f'<<<<<<<<<<<< stage {STAGE_NAME} started<<<<<<<<<')
          obj=MODEEL_EVALUATION_PIPELINE()
          obj.initiate_model_evaluation()
          logger.info(f'>>>>>>>>>>stage {STAGE_NAME}  completed >>>>>>>>>>>>>')
except Exception as e:
           logger.exception(e)    
           raise e