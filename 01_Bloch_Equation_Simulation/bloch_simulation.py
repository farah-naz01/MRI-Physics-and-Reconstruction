"""Educational Bloch equation simulation in the rotating frame (on resonance)."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def bloch_rhs(t, m, t1, t2, m0=1.0, omega1=0.0):
    """Bloch equations with an RF field along +x in the rotating frame.

    omega1 is the signed RF angular frequency in radians per millisecond.
    """
    mx, my, mz = m
    return [-mx / t2, omega1 * mz - my / t2,
            -omega1 * my + (m0 - mz) / t1]


def simulate(t1=900.0, t2=90.0, duration=2000.0):
    times = np.linspace(0, duration, 1001)
    initial = [1.0, 0.0, 0.0]  # ideal 90-degree pulse: transverse magnetization
    sol = solve_ivp(bloch_rhs, (0, duration), initial,
                    args=(t1, t2, 1.0, 0.0), t_eval=times,
                    rtol=1e-9, atol=1e-11)
    if not sol.success:
        raise RuntimeError(sol.message)
    mx, my, mz = sol.y
    transverse = np.hypot(mx, my)
    return times, transverse, mz


def main():
    t1, t2 = 900.0, 90.0
    t, transverse, mz = simulate(t1, t2)
    expected_mz = 1 - np.exp(-t / t1)
    expected_mxy = np.exp(-t / t2)
    assert np.allclose(mz, expected_mz, atol=1e-7)
    assert np.allclose(transverse, expected_mxy, atol=1e-7)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(t, mz, label='Longitudinal recovery (Mz)')
    ax.plot(t, transverse, label='Transverse decay (Mxy)')
    ax.set(xlabel='Time (ms)', ylabel='Normalized magnetization',
           title='Bloch equation relaxation simulation')
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig('01_Bloch_Equation_Simulation/figures/relaxation.png', dpi=180)
    print('Saved 01_Bloch_Equation_Simulation/figures/relaxation.png')


if __name__ == '__main__':
    main()
