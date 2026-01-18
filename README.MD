# Muon Lifetime Measurement via Unbinned Maximum Likelihood
## Overview

This project presents a full experimental data analysis pipeline to estimate the mean lifetime of the muon using real detector data. The analysis emphasises statistical rigour, correct treatment of detector effects, and likelihood-based inference, rather than curve fitting or textbook reproduction.

The final result is obtained using an unbinned maximum likelihood fit that accounts for:

- a finite observation window (truncation),

- background contamination from accidental coincidences,

- non-Gaussian uncertainty via likelihood profiling.

The project is designed to reflect the workflow and standards used in real experimental physics analyses.

All data used in this project is available from:

Duncan Carlsmith (2026). QuarkNet Muon Lifetime Explorer (https://www.mathworks.com/matlabcentral/fileexchange/114065-quarknet-muon-lifetime-explorer), MATLAB Central File Exchange. Retrieved January 2, 2026.  

## Scientific Objective

The primary scientific goal is to estimate the muon mean lifetime $\tau$ from observed decay-time data while correctly accounting for experimental limitations.

Specifically, the analysis aims to:

- infer $\tau$ from real experimental data,

- model background events explicitly,

- handle detector-imposed time cuts rigorously,

- quantify uncertainty without assuming Gaussian errors.

This is an experimental data analysis, not a detector simulation or a theoretical derivation.

## Data Description

The dataset consists of reconstructed candidate muon decay events recorded by a scintillator-based detector system. Each event corresponds to a start–stop coincidence consistent with a muon decay.

After initial inspection and cleaning, the following fields are used:

|Column | Description|
|---|---|
|`channel_numb` | Detector channel identifier (PMT pairing)|
|`julian_day` | The given julian day that the data was collected on|
|`start_decay` | Start time of the event (fraction of a Julian day)|
|`end_decay` | End time of the event (fraction of a Julian day)|

## Analysis Pipeline

The analysis follows a clearly defined pipeline, implemented modularly in the repository:

Raw data
   ↓
Data ingestion & cleaning
   ↓
Event selection & time window cuts
   ↓
Exploratory analysis
   ↓
Naïve binned fit (demonstration of limitations)
   ↓
Unbinned maximum likelihood fit
   ↓
Likelihood-based uncertainty estimation
   ↓
Validation on synthetic data


Each step is documented and justified in the analysis notebook.

## Event Selection

Only events satisfying:

$$t_{min}<t<t_{max}$$

are retained, where:

- $t_{min} ⁡=0.7 \mu s$ removes electronics-resolution effects
- $t_{max} ⁡=7.6 \mu s$ reflects the finite acquisition window

These cuts are fixed before fitting and treated as part of the experimental setup, not tuning parameters.

## Statistical Model
### Signal model

Muon decay is a memoryless process and is modelled as an exponential distribution:

$$f(t∣\tau)=\tfrac{1}{\tau} e^{−t/\tau},\space t≥0$$

Because only decays within the interval $(t_{min}, t_{max})$ are observed, the signal distribution is truncated and renormalised:

$$f_{sig}(t|\tau) = \dfrac{\tfrac{1}{\tau}e^{-t/\tau}}{e^{-t_{max}/\tau} - e^{-t_{min}/\tau}}\space (t_{min}<t<t_{max})$$

### Background model

Accidental coincidences and noise are modelled as a uniform distribution in decay time:

$$f_{bkg}(t) = \dfrac{1}{t_{max} - t_{min}}$$​

### Mixture model

Each event is assumed to be either signal or background. The total probability density is:

$$f(t|\tau, P) = P f_{sig}(t|\tau) + (1-P) f_{bkg}(t)$$

where $P$ is the signal fraction, treated as a nuisance parameter.

### Parameter Estimation

The parameters $\tau$ and $P$ are estimated using an unbinned maximum likelihood estimate fit. The likelihood for independent events is:

$$\mathcal{L}(\tau,P) = \prod_{i=1}^Nf(t_i|\tau,P)$$

For numerical stability, the negative log-likelihood is minimised using a bounded optimiser.

This approach:

- avoids information loss from binning,

- correctly accounts for truncation,

- allows for a principled treatment of background.

## Uncertainty Estimation

Statistical uncertainty on the muon lifetime is obtained via likelihood profiling.

For each fixed value of $\tau$, the likelihood is re-optimised with respect to the nuisance parameter $P$. The 68% confidence interval is defined by:

$$\Delta(-2\log\mathcal{L}(\tau)) = 1$$

according to Wilks’ theorem for one parameter of interest.

This method naturally yields asymmetric uncertainties, reflecting the non-Gaussian shape of the likelihood.

## Final Result

The measured muon lifetime is:

$$\tau = 2.118^{+0.067}_{-0.094}\space \mu s$$

The uncertainty represents the 68% confidence interval derived from the profile likelihood.

The result is consistent with the accepted muon lifetime within statistical uncertainty, given the detector size, background contamination, and finite observation window.

## Validation with Synthetic Data

The full analysis pipeline is validated using synthetic (“toy”) datasets generated with known input parameters.

- Signal events are drawn from a truncated exponential distribution.

- Background events are drawn from a uniform distribution.

- The same likelihood-based fit is applied.

The fitter successfully recovers the true lifetime within the estimated uncertainty, demonstrating that:

- the estimator is unbiased,

- the uncertainty estimation is reliable.

## Repository Structure
```
muon-lifetime/
├── data/
│   └── processed/
│   └── raw/
├── src/
│   ├── plots.py
│   ├── preprocessing.py
│   ├── simulation.py
│   └── validation.py
├── notebooks/
│   └── analysis.ipynb      # Main walkthrough of the project
├── README.md
└── environment.yml
```

## Notes and Limitations

- Detector physics is treated implicitly via the reconstructed decay times.

- Background is modelled as uniform; more complex models were not required by the data.

- Systematic uncertainties are limited to variations in the time window.

These choices are deliberate and appropriate for the scope of the dataset.

## Dependencies

Key Python packages:

- `numpy`

- `pandas`

- `scipy`

- `matplotlib`

See `environment.yml` for details.