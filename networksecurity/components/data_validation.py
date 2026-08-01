from networksecurity.entity.artifacts_entity import DataIngestionArtifacts,DataValidationArtifacts
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.utils import read_yaml,write_yaml_file
from networksecurity.logging.logger import logging
from pandas.api.types import is_numeric_dtype

from scipy.stats import ks_2samp
import pandas as pd
import sys
import os


class DataValidation:
    def __init__(self,data_ingestion_artifacts:DataIngestionArtifacts,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifacts=data_ingestion_artifacts
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None


    def validate_no_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config['columns'])

            logging.info(f"Required No of columns : {number_of_columns}")
            logging.info(f"Data has columns {len(dataframe.columns)}")

            if len(dataframe.columns) == number_of_columns:
                return True

            return False

        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def validate_numeric_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            numeric_columns_schema=self._schema_config['numrical_columns']
            numeric_columns_data=[col for col in dataframe.columns if is_numeric_dtype(dataframe[col])]

            if set(numeric_columns_schema) == set(numeric_columns_data):
                return True

            return False

        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def detect_dataset_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for col in base_df.columns:
                d1=base_df[col]
                d2=current_df[col]

                is_sample_dist=ks_2samp(d1,d2)
                if is_sample_dist.pvalue>=threshold:
                    is_found=False
                else :
                    is_found=True
                    status=False
                report.update({col:{
                        "p_value":float(is_sample_dist.pvalue),
                        "drift_status":is_found
                    }})
            drift_file_path=self.data_validation_config.data_drift_report_file_path

            dir_name=os.path.dirname(drift_file_path)
            os.makedirs(dir_name,exist_ok=True)

            write_yaml_file(drift_file_path,report)
            return status

        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

        
    def initiate_data_validation(self)->DataValidationArtifacts:
        try:
            logging.info("Entered into initiate_data_validation method in DataValidation class.")
            train_file_path=self.data_ingestion_artifacts.train_data_path
            test_file_path=self.data_ingestion_artifacts.test_data_path

            train_data=pd.read_csv(train_file_path)
            test_data=pd.read_csv(test_file_path)

            logging.info("Extracted Training and Testing Data")

            train_status=self.validate_no_of_columns(train_data)

            test_status=self.validate_no_of_columns(test_data)

            status= (train_status and test_status)
            if not status:
                    error_message="Train or Test DataFrame does not contain all columns."
                    logging.info("Train or Test DataFrame does not contain all columns.")
                    raise NetworkSecurityException(error_message,sys) from None

            train_status=self.validate_numeric_columns(train_data)
            test_status=self.validate_numeric_columns(test_data)

            status= (train_status and test_status)

            if not status:
                    error_message="Train or Test DataFrame does not contain all Numeric Columns."
                    logging.info("Train or Test DataFrame does not contain all Numeric Columns.")
                    raise NetworkSecurityException(error_message,sys) from None


            status=self.detect_dataset_drift(train_data,test_data)

            if not status:
                dir_name=os.path.dirname(self.data_validation_config.invalid_train_file_path)
            else :
                dir_name=os.path.dirname(self.data_validation_config.valid_test_file_path)

            os.makedirs(dir_name,exist_ok=True)

            if not status:
                train_data.to_csv(
                    self.data_validation_config.invalid_train_file_path,
                    index=False,
                    header=True
                )

                test_data.to_csv(
                    self.data_validation_config.invalid_test_file_path,
                    index=False,
                    header=True
                )
            else :
                train_data.to_csv(
                                    self.data_validation_config.valid_train_file_path,
                                    index=False,
                                    header=True
                                )
                
                test_data.to_csv(
                                    self.data_validation_config.valid_test_file_path,
                                    index=False,
                                    header=True
                                )

            data_validation_artifacts=DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.data_drift_report_file_path
            )

            return data_validation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys) from None