import sys , os
import numpy as np , pandas as pd 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from Network_Security.constants.training_pipeline import TARGET_COLUMN , DATA_TRANSFORMATION_IMPUTER_PARAMS
from Network_Security.entity.artifact_entity import(
    DataTransformationArtifact , DataValidationArtifact
)

from Network_Security.entity.config_entity import DataTransformationConfig
from Network_Security.exception.exception  import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.utils.main_utils.utils import save_numpy_array_data , save_object

class DataTransformation:
    def __init__(self , data_validation_artifact:DataValidationArtifact , data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config 
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_data_transformer_object(cls)-> Pipeline:
        """ 
        It initializes a KNN_Imputer with params in training_pipeline.py and returns a Pipeline object with the KNN imputer as the first step.
        """
        logging.info("entered get_data_transformer_object method of transformation class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Initialized KNN imputer")
            processor:Pipeline = Pipeline([("imputer",imputer)])
            
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("entered initiate data transformation method od data transforamtion class")
        try:
            logging.info("Started Data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ##training df
            input_feature_train_df = train_df.drop(columns = [TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0) # Binary classification
            
            ##testing df
            input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0) # Binary classification
            
            preprocessor = self.get_data_transformer_object()

            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.column_stack((transformed_input_train_feature, target_feature_train_df.to_numpy()))
            test_arr = np.column_stack((transformed_input_test_feature, target_feature_test_df.to_numpy()))
            
            #save numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path , array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path , array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path , preprocessor_object)            
            
            save_object("final_models/preprocessor.pkl" , preprocessor_object)
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )
            
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)