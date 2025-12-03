import os

# Determine which settings module to use based on environment variables
if os.getenv('AZURE_DEPLOYMENT', '0') == '1' and os.getenv('AUTO_PROD_ON_AZURE', '0') == '1':
    from .prod import *
else:
    from .dev import *
