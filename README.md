# Vacancy Interstitial Kinetic Monte Carlo

<p align="center">
<img src="https://user-images.githubusercontent.com/12766039/202262624-0dcd2c5a-86c5-44f9-9dbe-f67b3cf07799.png" width=70% height=70%>
<img src="https://user-images.githubusercontent.com/12766039/202262641-03219415-5a53-4307-adbd-4a1bd0e2e85e.png" width=70% height=70%>
</p>

Simulate movement of vacancies $n_v$ and interstitials $n_i$ in an amorphous solid (Si) using kinetic Monte Carlo. A Gaussian spherically symmetric initial distribution of vacancies and interstitials is generated, after which movement of defects is simulated by random jumps to nearest neighbour positions $r_{\text{nn}}$. If a vacancy and interstitial jump within a specified recombination distance $r_{\text{rc}}$, they disappear.

The vacancies and interstitials have a jump rate determined by

$$
\text{JR} = w \exp\left(\frac{-E_m}{k_B T}\right),
$$

at temperature $T$ with migration activation energy $E_m$. The transition that occurs is chosen from the cumulative rate

$$
\Gamma_i = \sum_{j=1}^i \text{JR}_j(T)
$$

using the condition

$$
U \Gamma_{\text{tot}} \leq \Gamma_i.
$$

where $U \sim \mathcal{U}(0, 1)$ a uniformly distributed random number. Time step is determined from the total transition rate $\Gamma_{\text{tot}}=n_v+n_i$ as

$$
\Delta t = \frac{-\ln(U)}{\Gamma_{\text{tot}}}.
$$

## Compilation and running

Compilation:

`make`

Usage: 

`./vikmc <number of vacancies> <number of interstitials> <temperature (K)> <recombination distance (Å)> <simulation time (fs)> <write frequency 1/step> <number of runs>`

Example: `./vikmc 150 150 1500 4 1.e9 1000 3`

Generate all results/plots:
	`./run.sh`

## Plotting

Plotting one log file:
	`./plot_log.py <out.log>`
	
Plotting one xyz file:
	`./plot_xyz.py <vi.xyz>`

