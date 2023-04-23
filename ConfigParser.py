import yaml

class Config:
    config = {}

    def __init__(self, filename: str):
        try:
            with open(filename, 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            raise ValueError('Could not read config file')