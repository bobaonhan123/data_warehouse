# print("hello")
from . import settings
import pandas as pd

df = pd.read_excel(settings.input_path)