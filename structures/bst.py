from typing import Optional, Callable

class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BinarySearchTree:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key, value):
        def _insert(node, key, value):
            if node is None:
                return BSTNode(key, value)
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                node.value = value
            return node
        self.root = _insert(self.root, key, value)

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        return None

    def inorder(self, visit: Callable):
        def _inorder(node):
            if node:
                _inorder(node.left)
                visit(node.key, node.value)
                _inorder(node.right)
        _inorder(self.root)

    def delete(self, key):
        def _min_value_node(n):
            current = n
            while current.left:
                current = current.left
            return current

        def _delete(node, key):
            if not node: return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                if not node.left: return node.right
                if not node.right: return node.left
                temp = _min_value_node(node.right)
                node.key, node.value = temp.key, temp.value
                node.right = _delete(node.right, temp.key)
            return node
        self.root = _delete(self.root, key)