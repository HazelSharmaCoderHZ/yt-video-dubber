from typing import List, TypeVar

T = TypeVar("T")


def chunk_list(items: List[T], chunk_size: int):
    """
    Yield successive chunks from a list.

    Example:
    [1,2,3,4,5], chunk_size=2

    ->
    [1,2]
    [3,4]
    [5]
    """

    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]