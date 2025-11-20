from src.logger import get_logger
from src.custom_exception import CustomException
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from config.path_config import *
from config.model_params import *
from utils.common_functions import read_yaml,load_data

if __name__ == "__main__":

    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()

    trainer = ModelTraining(PROCESSED_TRAIN_FILE_PATH, PROCESSED_TEST_FILE_PATH, MODEL_OUTPUT_PATH)
    trainer.run()