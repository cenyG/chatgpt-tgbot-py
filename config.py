import logging
from dotenv import dotenv_values

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

env = dotenv_values(".env")