import google.generativeai as genai
from typing import Dict, List
import json

class AIAssistant:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = self.model.start_chat(history=[])

    def get_response(self, user_message: str, problem: str = None, user_code: str = None, time_complexity: str = None, space_complexity: str = None) -> Dict[str, str]:
        context = f"The current coding problem is: {problem}"

        if user_code:
            context += f"\n\nUser's current code:\n```python\n{user_code}\n```"

        if time_complexity:
            context += f"\n\nUser's estimated time complexity: {time_complexity}"

        if space_complexity:
            context += f"\n\nUser's estimated space complexity: {space_complexity}"

        prompt = f"""
        {context}

        User: {user_message}

        Based on the problem description, the user's current code (if provided), and their estimated complexities, please provide a response in the following format:
        Chat: [Your explanation, guidance, or hint here. If the user is requesting a hint, make sure it's relevant to their current progress and complexities.]
        Code Hint: [A brief code hint or comment that can be inserted into the user's code. This should be directly related to the next step or improvement the user could make.]

        Remember to keep the Chat response concise and focused, and make the Code Hint a single line comment or short code snippet that's relevant to the user's current code state. 
        If the user has provided estimates for time and space complexity, consider them when giving feedback or hints. You can suggest ways to improve the complexity if they are not optimal for the problem.
        """

        #print(prompt)
        response = self.chat.send_message(prompt)
        
        # Parse the response to separate chat and code hint
        chat_response = ""
        code_hint = ""
        
        for line in response.text.split('\n'):
            if line.startswith("Chat:"):
                chat_response = line.replace("Chat:", "").strip()
            elif line.startswith("Code Hint:"):
                code_hint = line.replace("Code Hint:", "").strip()
        
        return {
            'chat': chat_response,
            'codeHint': code_hint
        }

    def clear_conversation(self):
        self.chat = self.model.start_chat(history=[])

    def get_final_feedback(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text
    
    def get_anki_cards(self, prompt: str) -> List[Dict[str, str]]:
        # Create a new model instance specifically for Anki card generation
        anki_model = genai.GenerativeModel('gemini-1.5-flash',
                                           generation_config={
                                               "response_mime_type": "application/json",
                                               "response_schema": {
                                                   "type": "array",
                                                   "items": {
                                                       "type": "object",
                                                       "properties": {
                                                           "question": {"type": "string"},
                                                           "answer": {"type": "string"}
                                                       },
                                                       "required": ["question", "answer"]
                                                   }
                                               }
                                           })
        
        response = anki_model.generate_content(prompt)
        
        try:
            anki_cards = json.loads(response.text)
            return anki_cards
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.text}")
            return []