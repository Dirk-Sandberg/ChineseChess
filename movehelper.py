"""
Meant to make it easier to index between the two grids
Easy indices to think about would be:

0,2  1,2  2,2
0,1  1,1  2,1
0,0  1,0  2,0

Without the helper, the grids go like:
0,0  0,1  0,2
1,0  1,1  1,2
2,0  2,1  2,2
 -- RIVER --
0,0  0,1  0,2
1,0  1,1  1,2
2,0  2,1  2,2

"""
from kivy.app import App


NUM_COLS = 9
NUM_ROWS = 10




