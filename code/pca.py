import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

from sklearn.decomposition import PCA
from matplotlib_inline.backend_inline import set_matplotlib_formats

set_matplotlib_formats('svg')

def percent_formatter(x, pos):
    return f"{x*100:.0f}%"

