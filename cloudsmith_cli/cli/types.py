"""CLI/Commands - Push packages."""
from __future__ import absolute_import, print_function, unicode_literals
import os


import click


class ExpandPath(click.Path):
   def convert(self, value, *args, **kwargs):
        value = os.path.expanduser(value)
        return super(ExpandPath, self).convert(value, *args, **kwargs)