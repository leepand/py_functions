# -*- coding: UTF-8 -*-
# 拉平多个list


def flatten(x):
    """
    >>> flatten([[1]])
    [1]
    >>> flatten([[1, 2], [3, 4]])
    [1, 2, 3, 4]
    >>> flatten([[[1], [2]], [[3], [4]]])
    [1, 2, 3, 4]
    """
    if isinstance(x[0], list):
        return list(toolz.concat(map(flatten, x)))
    else:
        return x
