import numpy as np
from scipy.optimize import curve_fit
from scipy.optimize import minimize

def exp_model(t, A, tau):
    return A * np.exp(-t / tau)

def naive_bins(bin_list, t_sel, t_min, t_max):
    taus = []
    for nb in bin_list:
        counts, edges = np.histogram(t_sel, bins=nb, range=(t_min, t_max))
        centers = 0.5 * (edges[:-1] + edges[1:])
        mask = counts > 0

        popt, _ = curve_fit(
            exp_model,
            centers[mask],
            counts[mask],
            p0=[counts.max(), 2.0]
        )
        taus.append(popt[1])
    return taus

def signal_pdf(t, tau, t_min, t_max):
    norm = np.exp(-t_min / tau) - np.exp(-t_max / tau)
    return (1.0/tau) * np.exp(-t / tau) / norm

def background_pdf(t, t_min, t_max):
    return np.full_like(t, 1.0/(t_max - t_min))

def total_pdf(t, tau, P, t_min, t_max):
    return (P * signal_pdf(t, tau, t_min, t_max) + (1-P) * background_pdf(t, t_min, t_max))

def neg_log_likelihood(params, t, t_min, t_max):
    tau, P = params
    # Physical bounds
    if tau<=0 or P<0 or P>1:
        return np.inf
    
    pdf_vals = total_pdf(t, tau, P, t_min, t_max)

    # Numerical safety
    if np.any(pdf_vals<=0):
        return np.inf

    return -np.sum(np.log(pdf_vals))

def halflife_estimation(initial_guess, t_sel, t_min, t_max):
    result = minimize(
        neg_log_likelihood,
        x0=initial_guess,
        args=(t_sel, t_min, t_max),
        bounds=[(0.1, 10.0), (0.0, 1.0)],
        method="L-BFGS-B"
    )
    return result.x