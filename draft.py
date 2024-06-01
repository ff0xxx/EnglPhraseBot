import os
import dotenv
from pprint import pprint

dotenv.load_dotenv()

pprint(os.getenv('BOT_TOKEN'))
pprint(os.getenv('ADMIN_ID'))