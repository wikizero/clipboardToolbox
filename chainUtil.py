"""
@Author  :   Name: Vance  Email: 937316808@qq.com
@Time    :   2019/07/07
@Desc    :   实现链式调用类
"""
import json
import heapq
import traceback

from collections import Iterable
from functools import reduce
from itertools import chain, groupby


class ChainUtil():
    def __init__(self, data):
        self.data = data

        # Make the function call simpler
        # self.list = self.list()
        # self.str = self.str()
        # self.dict = self.dict()
        # self.set = self.set()
        # self.tuple = self.tuple()

    def str(self, **kwargs):
        """
        :param kwargs: encoding=None, errors='strict'
        """
        return str(self.data, **kwargs)

    def join(self, sep=''):
        return sep.join(self.data)

    def list(self):
        return list(self.data)

    def dict(self, reverse: bool = False, **kwargs):
        ret = json.loads(self.data, **kwargs) if isinstance(self.data, str) else dict(self.data)
        return {v: k for k, v in ret.items()} if reverse else ret

    def set(self):
        return set(self.data)

    def tuple(self):
        return tuple(self.data)

    def max(self, n=1, key=None):
        return heapq.nlargest(n, self.data, key)

    def min(self, n=1, key=None):
        return heapq.nsmallest(n, self.data, key)

    def map(self, func):
        self.data = map(func, self.data)
        return self

    def filter(self, func):
        self.data = filter(func, self.data)
        return self

    def reduce(self, func):
        self.data = reduce(func, self.data)
        return self

    def chain(self):
        self.data = chain(*self.data)
        return self

    def flatten(self):
        """
        列表展平:
        [1, [2, [3], [4, [5, 6]]], []] -> [1, 2, 3, 4,  5, 6]
        :return: ChainUtil
        """
        ret = []
        caller = traceback.extract_stack()[-2][2]

        for el in self.data:
            if not isinstance(el, str) and isinstance(el, Iterable):
                ret += ChainUtil(el).flatten()
            else:
                ret += [el]
        if caller == self.flatten.__name__:
            return ret
        else:
            self.data = ret
            return self

    def group(self, n):
        """
        分组，N个元素为一组
        :return: ChainUtil
        """
        data = list(self.data)
        self.data = [data[idx:idx + n] for idx in range(0, len(data), n)]
        return self

    def groupby(self, key=None):
        """
        按连续性分组
        :return: ChainUtil
        """
        self.data = [(key, list(group)) for key, group in groupby(self.data, key)]
        return self

    def sort(self, key=None, reverse=False):
        """
        排序
        :return: ChainUtil
        """
        self.data = sorted(self.data, key=key, reverse=reverse)
        return self

    def unique(self):
        """
        去重
        [[1, 2], [1, 2], [1, 3]] -> [[1, 2], [1, 3]]
        :return: ChainUtil
        """
        ret = []
        for i in self.data:
            if i not in ret:
                ret.append(i)
        self.data = ret
        return self


if __name__ == '__main__':
    input = '12345678'
    print(ChainUtil('12345678').map(int).filter(lambda x: x & 1).reduce(lambda x, y: x * y).data)

    input = ['ABC', (1, 2), {3, 4}, range(5, 8)]
    print(ChainUtil(input).chain().list())

    input = [1, [2, [3], [4, [5, 6]]], []]
    print(ChainUtil(input).flatten().list())

    input = ['abc', 1, [2, [3, 4]], range(5, 8), [[]]]
    print(ChainUtil(input).flatten().list())

    input = [
        {'address': '5412 N CLARK', 'date': '07/01/2012'}, {'address': '5148 N CLARK', 'date': '07/04/2012'},
        {'address': '5800 E 58TH', 'date': '07/02/2012'}, {'address': '2122 N CLARK', 'date': '07/03/2012'},
        {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}, {'address': '1060 W ADDISON', 'date': '07/02/2012'},
        {'address': '4801 N BROADWAY', 'date': '07/01/2012'}, {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}, ]
    from operator import itemgetter

    print(ChainUtil(input).sort(itemgetter('date')).groupby(itemgetter('date')).list())

    input = range(10 ** 6)
    print(ChainUtil(input).max(5))

    input = 'ADEBCPYQ'
    print(ChainUtil(input).min(n=3))

    input = [(1, 'A'), (2, 'B')]
    print(ChainUtil(input).dict(reverse=True))

    input = [[1, 2], [1, 2], [5, 6]]
    print(ChainUtil(input).unique().list())

    input = 'abcdefghik'
    print(ChainUtil(input).map(str.upper).group(3).list())



