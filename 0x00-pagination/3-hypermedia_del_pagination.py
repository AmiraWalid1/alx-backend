#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes the Server."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> dict:
        """
        Returns a dictionary with pagination information, resilient to deletions.

        Parameters:
            index (int): The starting index (0-based).
            page_size (int): The number of items per page.

        Returns:
            Dict: A dictionary containing 'index', 'data', 'page_size', and 'next_index'.
        """
        assert index is not None and 0 <= index < len(self.dataset()), "Out of range"
        data = []
        curr_index = index
        cnt = 0
        while cnt < page_size and curr_index < len(self.dataset()):
            if curr_index in self.indexed_dataset():
                data.append(self.__indexed_dataset[curr_index])
                cnt += 1
            curr_index += 1
        return {
            "index": index,
            "next_index": curr_index,
            "page_size": page_size,
            "data": data,
        }
