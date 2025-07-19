import os,sys
import yaml
import numpy as np
import pickle

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.model_selection import GridSearchCV
# FIX: Import a proper classification metric utility
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score


def read_yaml_file(file_path: str)-> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path: str, content: object, replace: bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def save_numpy_array_data(file_path:str, array:np.array):
    # Save numpy array data to the given file path
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


#For saving the pickel file
def save_object(file_path:str, obj: object)->None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info('Exited the save_object method of MainUtils class')
    except Exception as e:
        raise NetworkSecurityException(e,sys)


#Read a pkl file
def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not present")
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_numpy_array(file_path:str)->np.array:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    """
    This function evaluates multiple models using GridSearchCV and returns a report
    of their performance along with the dictionary of best-fitted models.
    """
    try:
        report = {}

        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            para = param[model_name]

            # Use GridSearchCV for hyperparameter tuning
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            # Update the model in the dictionary with the best fitted estimator
            models[model_name] = gs.best_estimator_

            # Predict on the test set
            y_test_pred = models[model_name].predict(X_test)

            test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            report[model_name] = test_metric.f1_score

        return report, models

    except Exception as e:
        raise NetworkSecurityException(e, sys)
