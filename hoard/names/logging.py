import functools
import io
import logging
from typing import Any, Callable, cast, TypeVar

import click
from smart_open import open


logger = logging.getLogger(__name__)


F = TypeVar("F", bound=Callable[..., Any])


def s3_log(f: F) -> F:
    @functools.wraps(f)
    @click.pass_context
    def wrapped(ctx, *args, **kwargs):
        logger.propagate = False
        logger.setLevel(logging.INFO)
        stream = io.StringIO()
        hdlr = logging.StreamHandler(stream)
        hdlr.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(hdlr)
        try:
            res = ctx.invoke(f, *args, **kwargs)
        finally:
            if (filename := ctx.params.get("name_log")) :
                with open(filename, "w") as fp:
                    fp.write(stream.getvalue())
        return res

    return cast(F, wrapped)


def log(f: F) -> F:
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        for x in f(*args, **kwargs):
            logger.info(x)
            yield x

    return cast(F, wrapped)
