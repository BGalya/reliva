from gemini import init_model
import json


class GeminiObject():
    def __init__(self):
        self.gemini = init_model()
        self.__num_of_responses = 0
        self.__database, self.__community_database = None, None

    def response(self, user_input):
        response = self.gemini.ask(user_input)
        if self.__num_of_responses >= 20:
            self.gemini.ask("Reword the result of the last prompt such that it only provides a suggestion without a question in the end. Politely tell the patient you have to finish the session.")
        self.__num_of_responses += 1
        return response

    def init_chat(self):
        with open('database.json', 'r') as file:
            self.__database = json.load(file)
        with open('community.json', 'r') as file:
            self.__community_database = json.load(file)
        initial_prompt = "You are a therapist, speaking to a patient with traumatic brain injury. " \

        ended_prompt = ""

        if not self.__database["data"]:
            with open('init_data.json', 'r') as file:
                init_database = json.load(file)
            added_prompt = "You are treating a patient for the first time. " + str(init_database["data"]) + ". Ask him an initial short question, in plain English. Based on that try, and understand the problems he faced. Be sensitive. Don't offer solutions yet. "
        else:
            added_prompt = "Ask a specific question given the past conversation summaries data: " + str(self.__database["data"]) + \
                 ". Focus on errors and mistakes that have been made during the processes described. " \
                 "Keep it simple as it's an injured human being you are talking with, be polite and sensitive, " \
                 "in plain english. Always end with a relative questions, based on the user's answers and the above data given. "
            # added_prompt = "Ask a specific short question given the past conversation summaries data: " + str(self.__database["data"]) + \
            #                  ". Try to guide the patient toward a solution of this problem, or offer ways to solve it." \
            #                  " Don't ask him to solve the problem." \
            #                  "Keep it simple, short - don't ask him long questions! Use plain English as it's a human " \
            #                  "being recovering from a traumatic brain injury you are talking with. Be polite and sensitive." \
            #                  "Always end with a relative question, based on the user's answers and the data given above. " \
            #                  "Start the conversation with representing a short description of the prevous sessions"

            ended_prompt = "Also refer to the following data for examples of solutions that helped other patients: " + str(
                self.__community_database["data"])
        full_prompt = initial_prompt + " " + added_prompt + " " + ended_prompt

        # initial_prompt = "You are a therapist, speaking to a patient with traumatic brain injury. "
        # ended_prompt = ""
        # if not self.__database["data"]:
        #     with open('init_data.json', 'r') as file:
        #         init_database = json.load(file)
        #     added_prompt = "You are treating a patient for the first time. " + str(init_database[
        #                                                                                "data"]) + ". Ask him an initial question based on that to try and understand the problems. Be sensitive. Don't offer solutions yet. "
        # else:
        #     added_prompt = "Ask a specific question given the past conversation summaries data: " + str(
        #         self.__database["data"]) + \
        #                    ". Focus on errors and mistakes that have been made during the processes described. " \
        #                    "Keep it simple as it's an injured human being you are talking with, be polite and sensitive, " \
        #                    "in plain english. Always end with a relative questions, based on the user's answers and the above data given. "
        #
        #     ended_prompt = "Also refer to the following data for examples of solutions that helped other patients: " + str(
        #         self.__community_database["data"])
        #
        # full_prompt = initial_prompt + " " + added_prompt + " " + ended_prompt
        response = self.gemini.ask(full_prompt)
        return response

    def end_chat(self):
        response = self.gemini.ask("Summarize the session in terms of progress, main points, points to consider for the future. Mention all the errors and remember for future reference. Limit to 50 words total.")
        self.__database["data"].append(response)
        with open('database.json', 'w') as file:
            json.dump(self.__database, file, indent=4)
        # update community database:
        response = self.gemini.ask(
            "If this session was effective for solving the problem, describe what worked for some patient. Be concise and focus on the exact details.")
        self.__community_database["data"].append(response)
        with open('community.json', 'w') as file:
            json.dump(self.__community_database, file, indent=4)
        response = self.gemini.ask(
            "Based of what that has been discussed here, define an appropriate task and a precise date and time to complete it,"
            " along with pointers for successfully completing the task. Make it short and concise. "
            "You must include the following structure: The *exact* amount of hours from now should he perform the task, "
            "don't give a direct order but something similar to 'try to think if it feels ok, remember what we've discussed' "
            "and generate a hint based on the discussion")
        return response
