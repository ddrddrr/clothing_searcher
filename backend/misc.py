from typing import List, Any, Union, Optional, Tuple


def merge_two_sorted_iterables(lst1: Union[List[Any], Tuple[Any]],
                               lst2: Union[List[Any], Tuple[Any]]) -> List[Any]:
    if not lst1:
        return lst2
    if not lst2:
        return lst1

    i = 0
    j = 0
    res = []
    while i < len(lst1) or j < len(lst2):
        if i >= len(lst1):
            res.extend(lst2[j:])
            return res

        if j >= len(lst2):
            res.extend(lst1[i:])
            return res

        if lst1[i] < lst2[j]:
            res.append(lst1[i])
            i += 1
        else:
            res.append(lst2[j])
            j += 1

    return res


def merge_k_sorted_iterables(lists: List[Union[List[Any], Tuple[Any]]]) -> List[Any]:
    if len(lists) == 0:
        return []

    if len(lists) == 1:
        return lists[0].copy()

    if len(lists) == 2:
        return merge_two_sorted_iterables(lists[0], lists[1])

    return merge_two_sorted_iterables(merge_k_sorted_iterables(lists[:len(lists) // 2]),
                                      merge_k_sorted_iterables(lists[len(lists) // 2:]))


def find_first_digit(string: str) -> Optional[int]:
    for i, char in enumerate(string):
        if char.isdigit():
            return i

    return None


def find_last_digit(string: str) -> Optional[int]:
    for i in range(len(string) - 1, -1, -1):
        char = string[i]
        if char.isdigit():
            return i

    return None
