import unittest
from ..src.SpatialHash import SpatialEntity, SpatialHash

class TestSpatialHash(unittest.TestCase):
    def setUp(self):
        self.spatial_hash = SpatialHash(10, 100, 100)

    def test_insert(self):
        entity = SpatialEntity(10, 10, 20, 20, 'Entity1')
        self.spatial_hash.insert(entity)
        self.assertIn((entity.x, entity.y, entity.width, entity.height), self.spatial_hash.buckets[(1, 1)])

    def test_query_range(self):
        entity1 = SpatialEntity(10, 10, 20, 20, 'Entity1')
        entity2 = SpatialEntity(30, 30, 40, 40, 'Entity2')
        self.spatial_hash.insert(entity1)
        self.spatial_hash.insert(entity2)
        results = self.spatial_hash.query_range(SpatialEntity(0, 0, 50, 50, 'QueryEntity'))
        self.assertEqual(len(results), 2)
        self.assertIn('Entity1', results)
        self.assertIn('Entity2', results)

    def test_remove(self):
        entity = SpatialEntity(10, 10, 20, 20, 'Entity1')
        self.spatial_hash.insert(entity)
        self.assertTrue(self.spatial_hash.remove(entity))
        self.assertNotIn((entity.x, entity.y, entity.width, entity.height), self.spatial_hash.buckets.get((1, 1), {}))

    def test_move(self):
        old_entity = SpatialEntity(10, 10, 20, 20, 'Entity1')
        new_entity = SpatialEntity(30, 30, 40, 40, 'Entity1')
        self.spatial_hash.insert(old_entity)
        self.spatial_hash.move(old_entity, new_entity)
        self.assertNotIn((old_entity.x, old_entity.y, old_entity.width, old_entity.height), self.spatial_hash.buckets.get((1, 1), {}))
        self.assertIn((new_entity.x, new_entity.y, new_entity.width, new_entity.height), self.spatial_hash.buckets[(3, 3)])

if __name__ == '__main__':
    unittest.main()