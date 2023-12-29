class SpatialHash:
    def __init__(self, cell_size, width, height):
        self.cell_size = cell_size  # size of each cell in the grid
        self.width = width
        self.height = height
        self.buckets = {}  # store data in a dict based on grid location

    def _hash(self, x, y):
        # Compute the hash value based on the cell size
        return (int(x // self.cell_size), int(y // self.cell_size))

    def insert(self, x, y, data):
        # Insert the data into the correct bucket based on its position
        bucket_key = self._hash(x, y)
        if bucket_key not in self.buckets:
            self.buckets[bucket_key] = {}
        # Use a tuple of (x, y) as the key for quick lookup
        self.buckets[bucket_key][(x, y)] = data

    def query_range(self, x, y, width, height):
        # Query data within a given range
        results = []
        # Determine the range of cells that the query box intersects
        min_key = self._hash(x, y)
        max_key = self._hash(x + width, y + height)
        
        # Iterate over the range of relevant cells
        for i in range(min_key[0], max_key[0] + 1):
            for j in range(min_key[1], max_key[1] + 1):
                bucket_key = (i, j)
                if bucket_key in self.buckets:
                    # Check each item in the bucket to see if it falls within the query range
                    for (item_x, item_y), item_data in self.buckets[bucket_key].items():
                        if (x <= item_x < x + width) and (y <= item_y < y + height):
                            results.append(item_data)
        return results

    def remove(self, x, y, data):
        # 根据其位置从正确的存储桶中移除数据
        bucket_key = self._hash(x, y)
        if bucket_key in self.buckets:
            # Use the tuple (x, y) to directly access the item
            if (x, y) in self.buckets[bucket_key] and self.buckets[bucket_key][(x, y)] == data:
                del self.buckets[bucket_key][(x, y)]  # 直接删除
                if not self.buckets[bucket_key]:
                    del self.buckets[bucket_key]  # 如果存储桶为空，则移除存储桶
                return True
        return False

    def move(self, old_x, old_y, new_x, new_y, data):
        # 尝试从旧位置移除项目
        if self.remove(old_x, old_y, data):
            # 仅当移除成功时才在新位置插入项目
            self.insert(new_x, new_y, data)