import os
import logging

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Bot configs
currencies_url = 'https://openexchangerates.org/api/currencies.json'
base_api_url = 'https://api.exchangeratesapi.io'
round_index = 2
DEBUG=True