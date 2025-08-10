class Config() :
    DEBUG=False
    SQLALCHEMY_TRACK_MODIFICATION=True

class LocalDevelopmentConfig(Config):
    #configuration for DB
    SQLALCHEMY_DATABASE_URI="sqlite:///utility1.sqlite3"
    DEBUG = True

    #configuration for security
    JWT_SECRET_KEY = "this-is-a-secret-key"   #hash user credentials and store in session
    SECURITY_PASSWORD_HASH="bcrypt" #mechanism to hash credentials and store in data base
    SECURITY_PASSWORD_SALT="this-is-salt-key" 
    # WTF_CSRF_ENABLED=False     #web token form , only for frontend forms
    # SECURITY_TOKEN_AUTHENTICATION_HEADER="Authentication-Token"
