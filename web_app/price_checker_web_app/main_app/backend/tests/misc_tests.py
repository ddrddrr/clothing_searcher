from random import randint
from itertools import chain
# TODO not tested if works
from web_app.price_checker_web_app.main_app.backend import misc as m


def test_merge_two_sorted_lists():
    assert m.merge_two_sorted_iterables([], []) == []
    assert m.merge_two_sorted_iterables([1], []) == [1]
    assert m.merge_two_sorted_iterables([], [2]) == [2]
    assert m.merge_two_sorted_iterables([1], [2]) == [1, 2]
    assert m.merge_two_sorted_iterables([2], [1]) == [1, 2]

    for i in range(500):
        main_lst = [[], []]
        for j in range(randint(0, 500)):
            main_lst[0].append(randint(-10000000, 100000000))
            main_lst[1].append(randint(-10000000, 100000000))

        assert m.merge_two_sorted_iterables(sorted(main_lst[0]), sorted(main_lst[1])) == sorted(
                main_lst[0] + main_lst[1])

    for i in range(500):
        main_lst = [[], []]
        for j in range(randint(0, 500)):
            main_lst[0].append(chr(randint(ord("A"), ord("Z"))))
            main_lst[1].append(chr(randint(ord("A"), ord("Z"))))

        assert m.merge_two_sorted_iterables(sorted(main_lst[0]), sorted(main_lst[1])) == sorted(
                main_lst[0] + main_lst[1])


def test_merge_k_sorted_lists():
    assert m.merge_k_sorted_iterables([[1]]) == [1]
    assert m.merge_k_sorted_iterables([[1], [1]]) == [1, 1]
    assert m.merge_k_sorted_iterables([[], [1]]) == [1]
    assert m.merge_k_sorted_iterables([[1], []]) == [1]

    for i in range(100):
        main_lst = []
        for j in range(100):
            main_lst.append([])

        assert m.merge_k_sorted_iterables(main_lst) == []

    for i in range(500):
        main_lst = []
        for j in range(randint(0, 100)):
            main_lst.append([])
            for k in range(randint(0, 100)):
                main_lst[j].append(randint(-1000000, 1000000))

        assert m.merge_k_sorted_iterables([sorted(lst) for lst in main_lst]) == sorted(
                list(chain.from_iterable(main_lst)))
