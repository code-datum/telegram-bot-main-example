import os
import logging
base_dir = os.path.dirname(os.path.abspath(__file__))


# Enable debug mode.
DEBUG = True
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN_FILE = 'private_keys/telegram.token'
BASE_API_URL = 'https://api.exchangeratesapi.io'
DECIMAL_KEY = 2