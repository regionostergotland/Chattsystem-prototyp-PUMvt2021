import pytest

# Setup
# install pytester
# to run type pytest putester.py in terminal in the same file


def func(x):
    return x + 1


def test_shell1():
	assert func(0) == 1


def test_shell2():
	assert func(1) == 2
