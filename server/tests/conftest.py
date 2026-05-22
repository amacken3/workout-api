import sys
from pathlib import Path

server_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(server_dir))