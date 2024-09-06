from flask import Flask, render_template, request, jsonify, session
from ..problems.problem_set import PROBLEMS
from ..ai_assistant.assistant import AIAssistant
import os
from dotenv import load_dotenv
import json
from datetime import datetime

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
            categories[category] = []
        categories[category].append((problem_name, problem_data['title']))
    
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
    
    problem_data = PROBLEMS.get(problem_name)
    if not problem_data:
        return jsonify({'error': 'Problem not found'}), 404

    ai_response = ai_assistant.get_response(user_message, problem_data['description'], user_code)
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
        user_function = globals()['contains_duplicate']
        
        for case in problem_data['test_cases']:
            try:
                input_data = case['input']
                app.logger.debug(f"Testing input: {input_data}")
                
                user_result = user_function(input_data)
                expected_result = case['expected']
                
                app.logger.debug(f"User result: {user_result}")
                app.logger.debug(f"Expected result: {expected_result}")
                
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

    if  all_correct:
        actual_time_complexity = problem_data.get('time_complexity', 'N/A')
        actual_space_complexity = problem_data.get('space_complexity', 'N/A')
        
        complexity_feedback = generate_complexity_feedback(
            time_complexity_estimate,
            space_complexity_estimate,
            actual_time_complexity,
            actual_space_complexity
        )

        update_progress(
            problem_name,
            duration,
            time_complexity_estimate,
            space_complexity_estimate,
            actual_time_complexity,
            actual_space_complexity,
            complexity_feedback
        )
    else:
        complexity_feedback = None
    
    return jsonify({
        'all_correct': all_correct,
        'results': results,
        'complexity_feedback': complexity_feedback
    })


def update_progress(problem_name, duration, time_complexity_estimate, space_complexity_estimate, actual_time_complexity, actual_space_complexity, complexity_feedback):
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
            'complexity_feedback': complexity_feedback
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
            'complexity_feedback': complexity_feedback
        })
    
    save_progress(USER_PROGRESS)


@app.route('/update_progress', methods=['POST'])
def update_progress_route():
    data = request.json
    problem_name = data['problem']
    duration = data['duration']
    time_complexity_estimate = data.get('time_complexity_estimate', 'N/A')
    space_complexity_estimate = data.get('space_complexity_estimate', 'N/A')
    approach = data.get('approach', 'N/A')
    notes = data.get('notes', 'N/A')
    
    problem_data = PROBLEMS.get(problem_name)
    actual_time_complexity = problem_data.get('time_complexity', 'N/A')
    actual_space_complexity = problem_data.get('space_complexity', 'N/A')
    
    update_progress(
        problem_name, 
        duration, 
        time_complexity_estimate, 
        space_complexity_estimate, 
        approach, 
        notes, 
        actual_time_complexity, 
        actual_space_complexity
    )
    
    complexity_feedback = generate_complexity_feedback(
        time_complexity_estimate, 
        space_complexity_estimate, 
        actual_time_complexity, 
        actual_space_complexity
    )
    
    return jsonify({'status': 'success', 'complexity_feedback': complexity_feedback})


def generate_complexity_feedback(time_estimate, space_estimate, actual_time, actual_space):
    feedback = "Complexity Analysis Feedback:\n"
    
    if time_estimate.lower() == actual_time.lower():
        feedback += f"Your time complexity estimate of {actual_time} is correct!"
    else:
        feedback += f"Your time complexity estimate ({time_estimate}) differs from the actual complexity ({actual_time}). "
    
    if space_estimate.lower() == actual_space.lower():
        feedback += f"Your space complexity estimate of {actual_time} is correct!"
    else:
        feedback += f"Your space complexity estimate ({space_estimate}) differs from the actual complexity ({actual_space}). "
    
    return feedback

