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
        Provides pagination with resilience to deletions by returning
        a dictionary containing pagination information starting
        from a specific index.

        This method ensures that if items are deleted from the dataset,
        pagination remains accurate by skipping missing entries.

        Parameters:
            index (int): The starting index in the dataset (0-indexed).
            page_size (int): The number of items to include in the page.

        Returns:
            dict: A dictionary containing:
                - "index" (int): The starting index for the current page.
                - "data" (List[List[str]]): The list of items
                    on the current page.
                - "page_size" (int): The number of items on the current page.
                - "next_index" (int): The index to start the next page.
        """
        assert (index <= len(self.dataset())), "Out of range"
        data = []
        curr_index = index
        cnt = 0
        while (cnt < page_size):
            if (curr_index in self.__indexed_dataset.keys()):
                data.append(self.__indexed_dataset[curr_index])
                cnt += 1
            curr_index += 1
        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": curr_index,
        }
