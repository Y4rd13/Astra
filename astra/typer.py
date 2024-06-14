import re
import keyboard

class Typer:
    def __init__(self):
        pass

    def type_text(self, text):
        """
        Types the provided text using the keyboard.
        """
        keyboard.write(text)

    def parse_code(self, message):
        """
        Parses the message to extract code between code block delimiters.
        """
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', message, re.DOTALL)
        code = "\n\n".join(code_blocks)
        explanation = re.sub(r'```(?:\w+)?\n.*?```', '', message, flags=re.DOTALL).strip()
        return code, explanation

    def type_code(self, message):
        """
        Types the provided code in IDLE or any text editor.
        """
        code, explanation = self.parse_code(message)
        if code:
            keyboard.write(code)
        return explanation
