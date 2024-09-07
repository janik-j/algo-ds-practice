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

REVERSE_LINKED_LIST = {
    'title': 'Reverse Linked List',
    'category': 'Linked List',
    'signature': 'head',
    'description': 'Given the head of a singly linked list, reverse the list, and return the reversed list.',
    'function': reverse_linked_list,
    'test_cases': [
        {'input': [ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))], 'expected': [5,4,3,2,1]},
        {'input': [ListNode(1, ListNode(2))], 'expected': [2,1]},
        {'input': [None], 'expected': None}
    ],
    'time_complexity': 'O(n)',
    'space_complexity': 'O(1)',
    'difficulty': 'Easy',
    'examples': [
        {'input': '1 -> 2 -> 3 -> 4 -> 5', 'output': '5 -> 4 -> 3 -> 2 -> 1'},
        {'input': '1 -> 2', 'output': '2 -> 1'}
    ]
}