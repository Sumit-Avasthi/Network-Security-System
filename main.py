from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
import sys

if __name__=="__main__":
    try:
        logging.info("Entered into main.py try block")
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_validation_config=DataValidationConfig(training_pipeline_config)
        obj=DataIngestion(data_ingestion_config)
        logging.info("Data Ingestion Started")
        data_ingestion_artifacts=obj.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        logging.info("Data Validation Started")
        obj2=DataValidation(data_ingestion_artifacts,data_validation_config)
        data_validation_artifacts=obj2.initiate_data_validation()
        print(data_validation_artifacts)
        logging.info("Data Validation Completed")
    except Exception as e:
        raise NetworkSecurityException(e,sys) from None


