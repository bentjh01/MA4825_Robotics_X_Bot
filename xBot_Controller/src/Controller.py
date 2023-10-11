"""
1. receives input of goal position. 
2. Calculates point paths to goal postion within space constraints
3. creates list of points on path from dynamic contraints e.g. acceleration etc
4. outputs a dictionary of {ID:position} at a publish rate
5. receives completed flag
6. checks position within tolerance
7. moves again to go to goal 
"""