from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_validation import DataValidation

from Network_Security.components.data_transformation import DataTransformationConfig , DataTransformation

from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

from Network_Security.entity.config_entity import DataIngestionConfig , DataValidationConfig ,TrainingPipelineConfig
import os, sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Inittated Data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation completed")
        print(dataingestionartifact)
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        datavalidation = DataValidation(dataingestionartifact , data_validation_config)
        logging.info("Initiate the data validation")
        data_validation_artifact = datavalidation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info("Data transformation started")
        datatransformation = DataTransformation(data_validation_artifact , data_transformation_config)
        datatransformationartifact = datatransformation.initiate_data_transformation()
        print(datatransformationartifact)
        logging.info("Data transformation completed")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)