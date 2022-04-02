import os


def get_postgres_uri(host="localhost"):
    port = 5432
    password = os.environ.get("DB_PASSWORD", "postgres")
    user, db_name = "postgres", "postgres"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
