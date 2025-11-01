import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

print("\n🔍 Variáveis carregadas:")
for key, value in os.environ.items():
    if "AZURE" in key:
        print(f"{key} = {value}")