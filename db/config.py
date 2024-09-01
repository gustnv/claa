import os

# Database configuration using environment variables for sensitive data
config = {
    # Database username from environment variable or default to 'root'
    'user': os.environ.get('DB_USER', 'root'),
    # Database password from environment variable or default to 'P4ssw0rd!'
    'password': os.environ.get('DB_PASSWORD', 'P4ssw0rd!'),
    'host': '127.0.0.1',  # Host address of the database
    'database': 'claa',  # Name of the database
    # Raise exceptions for warnings (useful for debugging)
    'raise_on_warnings': True
}

# SMTP server configuration for sending emails
smtp_server = "smtp.gmail.com"  # SMTP server address
smtp_port = 587  # SMTP server port
smtp_username = "nunesvianagustavo@gmail.com"  # SMTP username (email address)
# SMTP password from environment variable or default (should be kept secret)
smtp_password = os.environ.get('EMAIL_PASSWORD', '')
