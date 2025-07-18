from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info('Initiate data ingestion')
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)

        data_validation=DataValidation(dataingestionartifact,datavalidationconfig)
        logging.info('Initiate the data validation')
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info('Data Validation completed')
        print(data_validation_artifact)

        logging.info('Data transformation started')
        datatransformationconfig=DataTransformationConfig(trainingpipelineconfig)
        data_tansformation=DataTransformation(data_validation_artifact, datatransformationconfig)
        data_transformation_artifact=data_tansformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info('Data transformation completed')

        logging.info("Model training started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("Model training completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
