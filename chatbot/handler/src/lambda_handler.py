import os
import sys

from mangum import Mangum

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .main import app

handler = Mangum(app)
