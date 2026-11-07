import importlib.util
from pathlib import Path
import numpy as np

path = Path(__file__).resolve().parents[1] / '01_Bloch_Equation_Simulation' / 'bloch_simulation.py'
spec = importlib.util.spec_from_file_location('bloch_simulation', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_relaxation_matches_analytic_solution():
    t, mxy, mz = module.simulate(t1=900, t2=90, duration=1000)
    np.testing.assert_allclose(mz, 1 - np.exp(-t / 900), atol=1e-7)
    np.testing.assert_allclose(mxy, np.exp(-t / 90), atol=1e-7)


def test_equilibrium():
    result = module.bloch_rhs(0, [0, 0, 1], 900, 90)
    np.testing.assert_allclose(result, [0, 0, 0])
