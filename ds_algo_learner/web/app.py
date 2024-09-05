from flask import Flask, render_template, request, jsonify
from ..problems.problem_set import PROBLEMS
from ..ai_assistant.assistant import AIAssistant
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
ai_assistant = AIAssistant(api_key=os.getenv('GOOGLE_AI_API_KEY'))

@app.route('/')
def index():
    categories = {}
    for problem_name, problem_data in PROBLEMS.items():
        category = problem_data['category']
        if category not in categories:
            categories[category] = []
        categories[category].append((problem_name, problem_data['title']))
    return render_template('index.html', categories=categories)

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
    
    problem_data = PROBLEMS.get(problem_name)
    if not problem_data:
        return jsonify({'error': 'Problem not found'}), 404

    results = []
    all_correct = True
    for case in problem_data['test_cases']:
        try:
            user_result = eval(user_solution)(*case['input'])
            expected_result = problem_data['function'](*case['input'])
            is_correct = user_result == expected_result
            if not is_correct:
                all_correct = False
            results.append({
                'input': str(case['input']),
                'expected': str(expected_result),
                'user_result': str(user_result),
                'is_correct': is_correct
            })
        except Exception as e:
            all_correct = False
            results.append({
                'input': str(case['input']),
                'expected': str(case['expected']),
                'user_result': str(e),
                'is_correct': False
            })
    
    return jsonify({
        'all_correct': all_correct,
        'results': results
    })
