import os,sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression,Lasso,Ridge,ElasticNet
from sklearn.ensemble import RandomForestRegressor
from dataclasses import dataclass
from src.utils import save_object,evaluate_models


@dataclass
class ModelTrainerConfig:
    model_file_path:str = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config= ModelTrainerConfig

    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info('initiate model trainer')

            x_train,y_train,x_test,y_test =(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
                'linear_regression':LinearRegression(),
                'lasso':Lasso(),
                'ridge':Ridge(),
                'elasticnet':ElasticNet(),
                'random_forest':RandomForestRegressor()
            }

            logging.info('start model training')

            report = evaluate_models(x_train,y_train,x_test,y_test,models)

            print(report)
            logging.info(f'report : {report}')

            best_score = max(sorted(report.values()))
            best_model_name = list(report.keys())[list(report.values()).index(best_score)]

            best_model = models[best_model_name]

            print(f'best model found {best_model_name} with accuracy of {best_score}')
            logging.info(f'best model found {best_model_name} with accuracy of {best_score}')

            save_object(
                self.model_trainer_config.model_file_path,best_model
            )
        except Exception as e:
            raise CustomException(e,sys)

