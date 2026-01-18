import numpy as np

def generate_signal(n, tau, t_min, t_max):
    u = np.random.uniform(
        np.exp(-t_max / tau),
        np.exp(-t_min / tau),
        size=n
    )
    return -tau * np.log(u)

def generate_background(n, t_min, t_max):
    return np.random.uniform(t_min, t_max, size=n)

def generate_toy_data(n, tau, P, t_min, t_max):
    n_sig = int(n * P)
    n_bkg = n - n_sig

    t_sig = generate_signal(n_sig, tau, t_min, t_max)
    t_bkg = generate_background(n_bkg, t_min, t_max)

    return np.concatenate([t_sig, t_bkg])