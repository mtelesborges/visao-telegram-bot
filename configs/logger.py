import logging
from datetime import datetime

time = datetime.now()

# Enable logging
logging.basicConfig(
    format="[%(asctime)s] %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
