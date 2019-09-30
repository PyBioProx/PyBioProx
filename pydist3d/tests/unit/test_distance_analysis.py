"""test_distance_analysis.py

Test distance_analysis submodule module

J. Metz <metz.jp@gmail.com>
"""

import os
import pytest
import numpy as np
from pydist3d import distance_analysis


def test_distance_analysis_none_inputs():
    with pytest.raises(AttributeError):
        distance_analysis.edge_to_edge(None, None)

def test_distance_analysis_wrong_num_inputs():
    with pytest.raises(TypeError):
        distance_analysis.edge_to_edge()
