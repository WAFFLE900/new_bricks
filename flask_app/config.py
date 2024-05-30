# Config to run Flask app in DEV and PROD mode

# Flask default configs
DEBUG = True
SECRET_KEY = "secret"

# Database configs
db_username = 'bricks'
db_password = 'NCCUgdsc1234!'
db_host = '104.199.143.218'
db_port = '3306'
db_name = 'bricksdata'
DB_URL = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

# Google OAuth2 credential configs
GOOGLE_OAUTH_CLIENT_ID = '1083338780028-1qnats3frrionef34vuiq5th6tetv8k4.apps.googleusercontent.com'
GOOGLE_OAUTH_CLIENT_SECRET = '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'

