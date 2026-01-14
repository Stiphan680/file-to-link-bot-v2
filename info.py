from os import environ

# Bot Configuration
API_ID = int(environ.get('API_ID', '0'))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')

# Admin
ADMINS = [int(i) for i in environ.get('ADMINS', '').split()] if environ.get('ADMINS') else []

# Database
DATABASE_URI = environ.get('DATABASE_URI', '')
DATABASE_NAME = environ.get('DATABASE_NAME', 'filetolinkbot')

# Channels
BIN_CHANNEL = int(environ.get('BIN_CHANNEL', '0'))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '0'))

# Settings
PROTECT_CONTENT = environ.get('PROTECT_CONTENT', 'False').lower() == 'true'
FSUB = environ.get('FSUB', 'False').lower() == 'true'
FSUB_CHANNEL = int(environ.get('FSUB_CHANNEL', '0')) if environ.get('FSUB_CHANNEL') else 0
