from typing import List

def contains_duplicate(nums : List[int]) -> bool:
    """
    Given an integer array nums, return true if any value appears 
    at least twice in the array, and return false if every element is distinct.
    """
    return len(nums) != len(set(nums))

CONTAINS_DUPLICATE = {
    'title': 'Contains Duplicate',
    'signature': 'nums : List[int]',
    'category': 'Array & Hashing',
    'description': 'Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.',
    'function': contains_duplicate,
    'test_cases': [
        {'input': [1,2,3,1], 'expected': True},
        {'input': [1,2,3,4], 'expected': False},
        {'input': [1,1,1,3,3,4,3,2,4,2], 'expected': True}
    ],
    'time_complexity': 'O(n)',
    'space_complexity': 'O(n)',
    'difficulty': 'Easy',
    'examples': [
        {'input': '[1, 2, 3, 1]', 'output': 'true'},
        {'input': '[1, 2, 3, 4]', 'output': 'false'}
    ]
}

def valid_anagram(s: str, t: str) -> bool:
    """
    Given two strings s and t, return true if t is an anagram of s, and false otherwise.
    """
    # Placeholder implementation
    return sorted(s) == sorted(t)

VALID_ANAGRAM = {
    'title': 'Valid Anagram',
    'signature': 's: str, t: str',
    'category': 'Array & Hashing',
    'description': 'Given two strings s and t, return true if t is an anagram of s, and false otherwise.',
    'function': valid_anagram,
    'test_cases': [
        {'input': ['anagram', 'nagaram'], 'expected': True},
        {'input': ['rat', 'car'], 'expected': False}
    ],
    'time_complexity': 'O(n log n)',  # Due to sorting
    'space_complexity': 'O(1)',
    'difficulty': 'Easy',
    'examples': [
        {'input': 's = "anagram", t = "nagaram"', 'output': 'true'},
        {'input': 's = "rat", t = "car"', 'output': 'false'}
    ]
}

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    """
    # Placeholder implementation
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

TWO_SUM = {
    'title': 'Two Sum',
    'signature': 'nums: List[int], target: int',
    'category': 'Array & Hashing',
    'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
    'function': two_sum,
    'test_cases': [
        {'input': [[2,7,11,15], 9], 'expected': [0,1]},
        {'input': [[3,2,4], 6], 'expected': [1,2]},
        {'input': [[3,3], 6], 'expected': [0,1]}
    ],
    'time_complexity': 'O(n)',
    'space_complexity': 'O(n)',
    'difficulty': 'Easy',
    'examples': [
        {'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]'},
        {'input': 'nums = [3,2,4], target = 6', 'output': '[1,2]'}
    ]
}

def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Given an array of strings strs, group the anagrams together. You can return the answer in any order.
    """
    # Placeholder implementation
    anagram_groups = {}
    for s in strs:
        sorted_s = ''.join(sorted(s))
        if sorted_s in anagram_groups:
            anagram_groups[sorted_s].append(s)
        else:
            anagram_groups[sorted_s] = [s]
    return list(anagram_groups.values())

