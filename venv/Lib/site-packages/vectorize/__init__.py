import functools
import inspect


def partition(l, i=1):
    return (l[:i], l[i:])

def head(l, i=1):
    return tuple(l[:i]) + (l[i:], )

def truncate(n):
    def truncate_n(fn):
        def truncate_fn(*vargs, **kwargs):
            vargs, _ = partition(vargs, n)
            return fn(*vargs, **kwargs)
        return truncate_fn
    return truncate_n

def splat(fn):
    @functools.wraps(fn)
    def splat_fn(vargs, **kwargs):
        return fn(*vargs, **kwargs)
    return splat_fn


def unsplat(fn):
    @functools.wraps(fn)
    def unsplat_fn(*vargs, **kwargs):
        return fn(vargs, **kwargs)
    return unsplat_fn


def vectorize(fn):
    """
    Allows a function to accept one or more values,
    but internally deal only with a single item,
    and returning a list or a single item depending
    on what is desired.
    """

    is_method = inspect.ismethod(fn)

    if is_method:
        fn = functools.partial(fn, self)

    @functools.wraps(fn)
    def vectorized_function(*vargs, **kwargs):
        if is_method:
            self, values, vargs = head(vargs, 2)
        else:
            values, vargs = head(vargs, 1)

        wrap = not isinstance(values, (list, dict))
        should_unwrap = not kwargs.setdefault('wrap', False)
        unwrap = wrap and should_unwrap
        del kwargs['wrap']

        if isinstance(values, dict):
            keys = values.keys()
            values = values.values()

        if wrap:
            values = [values]

        results = [fn(value, *vargs, **kwargs) for value in values]

        if isinstance(values, dict):
            results = dict(zip(keys, results))

        if unwrap:
            results = results[0]

        return results

    return vectorized_function
