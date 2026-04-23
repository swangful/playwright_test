from dotenv import load_dotenv


def load_environment() -> None:
    """Load environment variables from .env if present."""
    load_dotenv(override=False)
