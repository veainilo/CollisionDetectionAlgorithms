class SpatialEntity:
    def __init__(self, x, y, width, height, data):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data = data

    def get_bounds(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def intersects(self, other):
        return not (self.x > other.x + other.width or
                    self.x + self.width < other.x or
                    self.y > other.y + other.height or
                    self.y + self.height < other.y)

class SpatialHash:
    def __init__(self, cell_size, width, height):
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.buckets = {}

    def _hash(self, entity):
        bounds = entity.get_bounds()
        return (
            int(bounds[0] // self.cell_size),
            int(bounds[1] // self.cell_size),
            int(bounds[2] // self.cell_size),
            int(bounds[3] // self.cell_size)
        )

    def insert(self, entity):
        bucket_keys = self._hash(entity)
        for i in range(bucket_keys[0], bucket_keys[2] + 1):
            for j in range(bucket_keys[1], bucket_keys[3] + 1):
                bucket_key = (i, j)
                if bucket_key not in self.buckets:
                    self.buckets[bucket_key] = {}
                self.buckets[bucket_key][(entity.x, entity.y, entity.width, entity.height)] = entity.data

    def query_range(self, query_entity):
        results = []
        bucket_keys = self._hash(query_entity)
        for i in range(bucket_keys[0], bucket_keys[2] + 1):
            for j in range(bucket_keys[1], bucket_keys[3] + 1):
                bucket_key = (i, j)
                if bucket_key in self.buckets:
                    for (item_x, item_y, item_w, item_h), item_data in self.buckets[bucket_key].items():
                        item_entity = SpatialEntity(item_x, item_y, item_w, item_h, item_data)
                        if query_entity.intersects(item_entity):
                            results.append(item_entity.data)
        return results

    def remove(self, entity):
        bucket_keys = self._hash(entity)
        removed = False
        for i in range(bucket_keys[0], bucket_keys[2] + 1):
            for j in range(bucket_keys[1], bucket_keys[3] + 1):
                bucket_key = (i, j)
                if bucket_key in self.buckets:
                    obj_key = (entity.x, entity.y, entity.width, entity.height)
                    if obj_key in self.buckets[bucket_key] and self.buckets[bucket_key][obj_key] == entity.data:
                        del self.buckets[bucket_key][obj_key]
                        removed = True
                        if not self.buckets[bucket_key]:
                            del self.buckets[bucket_key]
        return removed

    def move(self, old_entity, new_entity):
        if self.remove(old_entity):
            self.insert(new_entity)