"""Entry point to run the Flask development server."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'app'))

from app import app  # noqa: E402

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
