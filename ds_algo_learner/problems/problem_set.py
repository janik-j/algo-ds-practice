
def contains_duplicate(nums):
    """
    Given an integer array nums, return true if any value appears 
    at least twice in the array, and return false if every element is distinct.
    """
    return len(nums) != len(set(nums))

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

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    """
    Given the head of a singly linked list, reverse the list, and return the reversed list.
    """
    prev = None
    current = head
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    return prev

PROBLEMS = {
    'contains_duplicate': {
        'title': 'Contains Duplicate',
        'category': 'Array',
        'description': 'Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.',
        'function': contains_duplicate,
        'test_cases': [
            {'input': [1,2,3,1], 'expected': True},
            {'input': [1,2,3,4], 'expected': False},
            {'input': [1,1,1,3,3,4,3,2,4,2], 'expected': True}
        ],
        'time_complexity': 'O(n)',
        'space_complexity': 'O(n)',
        'difficulty': 'Easy'
    },
    'reverse_string': {
        'title': 'Reverse String',
        'category': 'String',
        'description': 'Write a function that reverses a string. The input string is given as an array of characters s. You must do this by modifying the input array in-place with O(1) extra memory.',
        'function': reverse_string,
        'test_cases': [
            {'input': [["h","e","l","l","o"]], 'expected': ["o","l","l","e","h"]},
            {'input': [["H","a","n","n","a","h"]], 'expected': ["h","a","n","n","a","H"]}
        ],
        'time_complexity': 'O(n)',
        'space_complexity': 'O(1)',
        'difficulty': 'Easy'
    },
    'reverse_linked_list': {
        'title': 'Reverse Linked List',
        'category': 'Linked List',
        'description': 'Given the head of a singly linked list, reverse the list, and return the reversed list.',
        'function': reverse_linked_list,
        'test_cases': [
            {'input': [ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))], 'expected': [5,4,3,2,1]},
            {'input': [ListNode(1, ListNode(2))], 'expected': [2,1]},
            {'input': [None], 'expected': None}
        ],
        'time_complexity': 'O(n)',
        'space_complexity': 'O(1)',
        'difficulty': 'Easy'
    }
}

