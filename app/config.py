from dotenv import load_dotenv
import os

load_dotenv()

FGT_IP = os.getenv("FGT_IP")
FGT_TOKEN = os.getenv("FGT_API_KEY")