GROUP_ANAGRAMS = {
    'title': 'Group Anagrams',
    'signature': 'strs: List[str]',
    'category': 'Array & Hashing',
    'description': 'Given an array of strings strs, group the anagrams together. You can return the answer in any order.',
    'function': group_anagrams,
    'test_cases': [
        {'input': ["eat","tea","tan","ate","nat","bat"], 'expected': [["bat"],["nat","tan"],["ate","eat","tea"]]},
        {'input': [""], 'expected': [[""]]},
        {'input': ["a"], 'expected': [["a"]]}
    ],
    'time_complexity': 'O(n * k log k)',  # n is the number of strings, k is the maximum length of a string
    'space_complexity': 'O(n * k)',
    'difficulty': 'Medium',
    'examples': [
        {'input': 'strs = ["eat","tea","tan","ate","nat","bat"]', 'output': '[["bat"],["nat","tan"],["ate","eat","tea"]]'},
        {'input': 'strs = [""]', 'output': '[[""]]'}
    ]
}

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Given an integer array nums and an integer k, return the k most frequent elements.
    """
    # Placeholder implementation
    from collections import Counter
    return [x for x, _ in Counter(nums).most_common(k)]

TOP_K_FREQUENT_ELEMENTS = {
    'title': 'Top K Frequent Elements',
    'signature': 'nums: List[int], k: int',
    'category': 'Array & Hashing',
    'description': 'Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.',
    'function': top_k_frequent,
    'test_cases': [
        {'input': [[1,1,1,2,2,3], 2], 'expected': [1,2]},
        {'input': [[1], 1], 'expected': [1]}
    ],
    'time_complexity': 'O(n log k)',  # Using heap
    'space_complexity': 'O(n)',
    'difficulty': 'Medium',
    'examples': [
        {'input': 'nums = [1,1,1,2,2,3], k = 2', 'output': '[1,2]'},
        {'input': 'nums = [1], k = 1', 'output': '[1]'}
    ]
}

def encode(strs: List[str]) -> str:
    """
    Encodes a list of strings to a single string.
    """
    # Placeholder implementation
    return ''

def decode(s: str) -> List[str]:
    """
    Decodes a single string to a list of strings.
    """
    # Placeholder implementation
    return []

ENCODE_DECODE_STRINGS = {
    'title': 'Encode and Decode Strings',
    'signature': 'encode(strs: List[str]) -> str, decode(s: str) -> List[str]',
    'category': 'Array & Hashing',
    'description': 'Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and is decoded back to the original list of strings.',
    'function': (encode, decode),
    'test_cases': [
        {'input': ["Hello","World"], 'expected': ["Hello","World"]},
        {'input': ["", "a"], 'expected': ["", "a"]}
    ],
    'time_complexity': 'O(n)',
    'space_complexity': 'O(n)',
    'difficulty': 'Medium',
    'examples': [
        {'input': 'Input: ["Hello","World"]', 'output': 'Output: ["Hello","World"]'},
        {'input': 'Input: [""]', 'output': 'Output: [""]'}
    ]
}

def product_except_self(nums: List[int]) -> List[int]:
    """
    Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].
    """
    # Placeholder implementation
    return []

PRODUCT_OF_ARRAY_EXCEPT_SELF = {
    'title': 'Product of Array Except Self',
    'signature': 'nums: List[int]',
    'category': 'Array & Hashing',
    'description': 'Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].',
    'function': product_except_self,
    'test_cases': [
        {'input': [1,2,3,4], 'expected': [24,12,8,6]},
        {'input': [-1,1,0,-3,3], 'expected': [0,0,9,0,0]}
    ],
    'time_complexity': 'O(n)',
    'space_complexity': 'O(1)',  # Excluding the output array
    'difficulty': 'Medium',
    'examples': [
        {'input': 'nums = [1,2,3,4]', 'output': '[24,12,8,6]'},
        {'input': 'nums = [-1,1,0,-3,3]', 'output': '[0,0,9,0,0]'}
    ]
}

def longest_consecutive(nums: List[int]) -> int:
    """
    Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
    """
    # Placeholder implementation
    return 0

LONGEST_CONSECUTIVE_SEQUENCE = {
    'title': 'Longest Consecutive Sequence',
    'signature': 'nums: List[int]',
    'category': 'Array & Hashing',
    'description': 'Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.',
    'function': longest_consecutive,
    'test_cases': [
        {'input': [100,4,200,1,3,2], 'expected': 4},
        {'input': [0,3,7,2,5,8,4,6,0,1], 'expected': 9}
    ],
    'time_complexity': 'O(n)',
    'space_complexity': 'O(n)',
    'difficulty': 'Medium',
    'examples': [
        {'input': 'nums = [100,4,200,1,3,2]', 'output': '4'},
        {'input': 'nums = [0,3,7,2,5,8,4,6,0,1]', 'output': '9'}
    ]
}