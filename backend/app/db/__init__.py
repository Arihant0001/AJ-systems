from app.db.session import engine

# Ensure models are imported so metadata is complete
from app.db import models  # noqa: F401
