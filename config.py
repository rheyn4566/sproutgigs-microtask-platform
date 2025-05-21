class Config:
    SECRET_KEY = 'a_very_secret_key_that_should_be_changed'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
