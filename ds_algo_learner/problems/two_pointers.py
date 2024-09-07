def reverse_string(s):
    """
    Write a function that reverses a string. The input string is given as an array of characters s.
    You must do this by modifying the input array in-place with O(1) extra memory.
    """
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return s

REVERSE_STRING = {
    'title': 'Reverse String',
    'signature': 's : List[str]',
    'category': 'Two Pointers',
    'description': 'Write a function that reverses a string. The input string is given as an array of characters s. You must do this by modifying the input array in-place with O(1) extra memory.',
    'function': reverse_string,
    'test_cases': [
        {'input': ["h","e","l","l","o"], 'expected': ["o","l","l","e","h"]},
        {'input': ["H","a","n","n","a","h"], 'expected': ["h","a","n","n","a","H"]}
    ],
    'time_complexity': 'O(n)',
    'space_complexity': 'O(1)',
    'difficulty': 'Easy',
    'examples': [
        {'input': '["h", "e", "l", "l", "o"]', 'output': '["o", "l", "l", "e", "h"]'},
        {'input': '["H", "a", "n", "n", "a", "h"]', 'output': '["h", "a", "n", "n", "a", "H"]'}
    ]
}
