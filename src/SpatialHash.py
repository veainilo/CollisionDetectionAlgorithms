class SpatialEntity:
    def __init__(self, x, y, width, height, data):
        self.x, self.y, self.width, self.height, self.data = x, y, width, height, data

    def get_bounds(self):
        return self.x, self.y, self.x + self.width, self.y + self.height

    def intersects(self, other):
        return not (self.x > other.x + other.width or self.x + self.width < other.x or
                    self.y > other.y + other.height or self.y + self.height < other.y)

class SpatialHash:
    def __init__(self, cell_size, width, height):
        self.cell_size, self.width, self.height, self.buckets = cell_size, width, height, {}

    def _hash(self, entity):
        x1, y1, x2, y2 = entity.get_bounds()
        return int(x1 // self.cell_size), int(y1 // self.cell_size), int(x2 // self.cell_size), int(y2 // self.cell_size)

    def insert(self, entity):
        for i in range(*self._hash(entity)[:2]):
            for j in range(*self._hash(entity)[1:3]):
                self.buckets.setdefault((i, j), {})[(entity.x, entity.y, entity.width, entity.height)] = entity.data

    def query_range(self, query_entity):
        results = []
        for i in range(*self._hash(query_entity)[:2]):
            for j in range(*self._hash(query_entity)[1:3]):
                bucket = self.buckets.get((i, j), {})
                for (x, y, w, h), data in bucket.items():
                    if query_entity.intersects(SpatialEntity(x, y, w, h, data)):
                        results.append(data)
        return results

    def remove(self, entity):
        removed = False
        for i in range(*self._hash(entity)[:2]):
            for j in range(*self._hash(entity)[1:3]):
                bucket = self.buckets.get((i, j))
                if bucket:
                    key = (entity.x, entity.y, entity.width, entity.height)
                    if bucket.pop(key, None) is not None:
                        removed = True
                        if not bucket:
                            self.buckets.pop((i, j))
        return removed

    def move(self, old_entity, new_entity):
        self.remove(old_entity)
        self.insert(new_entity)