#!/usr/bin/env python3
"""
This module provides a helper function, `index_range`, to calculate the start
and end indices for paginated data based on a given page number and page size.
"""


def index_range(page, page_size):
    """
    Return a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for pagination.

    Parameters:
    - page (int): The page number (1-indexed).
    - page_size (int): The number of items per page.

    Returns:
    - tuple: A tuple containing the start index and end index.
    """
    return ((page-1) * page_size, page * page_size)
