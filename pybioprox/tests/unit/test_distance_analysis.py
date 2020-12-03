"""test_distance_analysis.py

Test distance_analysis submodule module

Copyright (C) 2020  Jeremy Metz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import pytest
import numpy as np
from pybioprox import distance_analysis


def test_distance_analysis_none_inputs():
    with pytest.raises(AttributeError):
        distance_analysis.edge_to_edge(None, None)

def test_distance_analysis_wrong_num_inputs():
    with pytest.raises(TypeError):
        distance_analysis.edge_to_edge()
