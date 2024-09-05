import google.generativeai as genai
from typing import Dict

class AIAssistant:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])

    def get_response(self, user_message: str, problem: str, user_code: str = None) -> Dict[str, str]:
        context = f"The current coding problem is: {problem}"
        if user_code:
            context += f"\n\nUser's current code:\n```python\n{user_code}\n```"
        
        prompt = f"""
        {context}

        User: {user_message}

        Based on the problem description and the user's current code (if provided), please provide a response in the following format:
        Chat: [Your explanation, guidance, or hint here. If the user is requesting a hint, make sure it's relevant to their current progress.]
        Code Hint: [A brief code hint or comment that can be inserted into the user's code. This should be directly related to the next step or improvement the user could make.]

        Remember to keep the Chat response concise and focused, and make the Code Hint a single line comment or short code snippet that's relevant to the user's current code state.
        """
        
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