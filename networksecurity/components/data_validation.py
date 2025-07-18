from lib2to3.btm_utils import reduce_tree
from multiprocessing.managers import convert_to_error

from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os,sys



class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self.schema_config)
            logging.info(f"Required Number of Columns:{number_of_columns}")
            logging.info(f"Dataframe has columns:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def validate_numerical_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            expected_numerical_columns = self.schema_config.get('numerical_columns', [])
            missing_columns = []
            wrong_dtype_columns = []

            for col in expected_numerical_columns:
                if col not in dataframe.columns:
                    missing_columns.append(col)
                else:
                    # Check if dtype is numeric
                    if not pd.api.types.is_numeric_dtype(dataframe[col]):
                        wrong_dtype_columns.append(col)

            if missing_columns:
                logging.error(f"Missing numerical columns: {missing_columns}")
                return False

            if wrong_dtype_columns:
                logging.error(f"Columns present but not numeric: {wrong_dtype_columns}")
                return False

            logging.info("All expected numerical columns are present and have numeric dtypes.")
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    'drift_status':is_found
                }})
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            #Create director
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            #Read data from train and test
            train_df=DataValidation.read_data(train_file_path)
            test_df=DataValidation.read_data(test_file_path)

            #VALIDATE NUMBER OF COLUMNS
            status=self.validate_number_of_columns(dataframe=train_df)
            if not status:
                error_message="Train df does not contain all columns.\n"
            status=self.validate_number_of_columns(dataframe=test_df)
            if not status:
                error_message="Test df does not contain all columns.\n"

            if not self.validate_numerical_columns(train_df):
                raise NetworkSecurityException("Train df missing expected numerical columns or wrong dtype.", sys)
            if not self.validate_numerical_columns(test_df):
                raise NetworkSecurityException("Test df missing expected numerical columns or wrong dtype.", sys)

            #Lets check data drift
            status=self.detect_dataset_drift(base_df=train_df, current_df=test_df)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )

            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)





