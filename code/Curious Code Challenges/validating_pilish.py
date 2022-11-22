import abc
import string
import timeit

from typing import Type

# http://www.cadaeic.net/pilish.htm
CASE_CONTEXT = """But a time I spent wandering in gloomy night;
Yon tower, tinkling chimewise, loftily opportune.
Out, up, and together came sudden to Sunday rite,
The one solemnly off to correct plenilune."""


class Spliter(abc.ABC):
    @abc.abstractmethod
    def to_split(self, context):
        raise NotImplementedError


class PySpliter(Spliter):
    def to_split(self, context):
        return context.split(" ")


class LazySpliter(Spliter):
    def to_split(self, context, split_on=string.whitespace):
        word = []
        for c in context:
            if c in split_on:
                if word:
                    yield "".join(word)
                    word = []
            else:
                word.append(c)
        if word:
            yield "".join(word)


class PilishValidater:
    def __init__(self, context, spliter: Type[Spliter] = None):
        self.context = context
        self.spliter: Type[Spliter] = spliter

    def get_pi_digits(self, n):
        """Generate n digits of Pi.
        https://gist.github.com/deeplook/4947835"""

        k, a, b, a1, b1 = 2, 4, 1, 12, 4
        while n > 0:
            p, q, k = k * k, 2 * k + 1, k + 1
            a, b, a1, b1 = a1, b1, p * a + q * a1, p * b + q * b1
            d, d1 = a / b, a1 / b1
            while d == d1 and n > 0:
                yield int(d)
                n -= 1
                a, a1 = 10 * (a % b), 10 * (a1 % b1)
                d, d1 = a / b, a1 / b1

    def replace_punctuation(self):
        return self.context.translate(str.maketrans('', '', string.punctuation)).replace("\n", " ").strip()

    def validating_pilish(self):
        runtime_context = self.spliter().to_split(self.replace_punctuation())
        runtime_context_len = "".join(map(lambda n: str(len(n)), runtime_context))
        runtime_pi_digits = "".join(map(str, self.get_pi_digits(len(list(runtime_context)))))
        return runtime_context_len == runtime_pi_digits
        # print(f"{runtime_context_len = }\n{runtime_pi_digits   = }")

    def run(self):
        self.validating_pilish()


def main():
    # pv1 = PilishValidater(CASE_CONTEXT, spliter=PySpliter)
    # pv1.validating_pilish()

    # pv2 = PilishValidater(CASE_CONTEXT, spliter=LazySpliter)
    # pv2.validating_pilish()

    print(timeit.timeit('PilishValidater(CASE_CONTEXT, spliter=PySpliter).run()',
                        setup="from __main__ import PilishValidater, CASE_CONTEXT, PySpliter", number=1000))
    print(timeit.timeit('PilishValidater(CASE_CONTEXT, spliter=LazySpliter).run()',
                        setup="from __main__ import PilishValidater, CASE_CONTEXT, LazySpliter", number=1000))


if __name__ == '__main__':
    main()
