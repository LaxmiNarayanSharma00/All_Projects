from src.datascience.constants import *
from src.datascience.entity.config_entity import (DataIngestionConfig,Datavalidationconfig,
                                                  Datatransformation_config,Datatrainer_config,model_evaluation_config)
from src.datascience.utils.common import read_yml,create_directories
class ConfigManager:
    def __init__(self,config_file_path=CONFIG_FILE_PATH,params_file_path=PARAMS_FILE_PATH,SCHEMA_FILE_PATH=SCHEMA_FILE_PATH):
        self.config=read_yml(config_file_path)
        self.params=read_yml(params_file_path)
        self.schema=read_yml(SCHEMA_FILE_PATH)

        create_directories([self.config.artifacts_roots])

    def get_data_ingestion_config(self)-> DataIngestionConfig:
        config=self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config=DataIngestionConfig(
                root_dir=config.root_dir,
                source_url=config.source_url,
                local_data_file=config.local_data_file,
                unzip_dir=config.unzip_dir
            
        )

        return data_ingestion_config
    
    def get_data_validation_config(self)-> Datavalidationconfig:
        config=self.config.data_validation
        schema=self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config=Datavalidationconfig(
                root_dir=config.root_dir,
                STATUS_FILE=config.STATUS_FILE,
                unzip_data_dir=config.unzip_data_dir,
                all_schema=schema
        )

        return data_validation_config
    def get_data_transformation_config(self)-> Datatransformation_config:
        config=self.config.data_transformation
        
        create_directories([config.root_dir])

        data_validation_config=Datatransformation_config(
                root_dir=config.root_dir,
                data_path=config.data_path
        )

        return data_validation_config

    def get_data_trainer_config(self)->Datatrainer_config:
        config=self.config.data_trainer
        schema_col=self.schema.TARGET_COLUMNS
        params=self.params.ELASTIC_NET
        create_directories([config.root_dir])

        data_trainer_config=Datatrainer_config(
                root_dir=config.root_dir ,
                train_data= config.train_path,
                test_data= config.test_path,
                model_name= config.model_name,
                alpha=params.l1_ratio,
                l1_ratio=params.alpha,
                target_col=schema_col.NAME          
        )   

        return data_trainer_config
    

    def get_model_evaluation_config(self)->model_evaluation_config:
        config=self.config.model_evaluation
        params=self.params.ELASTIC_NET
        schema=self.schema.TARGET_COLUMNS
        create_directories([config.root_dir])

        evaluation_config=model_evaluation_config(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            model_path=config.model_path,
            metric_file_path=config.metric_file_path,
            all_params=params,
            target_column=schema.NAME
        )

        return evaluation_config
            



        
