import string


def validating_pilish(context):
    remove_punctuation_context = context.translate(str.maketrans('', '', string.punctuation)).replace("\n", " ").strip()
    context_line = "".join(str(len(word)) for word in remove_punctuation_context.split(" "))
    rintime_pi_digits = "".join([str(n) for n in list(pi_digits(len(context_line)))])
    print(f"{context_line=}\n{rintime_pi_digits=}")
    return context_line in rintime_pi_digits


def pi_digits(x):
    """Generate x digits of Pi.
    https://gist.github.com/deeplook/4947835"""

    k, a, b, a1, b1 = 2, 4, 1, 12, 4
    while x > 0:
        p, q, k = k * k, 2 * k + 1, k + 1
        a, b, a1, b1 = a1, b1, p * a + q * a1, p * b + q * b1
        d, d1 = a / b, a1 / b1
        while d == d1 and x > 0:
            yield int(d)
            x -= 1
            a, a1 = 10 * (a % b), 10 * (a1 % b1)
            d, d1 = a / b, a1 / b1


def main():
    # http://www.cadaeic.net/pilish.htm
    case_context = """But a time I spent wandering in gloomy night;
Yon tower, tinkling chimewise, loftily opportune.
Out, up, and together came sudden to Sunday rite,
The one solemnly off to correct plenilune."""
    print(validating_pilish(case_context))


if __name__ == '__main__':
    main()
