import os
from typing import List, Optional
from urllib.parse import urlparse

import google.generativeai as genai
import json
import re
from random import randint

class AIGeneratorService:
    def __init__(self, api_key: str=None, client=None):
        """
        Initializes the service and configures the Google Gemini API key.
        """
        api_key = api_key or os.getenv("GEMINI_KEY")
        if not api_key:
            raise ValueError("GEMINI_KEY environment variable not set.")
        genai.configure(api_key=api_key)


    def create_new_question(self, topic: str):  
        try:
            sirs = [
                "Knowledge of Scientific Concepts and Principles",
                "Scientific Reasoning and Problem-solving",
                "Reasoning about the Design and Execution of Research",
                "Data-based Statistical Reasoning"
            ]

            prompt = f"""
            Give me an MCAT  question in the topic of {topic}.
            The question should try to test the Scientific Inquiry and Reasoning Skills "{sirs[randint(0,3)]}"
            The response should contain a question, four multiple choice answers, the correct answer and an explanation for why each option is correct or incorrect.
            The explanation should be as detailed as possible and include pitfalls people fall into while selecting that option
            Each option should begin with a number from one to four indicating the choice count.
            The correct answer should be a number corresponding to the correct answer choice. 
            Use this JSON schema:Question = 
            {{
                "question_name": str,
                "options": [{{
                    "option": str,
                    "explanation": str
                }}],
                "correct_answer":int }}
            """
            print(prompt)
            sys_instruct="You are a educator. You want to help students by creating questions that are most likely to appear in a real MCAT exam or have already appeared in past exams. You will never use any questions from an official source. You will not use graphs or other visual tools at all"

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",  
            
                contents=prompt
            )


            if response.text: 
                parsed_question = self.parse_gemini_json_response(response.text)
                if parsed_question:
                    return parsed_question
                else:
                    print("Error: Could not parse Gemini's response.")
                    return None
            else:
                print(f"Error: Gemini API returned no result.  Details: {response}")
                return None

        except Exception as e:
            print(f"Error communicating with Gemini API: {e}")
            return None

    def parse_gemini_json_response(self, json_string):
        try:
            json_string = re.sub(r'```json\n?', '', json_string) 
            json_string = re.sub(r'\n?```', '', json_string)  
            print(json_string)

            data = json.loads(json_string) 

            print(data)
            
            question_name = data["question_name"]
            options = data["options"]
            possible_choices = []
            correct_answer = data["correct_answer"]


            for index, answer_item in enumerate(options):
                option = answer_item["option"]
                explanation = answer_item["explanation"]
                possible_choices.append(
                    {
                        f'{index+1}': {
                            "option": f'{option}',
                            "explanation": f'{explanation}'
                        }
                    }
                )

            question_data = {
                "question": question_name,
                "options": possible_choices,
                "correct_answer": correct_answer
            }

            return question_data

        except (json.JSONDecodeError, KeyError, IndexError) as e:  # Handle JSON errors
            print(f"Error parsing JSON: {e}")
            return None
