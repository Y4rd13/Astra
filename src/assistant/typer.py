import re
import keyboard

class Typer:
    def __init__(self):
        pass

    def type_text(self, text):
        """
        Escribe el texto proporcionado utilizando el teclado.
        """
        keyboard.write(text)

    def parse_code(self, message):
        """
        Parsea el mensaje para extraer el código entre delimitadores de bloque de código.
        """
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', message, re.DOTALL)
        code = "\n\n".join(code_blocks)
        explanation = re.sub(r'```(?:\w+)?\n.*?```', '', message, flags=re.DOTALL).strip()
        return code, explanation

    def type_code(self, message):
        """
        Escribe el código proporcionado en la IDLE o cualquier editor de texto.
        """
        code, explanation = self.parse_code(message)
        if code:
            keyboard.write(code)
        return explanation
