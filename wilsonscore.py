# Code to compute wilsonscore confidence interval
from scipy.special import ndtri
import numpy as np


def rb_wilsonscore(count, nobs, confint):
    # -----------------------------------------------------------------------------------
    # This function computes the wilson score confidence intervals Score Interval for a binomial distribution.
    #
    #     Input :     count   =    Number of successes
    #                 nobs    =    Number of total Trials
    #                 confint =    Confindence interval for which Wilson Score is computed [e.g. confint =0.95 2\sigma]
    #
    #     Output
    # 				  center =  gives the center of the score intervals given the data
    #                 hi     =   Upper bound for given confint
    #                 lo     =   Lower bound for given confint
    #
    #     Example:    import rb_wilsonscore as w
    #                 XC, hi, lo = w.rb_wilsonscore(10.,20.,.95)
    #
    #     Written by :   Rongmon Bordoloi  Nov 2017
    #     Tested on  : Python 2.7, 3.x
    # -----------------------------------------------------------------------------------
    count = np.double(count)
    nobs = np.double(nobs)
    confint = np.double(confint)
    # Written by RB
    if nobs == 0.0:
        return (0.0, 0.5, 1.0)
    z = ndtri(1.0 - 0.5 * (1.0 - confint))
    p = count / nobs
    # now do it with Wilson score interval
    alpha = p + (z * z) / (2.0 * nobs)
    beta = ((p * (1.0 - p) / nobs) + ((z**2.0) / (4.0 * (nobs**2.0)))) ** 0.5
    center = (alpha) / (1.0 + ((z**2.0) / nobs))
    hi = (alpha + (z * beta)) / (1.0 + ((z**2.0) / nobs))
    lo = (alpha - z * (beta)) / (1.0 + ((z**2.0) / nobs))
    return (center, hi, lo)


rb_wilsonscore(10, 20, 0.95)
rb_wilsonscore(10, 20, 0.95)


def wilson_score(pos, total, p_z=2.0):
    """
    威尔逊得分计算函数
    参考：https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
    :param pos: 正例数
    :param total: 总数
    :param p_z: 正太分布的分位数
    :return: 威尔逊得分
    """
    pos_rat = pos * 1.0 / total * 1.0  # 正例比率
    score = (
        pos_rat
        + (np.square(p_z) / (2.0 * total))
        - (
            (p_z / (2.0 * total))
            * np.sqrt(4.0 * total * (1.0 - pos_rat) * pos_rat + np.square(p_z))
        )
    ) / (1.0 + np.square(p_z) / total)
    return score


wilson_score(10, 20, 2)

"""
Python implementation - Lower bound of Wilson score confidence interval for a Bernoulli parameter
- http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
- https://news.ycombinator.com/item?id=15131611
- https://stackoverflow.com/questions/10029588/python-implementation-of-the-wilson-score-interval/45965534
- https://stackoverflow.com/questions/10029588/python-implementation-of-the-wilson-score-interval/45965534#45965534
"""

import math

import scipy.stats as st


def get_z(confidence):
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    return z


def ci_lower_bound(pos, n, confidence=None, z=None):
    if n == 0:
        return 0
    if z is None:
        z = get_z(confidence)
    phat = 1.0 * pos / n
    return (
        phat
        + z * z / (2 * n)
        - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)
    ) / (1 + z * z / n)


ci_lower_bound(10, 20, confidence=0.95)


# Reddit Algo
# Rewritten code from /r2/r2/lib/db/_sorts.pyx

from math import sqrt


def _confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.0  # 1.0 = 85%, 1.6 = 95%
    phat = float(ups) / n
    return sqrt(
        phat + z * z / (2 * n) - z * ((phat * (1 - phat) + z * z / (4 * n)) / n)
    ) / (1 + z * z / n)


def confidence(ups, downs):
    if ups + downs == 0:
        return 0
    else:
        return _confidence(ups, downs)


# Reddit 公开了他们的代码，很方便就能找到。Reddit 是用 Python 实现的，源代码在 这里. 排名算法使用了 Pyrex (一个用来写 Python 的 C 扩展的语言) 来提高性能。这里为了方便说明，我用 Python 写了 他们的 Pyrex 代码.

# V1 :这个算法被称作热排名 (hot ranking),代码如下:
# Rewritten code from /r2/r2/lib/db/_sorts.pyx

from datetime import datetime, timedelta
from math import log

epoch = datetime(1970, 1, 1)


def epoch_seconds(date):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def score(ups, downs):
    return ups - downs


def hot(ups, downs, date):
    """The hot formula. Should match the equivalent function in postgres."""
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(order + sign * seconds / 45000, 7)
