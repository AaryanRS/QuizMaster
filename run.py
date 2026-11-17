import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from a .env file if present
load_dotenv()

app = create_app()

if __name__ == "__main__":
    # Read FLASK_DEBUG from environment, default to "0" (False), and evaluate to boolean
    debug_mode = os.environ.get("FLASK_DEBUG", "0").lower() in ["1", "true", "yes"]
    app.run(debug=debug_mode)