import unittest

from src.app.utils.db.query import GenericQueryBuilder


class TestGenericQueryBuilder(unittest.TestCase):

    def test_insert(self):
        table = "users"
        data = {"name": "John", "age": 30, "email": "john@example.com"}
        expected_query = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
        expected_values = ["John", 30, "john@example.com"]

        query, values = GenericQueryBuilder.insert(table, data)

        self.assertEqual(query, expected_query)
        self.assertEqual(values, expected_values)

    def test_update(self):
        table = "users"
        data = {"name": "John Doe", "age": 31}
        where = {"id": 1}
        expected_query = "UPDATE users SET name = ?, age = ? WHERE id = ?"
        expected_values = ["John Doe", 31, 1]

        query, values = GenericQueryBuilder.update(table, data, where)

        self.assertEqual(query, expected_query)
        self.assertEqual(values, expected_values)

    def test_delete(self):
        table = "users"
        where = {"id": 1}
        expected_query = "DELETE FROM users WHERE id = ?"
        expected_values = [1]

        query, values = GenericQueryBuilder.delete(table, where)

        self.assertEqual(query, expected_query)
        self.assertEqual(values, expected_values)

    def test_select_with_all_parameters(self):
        table = "users"
        columns = ["id", "name", "email"]
        where = {"age": 30}
        order_by = "id"
        limit = 10
        expected_query = (
            '''SELECT id, name, email FROM users WHERE age = ? ORDER BY id LIMIT 10'''
        )
        expected_values = [30]

        query, values = GenericQueryBuilder.select(table, columns, where, order_by, limit)

        self.assertEqual(query, expected_query)
        self.assertEqual(values, expected_values)

    def test_select_with_minimum_parameters(self):
        table = "users"
        expected_query = "SELECT * FROM users"
        expected_values = []

        query, values = GenericQueryBuilder.select(table)

        self.assertEqual(query, expected_query)
        self.assertEqual(values, expected_values)

    def test_select_with_where_clause(self):
        table = "users"
        where = {"active": 1}
        expected_query = "SELECT * FROM users WHERE active = ?"
        expected_values = [1]

        query, values = GenericQueryBuilder.select(table, where=where)

        self.assertEqual(query, expected_query)
        self.assertEqual(values, expected_values)

    def test_update_single_column(self):
        """Test update method with a single column to update"""
        table = "users"
        data = {"name": "John Doe"}
        where = {"id": 1}
        expected_query = "UPDATE users SET name = ? WHERE id = ?"
        expected_values = ["John Doe", 1]
        query, values = GenericQueryBuilder.update(table, data, where)
        self.assertEqual(query, expected_query)
        self.assertEqual(values, expected_values)