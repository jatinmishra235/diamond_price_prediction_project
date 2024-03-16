import os,sys
from src.exception import CustomException
from src.logger import logging
import pickle
from sklearn.metrics import r2_score



def save_object(filepath,obj):
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(x_train,y_train,x_test,y_test,models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            model_name = list(models.keys())[i]

            model.fit(x_train,y_train)
            y_pred = model.predict(x_test)

            r2 = r2_score(y_test,y_pred)

            report[model_name]=r2

        return report
    except Exception as e:
        raise CustomException(e,sys)

def load_object(filepath):
    try:
        with open(filepath , 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)