from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifacts

import os
import sys
import pymongo
from typing import List
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


from dotenv import load_dotenv
load_dotenv()

MONGO_URL=os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def export_data_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name

            mongo_client=pymongo.MongoClient(MONGO_URL)
            logging.info("Data collection is extrated from mongo db atlas")
            collection=mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df=df.drop(columns="_id")

            df.replace({"na":np.nan},inplace=True)
            logging.info("Data is converted into data frame")

            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:

            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("feature store directory created.")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logging.info("data is saved into featured stored path.")
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_data,test_data=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            

            logging.info("Performed Trained Test Split on dataframe")

            dir_path=os.path.dirname(self.data_ingestion_config.test_file_path)

            os.makedirs(dir_path,exist_ok=True)

            logging.info("Exporting train and test data")

            train_data.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_data.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)

            logging.info("Exported Train and Test Data")


        except Exception as e:
            raise NetworkSecurityException(e,sys) from None
        

    def initiate_data_ingestion(self):
        try:
            logging.info("Entered to DataIngestion class in data_ingestion.py")
            dataframe=self.export_data_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)

            DataIngestionArtifacts(train_data_path=self.data_ingestion_config.training_file_path,
                                                            test_data_path=self.data_ingestion_config.test_file_path)

        except Exception as e:
            raise NetworkSecurityException(e,sys) from None


        

