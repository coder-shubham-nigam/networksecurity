import os,sys
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

from Network_Security.entity.artifact_entity import DataTransformationArtifact , ModelTrainerArtifact
from Network_Security.entity.config_entity import ModelTrainerConfig

from Network_Security.utils.main_utils.utils import save_numpy_array_data , save_object , load_numpy_array_data , load_object , evaluate_models
from Network_Security.utils.ml_utils.metric.classification_metric import get_classification_score
from Network_Security.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
    AdaBoostClassifier , GradientBoostingClassifier , RandomForestClassifier
)

import mlflow
import dagshub
dagshub.init(repo_owner='coder-shubham-nigam', repo_name='networksecurity', mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig , data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def track_mlflow(self , best_model , classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score
            
            mlflow.log_metric("f1_score" , f1_score)
            mlflow.log_metric("precison" , precision_score)
            mlflow.log_metric("recall" , recall_score)
            mlflow.sklearn.log_model(best_model , "model")
    
    
    def train_model(self , xtrain , ytrain , xtest , ytest):
        models = {
            "Random Forest" : RandomForestClassifier(),
            "Decision Tree" : DecisionTreeClassifier() ,
            "Gradient Boosting" : GradientBoostingClassifier(),
            "Logistic Regression" : LogisticRegression() ,
            "AdaBoost" : AdaBoostClassifier()
        }
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,256]
            }   
        }
        
        model_report:dict = evaluate_models(xtrain , ytrain , xtest , ytest , models = models , params = params)
        
        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model = models[best_model_name]
        
        ytrain_pred = best_model.predict(xtrain)
        classification_train_metric = get_classification_score(ytrue= ytrain , ypred= ytrain_pred)
        
        ##track the experiments ml flow
        self.track_mlflow(best_model , classification_train_metric)
        
        ytest_pred = best_model.predict(xtest)
        classification_test_metric = get_classification_score(ytrue=ytest , ypred= ytest_pred)
        
        self.track_mlflow(best_model , classification_test_metric)
        
        preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path , exist_ok=True)
        
        Network_model = NetworkModel(preprocessor=preprocessor , model= best_model)
        save_object(self.model_trainer_config.trained_model_file_path , obj=NetworkModel)
        
        save_object("final_models/model.pkl" , best_model)
        
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path= self.model_trainer_config.trained_model_file_path ,
            train_metric_artifact = classification_train_metric ,
            test_metric_artifact = classification_test_metric
        )
        logging.info("Model trainer artifact: %s", model_trainer_artifact)
        return model_trainer_artifact
        
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            xtrain , ytrain , xtest , ytest = (
                train_arr[: , :-1] ,
                train_arr[: , -1] ,
                test_arr[: , :-1] ,
                test_arr[: , -1]
            )
            
            model = self.train_model(xtrain,ytrain,xtest,ytest)
            return model
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)