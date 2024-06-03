# import os
# from assistant.core import Assistant
# from dotenv import load_dotenv

# def main():
#     load_dotenv()  # Carga las variables de entorno del archivo .env
#     api_key = os.getenv('OPENAI_API_KEY')

#     # Crea una instancia del asistente
#     astra = Assistant(api_key=api_key)
#     astra.run()

# main.py

from app import main

if __name__ == "__main__":
    main()