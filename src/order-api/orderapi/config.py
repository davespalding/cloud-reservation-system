from .utils import read_yaml


class Config:
    """Config singleton class"""
    _instance = None
    _config_data = None

    def __new__(cls, file_path=None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            if file_path is not None:
                cls._load_config(file_path)
        return cls._instance

    @classmethod
    def _load_config(cls, file_path):
        cls._config_data = read_yaml(file_path)

    @classmethod
    def get_config(cls):
        if cls._config_data is None:
            raise Exception('Configuration not loaded.')
        return cls._config_data


def construct_db_string():
    conf = Config.get_config()['db']
    dbstr_template = 'postgresql://{}:{}@{}:{}/{}'
    dbstr = dbstr_template.format(conf['user'], conf['passw'], conf['addr'],
                                  conf['port'], conf['db'])

    return dbstr
