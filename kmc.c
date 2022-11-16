#include "kmc.h"

#define WI 1.717 // interstitial jump rate prefactor
#define WV 0.001282 // vacancy
#define EI 1.37 // interstitial migration activation energy
#define EV 0.1 // vacancy

#define R_NN 2.35 // nearest neighbour distance in Si

#define STD_V 20. // standard deviation for vacancies
#define STD_I 60. // interstitials

#define KB 8.617333262e-5 // Boltzmann constant (eV/K)

// jump rate at temperature T
double jump_rate(double w, double E, double T)
{
	return w * exp(-E / T / KB);
}

// write positions of particles to file (can be played e.g. with Ovito)
double write_vi(FILE *fd, vec3 *vi, int n_v, int n_i, double t, int t_step)
{
	int n = n_v+n_i;
	fprintf(fd, "%i\n", n); // number of "particles"
	fprintf(fd, "Time=%g, Timestep=%i Properties=type:I:1:id:I:1:pos:R:3\n", t, t_step); // timestep header
	int type = 0;
	for (int i = 0; i < n; ++i) {
		if (i >= n_v) type = 1; // type 0 = vacancy, type 1 = interstitial
		fprintf(fd, "%i %i %g %g %g\n", type, i, vi[i].x, vi[i].y, vi[i].z); // type, id, x, y, z
	}
}

/*
 * Kinetic Monte Carlo run with n_v vacancies and n_i interstitials in Si at
 * temperature temp. Recombination occurs at r <= r_rec. Simulation runs until
 * time t_end and output written every w_freq step to stdout and file fd.
 * Returns number of surviving defects and number of jumps for each 
 * defect type jumps_v and jumps_i.
 */
int kmc(int n_v, int n_i, double temp, double r_rec, double t_end, int w_freq,
	   FILE *fd, unsigned long *defects, unsigned long *jumps_v, unsigned long *jumps_i)
{
	double t = 0.; // simulation time (fs)
	int n_vi = n_v + n_i; // total of vacancies and interstitials

	*jumps_v = 0;
	*jumps_i = 0;
	
	vec3 *r_vi = malloc(sizeof(vec3) * n_vi); // allocate vacancies and interstitials contiguously in memory
	vec3 *r_v = r_vi; // positions of vacancies, size n_v
	vec3 *r_i = r_v + n_v; // positions of interstitials, size n_i

	double *g_vi = calloc(sizeof(double), n_vi); // rates of transitions
	double *g_v = g_vi; // vacancies
	double *g_i = g_v + n_v; // interstitials

	for (int i = 0; i < n_v; ++i) { // generate initial distribution of vacancies
		r_v[i] = vec3_random(); // direction uniformly distributed
		r_v[i] = vec3_mul(&r_v[i], fabs(gaussian(0., STD_V))); // r distributed as N(0, STD_V^2)
	}
	for (int i = 0; i < n_i; ++i) { // generate initial distribution of vacancies
		r_i[i] = vec3_random();
		r_i[i] = vec3_mul(&r_i[i], fabs(gaussian(0., STD_I)));
	}
	
	printf("t=%g, n_v=%i, n_i=%i, jumps_v=%lu, jumps_i=%lu\n", t, n_v, n_i, *jumps_v, *jumps_i);
	write_vi(fd, r_vi, n_v, n_i, t, 0); // write initial state
	
	for (int i = 0; t < t_end; ++i) {
		g_v[0] = jump_rate(WV, EV, temp); // calculate cumulative sum of transition rates
		for (int j = 1; j < n_v; ++j) { // vacancies
			g_v[j] = jump_rate(WV, EV, temp) + g_v[j - 1];
			//printf("%g\n", g_v[j]);
		}
		g_i[0] = jump_rate(WI, EI, temp) + g_v[n_v - 1];
		for (int j = 1; j < n_i; ++j) { // interstitials
			g_i[j] = jump_rate(WI, EI, temp) + g_i[j - 1];
			//printf("%g\n", g_i[j]);
		}
	
		double gtot = g_vi[n_vi - 1]; // total of transition rates
		double ug = genrand64_real3(); // random number [0, 1]

		for (int j = 0; j < n_vi; ++j) { // figure out which event occurs
			if (ug * gtot <= g_vi[j]) { // do transition for j
				vec3 dr = vec3_random(); // jump in random direction
				dr = vec3_mul(&dr, R_NN); // jump by nearest neighbour distance
				r_vi[j] = vec3_add(&r_vi[j], &dr);

				if (j < n_v)
					++*jumps_v; // this is a vacancy jump
				else
					++*jumps_i; // interstitial jump
				
				break;
			}
		}
		
		for (int jv = 0; jv < n_v; ++jv) {
			for (int ji = 0; ji < n_i; ++ji) {
				vec3 r = vec3_sub(&r_v[jv], &r_i[ji]);
				double d = vec3_norm(&r); // distance between r_v and r_i
				
				if (d <= r_rec) { // at recombination distance, remove vacancy and interstitial
					r_v[jv] = r_v[n_v - 1]; // move vacancy from end to this spot
					r_v[n_v - 1] = r_i[n_i - 1]; // last element of vacancy array becomes interstitial
					if (n_i > 1)
						r_i[ji] = r_i[n_i - 2];

					--r_i; // move interstitial array pointer back
					--n_v; // resize vacancy and interstitial arrays
					--n_i;
					n_vi -= 2;
				}
			}
		}

		double dt = -log(genrand64_real3()) / gtot; // determine timestep based on a random number and total transition rate
		t += dt;

		if (i % w_freq == 0) { // write state of system
			printf("t=%g, n_v=%i, n_i=%i, jumps_v=%lu, jumps_i=%lu\n", t, n_v, n_i, *jumps_v, *jumps_i);
			write_vi(fd, r_vi, n_v, n_i, t, i);
		}
	}

	free(r_vi);
	free(g_vi);

	*defects = n_v + n_i; // number of defects is vacancies + interstitials

	return 0;
}

