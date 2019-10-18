import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "light_sabers_exist")
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class StagingConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False


config_table = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "staging": ProductionConfig,
    "prod": ProductionConfig
}
