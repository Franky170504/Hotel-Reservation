import os 
import sys
import joblib
import pandas as pd
import numpy as np

from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from config.model_params import *
from utils.common_functions import read_yaml,load_data

from lightgbm import LGBMClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, train_path, test_path, model_output_dir, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_dir = model_output_dir
        self.model_output_path = model_output_path

        self.model_params_dict = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from {self.test_path}")
            test_df = load_data(self.test_path)

            X_train= train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']

            X_test= test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']

            logger.info("Data Splitting done")

            return X_train, y_train, X_test, y_test

        except Exception as e:
            logger.error(f"Error during data loading & splitting {e}")
            raise CustomException("Error while data loading & splitting", e)
    
    def training(self, X_train, y_train):
        try:
            logger.info("Model Initialized")

            lgbm_model = LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Hyperparameter tuning started")

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.model_params_dict,
                n_iter=self.random_search_params["n_iter"],
                cv=self.random_search_params["cv"],
                verbose=self.random_search_params["verbose"],
                n_jobs=self.random_search_params["n_jobs"],
                random_state=self.random_search_params["random_state"],
                scoring=self.random_search_params["scoring"]
            )

            random_search.fit(X_train, y_train)

            logger.info("Hyperparameter tuning ended")

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best parameters are {best_params}")

            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error during model training {e}")
            raise CustomException("Error while data training", e)
        
    def model_evaluation(self, model, X_test, y_test):
        try:
            logger.info("Model Evaluation started")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Accuracy score : {accuracy}")
            logger.info(f"Precision score : {precision}")
            logger.info(f"Recall score : {recall}")
            logger.info(f"F1 score : {f1}")

            return{
                "Accuracy score" : accuracy,
                "Precision score" : precision,
                "Recall score" : recall,
                "F1 score" : f1,
            }
        except Exception as e:
            logger.error(f"Error during model evaluatation {e}")
            raise CustomException("Error while data evaluation", e)
        
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok=True)
            model_path = os.path.join(self.model_output_path, "lightgbm.pkl")
            logger.info("Saving the model")

            joblib.dump(model,model_path)

            logger.info(f"Model Saved at {self.model_output_path}")
        
        except Exception as e:
            logger.error(f"Error during model saving {e}")
            raise CustomException("Error while data savng", e)
        
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting model training pipeline")

                logger.info("Starting MLflow")
                logger.info("Logging the training and testing dataset to MLflow")

                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_model = self.training(X_train, y_train)
                metrics = self.model_evaluation(best_model, X_test, y_test)
                self.save_model(best_model)

                logger.info("Logging model into MLflow")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging params and metrics to MLflow")
                mlflow.log_params(best_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model training completed")

        except Exception as e:
            logger.error(f"Error during running model training pipeline {e}")
            raise CustomException("Error while running model training pipeline", e)
                   
if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_FILE_PATH, PROCESSED_TEST_FILE_PATH, MODEL_OUTPUT_DIR, MODEL_OUTPUT_PATH)
    trainer.run()