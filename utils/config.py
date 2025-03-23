from dotenv import load_dotenv
import os

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# DB config
SQL_BACKEND_API_URL = os.getenv("SQL_BACKEND_API_URL")



