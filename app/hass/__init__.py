#!/usr/bin/env python3
import re

def norm(s: str):
    s = re.sub(u"[\\W|_]", "", s)
    return s.lower()


def load_attr(key: str, data: dict, optional=False):
    value = None
    if not optional:
        assert key in data
    if key in data:
        value = data[key]
        del data[key]
    return value
