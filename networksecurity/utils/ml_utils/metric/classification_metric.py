from networksecurity.entity.artifacts_entity import ClassificationMetricArtifacts
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score
import sys


def get_classification_score(y_true,y_pred)->ClassificationMetricArtifacts:
    try:
        classification_metric=ClassificationMetricArtifacts()
        classification_metric.f1_score=f1_score(y_true,y_pred)
        classification_metric.precision_score=precision_score(y_true,y_pred)
        classification_metric.recall_score=recall_score(y_true,y_pred)

        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)