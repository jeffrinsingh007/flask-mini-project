SECRET_KEY = 'your_super_secret_key'
SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://localhost\\SQLEXPRESS/testconnection"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
