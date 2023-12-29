class QuadTreeNode:
    def __init__(self, x, y, width, height, data=None):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.children = [None] * 4
        self.data = data

class QuadTree:
    def __init__(self, x, y, width, height, max_depth):
        self.root = QuadTreeNode(x, y, width, height)
        self.max_depth = max_depth

    def insert(self, x, y, data):
        def _insert(node, x, y, data, depth):
            if depth == self.max_depth or not node.children[0]:
                node.data = data
                return
            i = (x >= node.x + node.width // 2) + (y >= node.y + node.height // 2) * 2
            if not node.children[i]:
                dx, dy = (i % 2) * node.width // 2, (i // 2) * node.height // 2
                node.children[i] = QuadTreeNode(node.x + dx, node.y + dy, node.width // 2, node.height // 2)
            _insert(node.children[i], x, y, data, depth + 1)
        _insert(self.root, x, y, data, 0)

    def query_range(self, x, y, width, height):
        def _intersects(ax, ay, aw, ah, bx, by, bw, bh):
            return ax < bx + bw and ay < by + bh and bx < ax + aw and by < ay + ah

        def _query_range(node, x, y, width, height):
            if not node or not _intersects(node.x, node.y, node.width, node.height, x, y, width, height):
                return []
            if node.data and (node.x, node.y) == (x, y):
                return [node.data]
            return sum((_query_range(c, x, y, width, height) for c in node.children), [])
        return _query_range(self.root, x, y, width, height)

    def remove(self, x, y, data):
        def _remove(node, x, y, data):
            if not node:
                return False
            if node.data == data and (node.x, node.y) == (x, y):
                node.data = None
                return True
            i = (x >= node.x + node.width // 2) + (y >= node.y + node.height // 2) * 2
            return _remove(node.children[i], x, y, data) if node.children[i] else False
        return _remove(self.root, x, y, data)

    def move(self, old_x, old_y, new_x, new_y, data):
        if self.remove(old_x, old_y, data):
            self.insert(new_x, new_y, data)
            return True
        return False