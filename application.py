import coloredlogs
import dotenv
import logging
import os

from peewee import PostgresqlDatabase


class Application:
    """
    Provides singleton implementation of App configurations e.g.
    database connections, environment configurations comes here.
    """
    _instance = None

    def __init__(self, name, load_environment=True, configure_logging=True):
        self.name = name
        self.environment = os.getenv("ENV", "development")
        self.db_engines = {}

        if load_environment:
            self.load_environment()

        if configure_logging:
            self.configure_logging()

        self.logger = logging.getLogger(__name__)

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def env(self, name, default_value=None):
        """
        Fetches environment variable key on the basis of provided name.

        param str name: Name of the environment
        param str default_Value: Set to None, it is used if name is not provided.

        return str: Name of the environment key
        """
        return os.getenv(name, default_value)

    def load_environment(self):
        """
        Loads environment configuration from the provided environment file.
        """
        dotenv.load_dotenv(dotenv_path=".env.{}".format(self.environment))

    def configure_logging(self):
        """
        Configures enabling disabling of logs on the basis of configuration.
        """
        logging.basicConfig(filename="migrations.log")
        coloredlogs.install(
            level="DEBUG",
            milliseconds=True
        )

    def db_config(self):
        """
        Manages base peewee database connection for Postgres db.

        return PostgresqlDatabase: Database object is provided.
        """
        return PostgresqlDatabase(
            self.env("DB"),
            user=self.env("DB_USER"),
            password=self.env("DB_PASSWORD"),
            host=self.env("DB_HOST"),
            port=self.env("DB_PORT")
        )

    def db_engine(self, db_alias):
        """
        Iterates through configured database engines and against the provided alias database conig is stored.

        param str db_alias: Name of the database table.

        return PostgresqlDatabase: Database object is provided.
        """
        if db_alias not in self.db_engines:
            self.db_engines[db_alias] = self.db_config()

        return self.db_engines[db_alias]

    def db_session(self, db_alias):
        """
        Manages connection to the database against provided alias.

        param str db_alias: Name of the database table.

        return PostgresqlDatabase: Database object is provided.
        """
        return self.db_engine(db_alias)

    def run(self, callable, *args):
        """
        Base runner for application object.
        """
        self.logger.info(f"Starting {self.name}")
        callable(*args)
        self.logger.info(f"Finished {self.name}")
