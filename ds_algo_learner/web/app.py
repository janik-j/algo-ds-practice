from flask import Flask, render_template, request, jsonify, session
from ..problems.problem_set import PROBLEMS
from ..ai_assistant.assistant import AIAssistant
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import genanki
import io
from typing import List, Dict, Any
from flask import send_file, jsonify, request
import inspect
from collections import *

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Set a secret key for sessions
ai_assistant = AIAssistant(api_key=os.getenv('GOOGLE_AI_API_KEY'))

# File to store user progress
PROGRESS_FILE = 'user_progress.json'

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

# Load progress at startup
USER_PROGRESS = load_progress()

@app.route('/')
def index():
    categories = {}
    for problem_name, problem_data in PROBLEMS.items():
        category = problem_data['category']
        if category not in categories:
            categories[category] = {}
        categories[category][problem_name] = {
            'title': problem_data['title'],
            'difficulty': problem_data['difficulty']
        }
        
    user_id = session.get('user_id', 'default_user')
    progress = USER_PROGRESS.get(user_id, [])
    
    return render_template('index.html', categories=categories, progress=progress)

    
@app.route('/problem/<problem_name>')
def problem(problem_name):
    problem_data = PROBLEMS.get(problem_name)
    if problem_data:
        return render_template('problem.html', problem=problem_data, problem_name=problem_name)
    return "Problem not found", 404

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    problem_name = data['problem']
    user_message = data['message']
    user_code = data.get('code', '')
    time_complexity_estimate = data.get('time_complexity_estimate', '')  
    space_complexity_estimate = data.get('space_complexity_estimate', '') 

    problem_data = PROBLEMS.get(problem_name)
    if not problem_data:
        return jsonify({'error': 'Problem not found'}), 404

    ai_response = ai_assistant.get_response(user_message, problem_data['description'], user_code, time_complexity_estimate, space_complexity_estimate)
    return jsonify(ai_response)

@app.route('/check_solution', methods=['POST'])
def check_solution():
    data = request.json
    problem_name = data['problem']
    user_solution = data['solution']
    duration = data['duration']
    time_complexity_estimate = data['time_complexity_estimate']
    space_complexity_estimate = data['space_complexity_estimate']
    
    problem_data = PROBLEMS.get(problem_name)
    if not problem_data:
        return jsonify({'error': 'Problem not found'}), 404

    results = []
    all_correct = True
    
    try:
        # Execute the user's function definition
        exec(user_solution, globals())
        
        # Get the user's function
        user_function = globals()[problem_name]
        
        # Get the number of parameters the function expects
        num_params = len(inspect.signature(user_function).parameters)

        for case in problem_data['test_cases']:
            try:
                input_data = case['input']
                expected_result = case['expected']
                
                # Call the user's function
                if isinstance(input_data, list):
                    if num_params == 1:
                        # If the function expects one argument, pass the whole list
                        user_result = user_function(input_data)
                    else:
                        # If the function expects multiple arguments, unpack the list
                        user_result = user_function(*input_data)
                else:
                    # If input is not a list, pass it directly
                    user_result = user_function(input_data)
                
                if problem_name == 'group_anagrams':
                    is_correct = sorted([sorted(group) for group in user_result]) == sorted([sorted(group) for group in expected_result])
                else:
                    is_correct = user_result == expected_result

                if not is_correct:
                    all_correct = False

                
                results.append({
                    'input': str(input_data),
                    'expected': str(expected_result),
                    'user_result': str(user_result),
                    'is_correct': is_correct
                })
                
            except Exception as e:
                app.logger.error(f"Error in test case: {str(e)}")
                all_correct = False
                results.append({
                    'input': str(input_data),
                    'expected': str(expected_result),
                    'user_result': f"Error: {str(e)}",
                    'is_correct': False
                })
    
    except Exception as e:
        app.logger.error(f"Error in code execution: {str(e)}")
        all_correct = False
        results.append({
            'input': 'N/A',
            'expected': 'N/A',
            'user_result': f"Error in code: {str(e)}",
            'is_correct': False
        })

    if all_correct:
        actual_time_complexity = problem_data.get('time_complexity', 'N/A')
        actual_space_complexity = problem_data.get('space_complexity', 'N/A')
        
        feedback = generate_feedback(
            time_complexity_estimate, 
            space_complexity_estimate, 
            actual_time_complexity, 
            actual_space_complexity, 
            data['chat_log'], 
            user_solution,
            problem_name
        )

        anki_cards = generate_anki_cards(problem_data, user_solution, feedback)
        
        update_progress(
            problem_name,
            duration,
            time_complexity_estimate,
            space_complexity_estimate,
            actual_time_complexity,
            actual_space_complexity,
            feedback,
            [[] if not anki_cards else anki_cards]
        )
    else:
        feedback = None
        anki_cards = []
    
    return jsonify({
        'all_correct': all_correct,
        'results': results,
        'feedback': feedback,
        'anki_cards': anki_cards
    })

