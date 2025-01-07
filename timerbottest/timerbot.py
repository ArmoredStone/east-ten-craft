import os
import logging

# Enable logging
log_filename = os.path.splitext(os.path.basename(__file__))[0]+".log"
logging.basicConfig(
    filename=log_filename, filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

#Retrieve token from environment variable
TOKEN = os.getenv("BOT_TOKEN")