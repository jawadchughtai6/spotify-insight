from peewee import PostgresqlDatabase

from application import Application

app = Application("Compute Insight")

db = PostgresqlDatabase(
    app.env("DB"),
    user=app.env("DB_USER"),
    password=app.env("DB_PASSWORD"),
    host=app.env("DB_HOST"),
    port=app.env("DB_PORT")
)
