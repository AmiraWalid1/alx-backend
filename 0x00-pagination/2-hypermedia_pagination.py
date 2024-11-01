#!/usr/bin/env python3
""" Server Class"""

import csv
import math
from typing import List, Tuple


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes the Server with a cached dataset."""
        self.__dataset = None

    def dataset(self) -> List[List[str]]:
        """
        Returns the cached dataset of baby names.

        If the dataset is not already loaded, it reads from the CSV file,
        caches it,
        and then returns the dataset excluding the header row.

        Returns:
            List[List[str]]: A list of lists, where each inner list represents
            a row in the CSV file.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Exclude header row
        return self.__dataset

    def index_range(self, page: int, page_size: int) -> Tuple[int, int]:
        """
        Calculates the start and end index for pagination.

        Given a page number and page size, this method returns the
        range of indices to return for that page.

        Parameters:
            page (int): The page number (1-indexed).
            page_size (int): The number of items per page.

        Returns:
            Tuple[int, int]: A tuple containing the start index (inclusive)
            and end index (exclusive).
        """
        return (page - 1) * page_size, page * page_size

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List[str]]:
        """
        Retrieves a page of data for pagination.

        Ensures the page and page_size parameters are positive integers,
        then returns the requested page of data from the dataset. If the
        requested page exceeds the dataset length, it returns an empty list.

        Parameters:
            page (int): The page number (1-indexed).
            page_size (int): The number of items per page.

        Returns:
            List[List[str]]: A list of lists representing the data
            for the given page.
        """
        assert isinstance(page, int) and page > 0, \
            "Page must be a positive integer."
        assert isinstance(page_size, int) and page_size > 0, \
            "Page size must be a positive integer."

        start_index, end_index = self.index_range(page, page_size)
        data = self.dataset()

        if start_index >= len(data):
            # Return an empty list if the page exceeds the dataset size
            return []
        return data[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Returns a dictionary with pagination information and metadata.

        Parameters:
            page (int): The current page number (1-indexed).
            page_size (int): The number of items per page.

        Returns:
            dict: A dictionary with keys:
                - "page_size" (int): The size of each page.
                - "page" (int): The current page number.
                - "data" (List[List[str]]): The data for the specified page.
                - "next_page" (int or None): The number of the next page,
                   or None if there is no next page.
                - "prev_page" (int or None): The number of the previous page,
                   or None if there is no previous page.
                - "total_pages" (int): The total number of pages.
        """
        data = self.get_page(page, page_size)
        total_pages = (len(self.dataset()) + page_size - 1) // page_size
        next_page = None if page >= total_pages else page + 1
        prev_page = None if page <= 1 else page - 1
        return {
            "page_size": page_size,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages,
        }
