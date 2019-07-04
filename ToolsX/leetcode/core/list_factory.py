import random


class ListFactory():
    @classmethod
    def from_iter(cls, iterable):
        return [int(i) for i in iterable]

    @classmethod
    def from_args(cls, *args):
        return cls.from_iter(list(args))

    @classmethod
    def from_str(cls, values: str):
        return cls.from_iter(values)

    @classmethod
    def from_num(cls, num: int):
        return cls.from_str(str(num))

    @classmethod
    def create(cls, length=5, start=1, rand_max=10, rand=False):
        return [i if not rand else random.randint(start, rand_max) for i in range(start, start + length)]

    @classmethod
    def random(cls, length=5, **kwargs):
        return cls.create(length, rand=True, **kwargs)