@app.route('/remove_problem', methods=['POST'])
def remove_problem():
    data = request.json
    problem_name = data.get('problem')
    
    if not problem_name:
        return jsonify({'status': 'error', 'message': 'Problem name is required'}), 400
    
    user_id = session.get('user_id', 'default_user')
    
    if user_id not in USER_PROGRESS:
        return jsonify({'status': 'error', 'message': 'No progress found for this user'}), 404
    
    user_progress = USER_PROGRESS[user_id]
    
    # Find the index of the problem to remove
    index_to_remove = next((index for (index, d) in enumerate(user_progress) if d["problem"] == problem_name), None)
    
    if index_to_remove is not None:
        # Remove the problem from the user's progress
        del user_progress[index_to_remove]
        
        # Save the updated progress
        save_progress(USER_PROGRESS)
        
        return jsonify({'status': 'success', 'message': 'Problem removed successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Problem not found in user progress'}), 404


@app.route('/download_anki_cards/<problem_name>', methods=['GET'])
def download_anki_cards(problem_name):
    user_id = session.get('user_id', 'default_user')
    user_progress = USER_PROGRESS.get(user_id, [])
    problem_entry = next((item for item in user_progress if item['problem'] == problem_name), None)
    
    if problem_entry and 'anki_cards' in problem_entry:
        anki_cards = problem_entry['anki_cards']
        
        try:
            file_obj = create_anki_package(problem_name, anki_cards)
            
            return send_file(
                file_obj,
                as_attachment=True,
                download_name=f"{problem_name}_anki_cards.apkg",
                mimetype='application/apkg'
            )
        except Exception as e:
            return jsonify({"error": "Failed to create Anki package", "details": str(e)}), 500
    else:
        return jsonify({"error": "No Anki cards found for this problem"}), 404

def update_progress(problem_name, duration, time_complexity_estimate, space_complexity_estimate, actual_time_complexity, actual_space_complexity, feedback, anki_cards):
    user_id = session.get('user_id', 'default_user')
    if user_id not in USER_PROGRESS:
        USER_PROGRESS[user_id] = []
    
    problem_data = PROBLEMS.get(problem_name)
    problem_difficulty = problem_data.get('difficulty', 'Not specified')

    entry = next((item for item in USER_PROGRESS[user_id] if item['problem'] == problem_name), None)
    if entry:
        entry.update({
            'date': datetime.now().strftime('%d %b'),
            'duration': duration,
            'difficulty': problem_difficulty,
            'time_complexity_estimate': time_complexity_estimate,
            'space_complexity_estimate': space_complexity_estimate,
            'actual_time_complexity': actual_time_complexity,
            'actual_space_complexity': actual_space_complexity,
            'feedback': feedback,
            'anki_cards': anki_cards
        })
    else:
        USER_PROGRESS[user_id].append({
            'date': datetime.now().strftime('%d %b'),
            'problem': problem_name,
            'duration': duration,
            'difficulty': problem_difficulty,
            'time_complexity_estimate': time_complexity_estimate,
            'space_complexity_estimate': space_complexity_estimate,
            'actual_time_complexity': actual_time_complexity,
            'actual_space_complexity': actual_space_complexity,
            'feedback': feedback,
            'anki_cards': anki_cards
        })
    
    save_progress(USER_PROGRESS)


@app.route('/update_progress', methods=['POST'])
def update_progress_route():
    data = request.json
    problem_name = data['problem']
    duration = data['duration']
    time_complexity_estimate = data.get('time_complexity_estimate', 'N/A')
    space_complexity_estimate = data.get('space_complexity_estimate', 'N/A')
    user_message = data['message']
    user_code = data.get('code', '')

    problem_data = PROBLEMS.get(problem_name)
    actual_time_complexity = problem_data.get('time_complexity', 'N/A')
    actual_space_complexity = problem_data.get('space_complexity', 'N/A')
    
    update_progress(
        problem_name, 
        duration, 
        time_complexity_estimate, 
        space_complexity_estimate, 
        user_message,
        user_code,
        actual_time_complexity,
        actual_space_complexity,
        None,
        []
    )
    
    feedback = generate_feedback(
        time_complexity_estimate, 
        space_complexity_estimate, 
        actual_time_complexity, 
        actual_space_complexity, 
        data['chat_log'],
        data['solution'],
        data['problem']
    )
    
    return jsonify({'status': 'success', 'feedback': feedback})


