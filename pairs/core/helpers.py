"""Misc helper funcs"""
from textwrap import wrap


def ft(msg):
    """Format a message for the terminal"""
    return '\n'.join(wrap(msg, 80))

