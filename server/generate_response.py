import random

class GenerateResponse:
    def __init__(self, user_message: str):
        self.user_message = user_message

    def get_response(self, user_input) -> str:
        # Get response from Gemini - simple as that!
        response = gemini.ask(user_input)
        if i == 20:
            response = gemini.ask(
                "Reword the result of the last prompt such that it only provides a suggestion without a question in the end. Politely tell the patient you have to finish the session.")
            print(response + "\n")

        return random.choice(['Yes', 'No'])