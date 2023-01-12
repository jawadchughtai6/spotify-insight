import os
import logging

# External libraries
import coloredlogs
import dotenv
from peewee import *


class Application:
    """
    App configurations e.g. database connections come here
    """

    def __init__(self, name, load_environment=True, configure_logging=True):
        self.name = name
        self.environment = os.getenv('ENV', 'development')
        self.db_engines = {}

        if load_environment:
            self.load_environment()

        if configure_logging:
            self.configure_logging()

        self.logger = logging.getLogger(__name__)

    def env(self, name, default_value=None):
        return os.getenv(name, default_value)

    def load_environment(self):
        dotenv.load_dotenv(dotenv_path='.env.{}'.format(self.environment))

    def configure_logging(self):
        logging.basicConfig(filename='migrations.log')
        coloredlogs.install(
            level='DEBUG',
            milliseconds=True
        )

    def db_engine(self, db_alias):
        if not db_alias in self.db_engines:
            self.db_engines[db_alias] = PostgresqlDatabase(self.env('DB'),
                                                           user=self.env('DB_USER'),
                                                           password=self.env('DB_PASSWORD'),
                                                           host=self.env('DB_HOST'),
                                                           port=self.env('DB_PORT'))

        return self.db_engines[db_alias]

    def db_session(self, db_alias):
        return self.db_engine(db_alias)

    def run(self, callable, *args):
        self.logger.info('Starting "{}"'.format(self.name))
        callable(*args)
        self.logger.info('Finished "{}"'.format(self.name))
