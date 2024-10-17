import numpy as np
import scipy.stats as st
from scipy.special import gamma

from ._d_table import _D_TABLE, D


def d(m: int, sim_size: int = 100_000) -> D:
    """Correction factors for the R and X control charts.

    Args:
        m: Size of each sample.
        sim_size: Number of simulations performed to estimate d2 and d3 if no
                  predifined value is available.

    Returns:
        D: Dataclass with the corrisponding d2 and d3 value.
    """
    if m < 2:
        raise ValueError("The sample size m has to be >= 2.")

    if m in _D_TABLE:
        return _D_TABLE[m]

    x = np.array(st.norm.rvs(size=(sim_size, m)))
    R_i = x.max(axis=1) - x.min(axis=1)
    d2 = np.mean(R_i)
    d3 = np.std(R_i, ddof=1)
    return D(d2=d2, d3=d3)


def c4(m: int) -> float:
    """Correction factor used for the s and corrisponding X control charts.

    Args:
        m: Size of each sample.

    Returns:
        float: Calculated c4 value.
    """
    return gamma(m / 2) / gamma((m - 1) / 2) * np.sqrt(2 / (m - 1))