class Config:
    # Database configuration (MySQL)
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:200875@localhost/flask_ecommerce_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to avoid warnings.

    # JWT configuration
    JWT_SECRET_KEY = 'secretestkey'  # Secret key used to sign JWT tokens.
