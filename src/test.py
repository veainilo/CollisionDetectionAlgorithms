import random
import time
from QuadTree import QuadTree
from SpatialHash import SpatialHash, SpatialEntity

def performance_test1(spatial_index, num_insertions: int, num_queries: int, num_movements: int, num_removals: int, seed: int = 0):
    random.seed(seed)
    
    # Prepare a list to keep track of inserted points for later removal and moving
    inserted_points = []

    # 插入随机点并将其添加到空间索引中
    start_time = time.time()
    for _ in range(num_insertions):
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        point_data = f"Point({x},{y})"
        spatial_index.insert(x, y, point_data)
        inserted_points.append((x, y, point_data))
    end_time = time.time()
    print(f"Inserted {num_insertions} points in {end_time - start_time} seconds")

    # 随机生成查询矩形并查询空间索引
    query_results = []
    start_time = time.time()
    for _ in range(num_queries):
        qx = random.uniform(0, 1000)
        qy = random.uniform(0, 1000)
        qwidth = random.uniform(1, 100)
        qheight = random.uniform(1, 100)
        result = spatial_index.query_range(qx, qy, qwidth, qheight)
        query_results.append(result)
    end_time = time.time()
    print(f"Performed {num_queries} rectangular range queries in {end_time - start_time} seconds")

    # 随机移动已插入的点
    start_time = time.time()
    for _ in range(num_movements):
        old_x, old_y, point_data = random.choice(inserted_points)
        new_x = random.uniform(0, 1000)
        new_y = random.uniform(0, 1000)
        spatial_index.move(old_x, old_y, new_x, new_y, point_data)
        inserted_points.append((new_x, new_y, point_data))
    end_time = time.time()
    print(f"Moved {num_movements} points in {end_time - start_time} seconds")

    # 随机移除已插入的点
    start_time = time.time()
    for _ in range(num_removals):
        if inserted_points:
            x, y, point_data = inserted_points.pop()
            spatial_index.remove(x, y, point_data)
    end_time = time.time()
    print(f"Removed {num_removals} points in {end_time - start_time} seconds")

    # 输出第一次查询返回的点的数量
    if query_results:
        print(f"Query 1 returned {len(query_results[0])} points")
        

def performance_test2(spatial_index, num_insertions: int, num_queries: int, num_movements: int, num_removals: int, seed: int = 0):
    random.seed(seed)
    
    # Prepare a list to keep track of inserted entities for later removal and moving
    inserted_entities = []

    # Insert random entities and add them to the spatial index
    start_time = time.time()
    for _ in range(num_insertions):
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        w = random.uniform(1, 10)  # Assign a small width
        h = random.uniform(1, 10)  # Assign a small height
        data = f"Entity({x},{y})"
        entity = SpatialEntity(x, y, w, h, data)
        spatial_index.insert(entity)
        inserted_entities.append(entity)
    end_time = time.time()
    print(f"Inserted {num_insertions} entities in {end_time - start_time} seconds")

    # Perform rectangular range queries on the spatial index
    query_results = []
    start_time = time.time()
    for _ in range(num_queries):
        qx = random.uniform(0, 1000)
        qy = random.uniform(0, 1000)
        qwidth = random.uniform(1, 100)
        qheight = random.uniform(1, 100)
        query_entity = SpatialEntity(qx, qy, qwidth, qheight, None)
        result = spatial_index.query_range(query_entity)
        query_results.append(result)
    end_time = time.time()
    print(f"Performed {num_queries} rectangular range queries in {end_time - start_time} seconds")

    # Randomly move inserted entities
    start_time = time.time()
    for _ in range(num_movements):
        entity = random.choice(inserted_entities)
        new_x = random.uniform(0, 1000)
        new_y = random.uniform(0, 1000)
        new_entity = SpatialEntity(new_x, new_y, entity.width, entity.height, entity.data)
        spatial_index.move(entity, new_entity)
    end_time = time.time()
    print(f"Moved {num_movements} entities in {end_time - start_time} seconds")

    # Randomly remove inserted entities
    start_time = time.time()
    for _ in range(num_removals):
        if inserted_entities:
            entity = inserted_entities.pop()
            spatial_index.remove(entity)
    end_time = time.time()
    print(f"Removed {num_removals} entities in {end_time - start_time} seconds")

    # Output the number of entities returned by the first query
    if query_results:
        print(f"Query 1 returned {len(query_results[0])} entities")


print("QuadTree:")
performance_test1(QuadTree(0, 0, 1000, 1000, 10), num_insertions=10000, num_queries=10000, num_movements=10000, num_removals=10000)

print("\nSpatialHash:")
performance_test2(SpatialHash(10, 1000, 1000), num_insertions=10000, num_queries=10000, num_movements=10000, num_removals=10000)