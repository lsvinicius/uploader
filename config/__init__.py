import os

environment = os.environ.get('ENVIRONMENT')
if environment == 'prod':
    from config.prod import *
elif environment == 'stg':
    from config.stg import *
else:
    from config.dev import *
