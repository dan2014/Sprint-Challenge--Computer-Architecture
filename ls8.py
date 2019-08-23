
"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load(sys.argv)
cpu.run()