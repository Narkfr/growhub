import unittest
import redis
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from app import app, connect_mqtt, connect_redis, client, redisServer

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.client')
    def test_connect_mqtt_success(self, mock_client):
        mock_client.connect.return_value = None
        mock_client.loop_start.return_value = None
        connect_mqtt()
        mock_client.connect.assert_called_once()
        mock_client.loop_start.assert_called_once()

    @patch('app.client')
    def test_connect_mqtt_failure(self, mock_client):
        mock_client.connect.side_effect = Exception("Connection failed")
        with self.assertLogs(level='ERROR') as log:
            connect_mqtt()
            self.assertIn("❌ Error connecting to MQTT broker: Connection failed", log.output)

    @patch('app.redisServer')
    def test_connect_redis_success(self, mock_redis):
        mock_redis.ping.return_value = True
        connect_redis()
        mock_redis.ping.assert_called_once()

    @patch('app.redisServer')
    def test_connect_redis_failure(self, mock_redis):
        mock_redis.ping.side_effect = redis.ConnectionError
        with self.assertRaises(SystemExit):
            connect_redis()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'index.html', response.data)

    def test_chicken_route(self):
        response = self.app.get('/chicken')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'chicken.html', response.data)

    @patch('app.client')
    def test_mqtt_post_success(self, mock_client):
        mock_client.is_connected.return_value = True
        mock_client.publish.return_value = None
        response = self.app.post('/mqtt', json={"topic": "test", "message": "hello"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"topic": "test", "message": "hello"})

    @patch('app.client')
    def test_mqtt_post_failure(self, mock_client):
        mock_client.is_connected.return_value = False
        response = self.app.post('/mqtt', json={"topic": "test", "message": "hello"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "MQTT client is not connected"})

    @patch('app.redisServer')
    def test_redis_post_success(self, mock_redis):
        mock_redis.set.return_value = True
        response = self.app.post('/redis', json={"key": "test", "value": "hello"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"key": "test", "value": "hello"})

    @patch('app.redisServer')
    def test_redis_post_failure(self, mock_redis):
        mock_redis.set.side_effect = Exception("Redis error")
        response = self.app.post('/redis', json={"key": "test", "value": "hello"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Redis error"})

if __name__ == '__main__':
    unittest.main()