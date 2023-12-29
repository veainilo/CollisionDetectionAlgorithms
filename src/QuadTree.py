class QuadTreeNode():
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.children = [None] * 4
        self.is_leaf = True
        self.data = None

class QuadTree():
    def __init__(self, x, y, width, height, max_depth):
        self.root = QuadTreeNode(x, y, width, height)
        self.max_depth = max_depth

    def insert(self, x, y, data):
        self._insert(self.root, x, y, data, 0)

    def _insert(self, node, x, y, data, depth):
        if node.is_leaf:
            if node.data is None or depth >= self.max_depth:
                node.data = data
            else:
                self.subdivide(node)
                self._insert(node, x, y, data, depth)
        else:
            index = self.get_quadrant(node, x, y)
            if node.children[index] is None:
                new_width, new_height = node.width // 2, node.height // 2
                offsets = [(0, 0), (new_width, 0), (0, new_height), (new_width, new_height)]
                node.children[index] = QuadTreeNode(
                    node.x + offsets[index][0],
                    node.y + offsets[index][1],
                    new_width,
                    new_height
                )
            self._insert(node.children[index], x, y, data, depth + 1)

    def subdivide(self, node):
        midx, midy = node.x + node.width // 2, node.y + node.height // 2
        half_width, half_height = node.width // 2, node.height // 2
        node.children[0] = QuadTreeNode(node.x, node.y, half_width, half_height)
        node.children[1] = QuadTreeNode(midx, node.y, half_width, half_height)
        node.children[2] = QuadTreeNode(node.x, midy, half_width, half_height)
        node.children[3] = QuadTreeNode(midx, midy, half_width, half_height)
        node.is_leaf = False

    def get_quadrant(self, node, x, y):
        midx, midy = node.x + node.width // 2, node.y + node.height // 2
        if x < midx and y < midy:
            return 0
        elif x >= midx and y < midy:
            return 1
        elif x < midx and y >= midy:
            return 2
        else:
            return 3
    
    def query_range(self, x, y, width, height):
        return self._query_range(self.root, x, y, width, height)

    def _query_range(self, node, x, y, width, height):
        results = []
        if node.is_leaf:
            if node.data and self._intersects(node.x, node.y, node.width, node.height, x, y, width, height):
                results.append(node.data)
        else:
            for child in node.children:
                if child and self._intersects(child.x, child.y, child.width, child.height, x, y, width, height):
                    results.extend(self._query_range(child, x, y, width, height))
        return results

    def _intersects(self, ax, ay, awidth, aheight, bx, by, bwidth, bheight):
        return not (ax + awidth <= bx or bx + bwidth <= ax or
                    ay + aheight <= by or by + bheight <= ay)
    
    def remove(self, x, y, data):
        # 尝试移除点，并返回是否移除成功
        return self._remove(self.root, x, y, data)

    def _remove(self, node, x, y, data):
        if node.is_leaf:
            if node.data == data and self._contains(node, x, y):
                node.data = None
                return True
            else:
                return False

        index = self.get_quadrant(node, x, y)
        child = node.children[index]
        if child is not None:
            removed = self._remove(child, x, y, data)
            if removed:
                # 如果子节点现在为空，尝试合并兄弟节点
                if all(c is None or (c.is_leaf and c.data is None) for c in node.children):
                    node.children = [None] * 4
                    node.is_leaf = True
                return True
        return False
    
    def _contains(self, node, x, y):
        return node.x <= x < node.x + node.width and node.y <= y < node.y + node.height
            
    def move(self, old_x, old_y, new_x, new_y, data):
        # 首先确认点是否存在于四叉树中
        if not self.remove(old_x, old_y, data):
            # 如果点不存在，返回错误或进行错误处理
            return False

        # 如果点确实被移除了，再将其重新插入
        self.insert(new_x, new_y, data)
        return True