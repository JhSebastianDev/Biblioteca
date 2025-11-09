class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left: 'AVLNode' = None
        self.right: 'AVLNode' = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root: AVLNode = None

    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def insert(self, key, value):
        def _insert(node, key, value):
            if not node:
                return AVLNode(key, value)
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                node.value = value
                return node
            self._update_height(node)
            return self._rebalance(node)
        self.root = _insert(self.root, key, value)

    def _rebalance(self, node):
        bf = self._balance_factor(node)
        if bf > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if bf < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def search(self, key):
        cur = self.root
        while cur:
            if key == cur.key:
                return cur.value
            cur = cur.left if key < cur.key else cur.right
        return None

    def inorder(self, visit):
        def _in(node):
            if node:
                _in(node.left)
                visit(node.key, node.value)
                _in(node.right)
        _in(self.root)

    def delete(self, key):
        def _min_node(n):
            while n.left:
                n = n.left
            return n

        def _delete(node, key):
            if not node: return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                if not node.left: return node.right
                if not node.right: return node.left
                temp = _min_node(node.right)
                node.key, node.value = temp.key, temp.value
                node.right = _delete(node.right, temp.key)
            self._update_height(node)
            return self._rebalance(node)
        self.root = _delete(self.root, key)