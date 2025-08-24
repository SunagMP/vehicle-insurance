import logging
import os
import yaml

def create_logger(name:str):
    logger = logging.getLogger(name)
    logger.setLevel("DEBUG")

    console_handler = logging.StreamHandler()
    console_handler.setLevel('DEBUG')

    os.makedirs('logs', exist_ok=True)
    with open(f"./logs/{name}.log", 'w') as f:
        f.write(f"This file contains all logs related to {name}\n")

    file_handler = logging.FileHandler(f'logs/{name}.log')
    file_handler.setLevel('DEBUG')

    formate = logging.Formatter("%(asctime)s %(name)s %(message)s %(levelname)s")
    console_handler.setFormatter(formate)
    file_handler.setFormatter(formate)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def load_all_params(component:str):
    with open('params.yaml', 'r') as f:
        all_params = yaml.safe_load(f)
    return all_params[component]
