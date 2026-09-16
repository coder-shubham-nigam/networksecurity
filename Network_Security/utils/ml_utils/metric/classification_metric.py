from Network_Security.entity.artifact_entity import ClassificationMetricArtifact
from Network_Security.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score , precision_score , recall_score
import sys

def get_classification_score(ytrue , ypred) -> ClassificationMetricArtifact :
    try: 
        model_f1_score = f1_score(ytrue , ypred)
        model_recall_score = recall_score(ytrue , ypred)
        model_precision_score = precision_score(ytrue , ypred)
        
        classification_metric = ClassificationMetricArtifact(
            f1_score = model_f1_score ,
            precision_score = model_precision_score , 
            recall_score = model_recall_score
        )
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e