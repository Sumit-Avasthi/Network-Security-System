from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from networksecurity.components.data_ingestion import DataIngestion
import sys

if __name__=="__main__":
    try:
        logging.info("Entered into main.py try block")
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        obj=DataIngestion(data_ingestion_config)
        logging.info("Data Ingestion Started")
        obj.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
    except Exception as e:
        raise NetworkSecurityException(e,sys) from None


