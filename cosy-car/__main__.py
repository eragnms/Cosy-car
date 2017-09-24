# -*- coding: utf-8 -*-
# see https://softwareengineering.stackexchange.com/questions/333761/where-do-you-put-the-main-function-of-a-python-app
from . import helpers

def get_hmm():
    """Get a thought."""
    return 'hmmm...'


def hmm():
    """Contemplation..."""
    if helpers.get_answer():
        print(get_hmm())
