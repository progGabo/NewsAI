import os, sys
import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
import pandas as pd
import cProfile
import io
import pstats
from io import StringIO
srcpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(srcpath)
from utils.dbconnector import get_mongo_client, MongoDBClientSingleton

# Importované funkcie, ktoré chcete testovať
from utils.dbconnector import (
    get_mongo_client,
    content_manager,
    insert_document,
    find_one_document,
    append_to_document,
    find_documents,
    fetch_and_combine_articles
)

class TestMongoDBClientSingleton(unittest.TestCase):
    
    @patch("utils.dbconnector.MongoClient")
    def test_repeated_connections_profile(self, mock_mongo_client):
        """
        Test that repeated calls to get_mongo_client use the same MongoDB instance.
        """
        mock_instance = MagicMock()
        mock_mongo_client.return_value = mock_instance
        profiler = cProfile.Profile()
        profiler.enable()

        clients = [get_mongo_client() for _ in range(1000)]

        profiler.disable()

        profiler_output = StringIO()
        stats = pstats.Stats(profiler, stream=profiler_output)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

        print("\n[Profiling Results]")
        print(profiler_output.getvalue())

        for client in clients:
            self.assertIs(client, clients[0])

        mock_instance.__getitem__.assert_called_with("news_ai")

if __name__ == "__main__":
    unittest.main()