def generate_feedback(time_estimate, space_estimate, actual_time, actual_space, chat_log, solution, problem_description):
    print("Generating feedback...")
    # Prepare the prompt for the LLM (using the AIAssistant class)
    prompt = f"""
    ## Code Review and Skill Assessment

    **Problem Description:** {problem_description}

    **User's Solution:**
    ```python
    {solution}
    ```

    **Chat Log:**
    ```
    {chat_log}
    ```

    **Complexity Estimates:**
    - Time Complexity Estimate: {time_estimate}
    - Space Complexity Estimate: {space_estimate}

    **Actual Complexities:**
    - Time Complexity: {actual_time}
    - Space Complexity: {actual_space}

    **Task:**
    1. **Evaluate the user's understanding of the problem and their approach to solving it.**
    2. **Assess the quality and efficiency of their solution.** 
    3. **Provide a score (1-10) representing the user's estimated skill level in solving this type of problem.**
    4. **Offer concise and constructive feedback, including:**
        - Accuracy of complexity estimates.
        - Strengths and weaknesses of the solution (e.g., correctness, readability, efficiency).
        - Potential areas for improvement.
        - Insights from the chat log (if relevant).

    **Feedback Format:**
    ```
    Estimated Skill Level: [Score]/10

    [Concise and specific feedback points, as described in the task above. Maximum 1 short sentences that focus on weakness, don't use any formatting or code blocks.] 
    ```
    """

    # Use the AIAssistant to get the LLM response
    response = ai_assistant.get_final_feedback(prompt)
    return response

def generate_anki_cards(problem_data: Dict, user_solution: str, feedback: str) -> List[Dict[str, str]]:
    prompt = f"""
    Based on the following information about a coding problem and the user's solution, generate 5-7 Anki cards. 
    These cards should cover various aspects of the problem, including but not limited to:
    1. Core concepts related to the problem
    2. Time and space complexity considerations
    3. Common pitfalls or edge cases
    4. Optimization techniques
    5. Related problems or algorithms

    Problem Information:
    Title: {problem_data['title']}
    Description: {problem_data['description']}
    Difficulty: {problem_data['difficulty']}
    
    User's Solution:
    ```python
    {user_solution}
    ```
    
    Feedback on User's Solution:
    {feedback}

    For each card, provide a question that tests understanding of an important aspect of the problem or solution, and an answer that explains the concept.
    
    Return the cards as a JSON array of objects, each with 'question' and 'answer' keys.
    """
    
    anki_cards = ai_assistant.get_anki_cards(prompt)
    
    # Validate the structure of the anki_cards
    valid_cards = []
    for card in anki_cards:
        if isinstance(card, dict) and 'question' in card and 'answer' in card:
            valid_cards.append(card)
        else:
            print(f"Invalid card structure: {card}")
    
    return valid_cards

def create_anki_package(problem_name: str, anki_cards: List[List[Dict[str, str]]]) -> io.BytesIO:
    # Create a unique deck ID (you may want to generate this more systematically)
    deck_id = hash(problem_name) % (2**63)
    
    # Create the deck
    deck = genanki.Deck(deck_id, f"Coding Practice: {problem_name}")
    
    # Create a unique model ID
    model_id = deck_id + 1
    
    # Create the note model
    model = genanki.Model(
        model_id,
        'Coding Practice Card',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])
    
    # Add notes to the deck
    if anki_cards and isinstance(anki_cards[0], list):
        for card_list in anki_cards:
            for card in card_list:
                if isinstance(card, dict) and 'question' in card and 'answer' in card:
                    note = genanki.Note(
                        model=model,
                        fields=[card['question'], card['answer']]
                    )
                    deck.add_note(note)
    else:
        raise ValueError("Invalid anki_cards format")

    # Create the package
    package = genanki.Package(deck)
    
    # Save the package to a byte stream
    file_obj = io.BytesIO()
    package.write_to_file(file_obj)
    file_obj.seek(0)
    
    return file_obj