int main(int argc, char *args[])
{
	init_genrand64(time(NULL)); // initialize Mersenne twister

	FILE *fd = fopen("vi.xyz", "w");

	double t_end = 1.e9; // end time (fs)
	int w_freq = 1000; // write frequency 1/step

	double temp = 1500.; // temperature (K)
	double r_rec = 4.; // recombination distance (Å)
	
	int n_v = 150; // initial number of vacancies and interstitials
	int n_i = 150; // initial number of interstitials

	int nruns = 1; // number of runs to average over

	if (argc < 8)
		printf("Usage: %s <number of vacancies> <number of interstitials> <temperature (K)> <recombination distance (Å)> <simulation time (fs)> <write frequency 1/step> <number of runs>", args[0]);
	else {
		n_v = atoi(args[1]);
		n_i = atoi(args[2]);
		temp = atof(args[3]);
		r_rec = atof(args[4]);
		t_end = atof(args[5]);
		w_freq = atoi(args[6]);
		nruns = atoi(args[7]);
		printf("n_v=%i, n_i=%i, temp=%g, r_rec=%g, t_end=%g, w_freq=%i, nruns=%i\n", n_v, n_i, temp, r_rec, t_end, w_freq, nruns);
	}

	double *f = malloc(sizeof(double) * nruns); // fraction of surviving defects
	double *r = malloc(sizeof(double) * nruns); // ratio of interstitial jumps to vacancy jumps
	double fs = 0., riv = 0.; // means for the above
	for (int i = 0; i < nruns; ++i) {
		printf("run %i\n", i+1);
		unsigned long defects, jumps_v, jumps_i;
		kmc(n_v, n_i, temp, r_rec, t_end, w_freq, fd, &defects, &jumps_v, &jumps_i);
	
		printf("defects=%lu, jumps_v=%lu, jumps_i=%lu\n", defects, jumps_v, jumps_i);
		double fi = (double) defects / (double) (n_v + n_i);
		double ri = (double) jumps_i / (double) jumps_v;
		f[i] = fi;
		r[i] = ri;
		fs += fi / (double) nruns;
		riv += ri / (double) nruns;
	}

	double fs_err = 0., riv_err = 0.;
	for (int i = 0; i < nruns && nruns > 1; ++i) { // calculate errors from sample standard deviation
		fs_err += (f[i] - fs) * (f[i] - fs) / (double) (nruns - 1);
		riv_err += (r[i] - riv) * (r[i] - riv) / (double) (nruns - 1);
	}
	fs_err = sqrt(fs_err);
	riv_err = sqrt(riv_err);
	
	printf("fraction surviving: %.20g +- %.20g\n", fs, fs_err);
	printf("ratio i/v: %.20g +- %.20g\n", riv, riv_err);
	
	return 0;
}

