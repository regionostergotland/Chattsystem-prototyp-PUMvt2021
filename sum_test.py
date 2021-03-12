import pytest
from sum import sum

# Setup
# install pytester
# to run type pytest putester.py in terminal in the same file


def test_sum1():
	assert sum(1, 2) == 3