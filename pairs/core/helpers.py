"""Misc functions for app"""
from textwrap import wrap


def fmt_term(msg):
    """Formats text for terminal output"""
    return '\n'.join(wrap(msg, 80))
