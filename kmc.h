/*
 * Simulate movement of vacancies and interstitials in a solid using
 * kinetic Monte Carlo
 * Roni Koitermaa 2022
 */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

// Mersenne twister random number generator
#include "mt64.h"

// Kinetic Monte Carlo simulation of vacancies and interstitials
int kmc(int n_v, int n_i, double temp, double r_rec, double t_end, int w_freq,
	  FILE *fd, unsigned long *defects, unsigned long *jumps_v, unsigned long *jumps_i);

// Gaussian random numbers N(0, 1)
double box_muller()
{
	return sqrt(-2. * log(genrand64_real3())) * cos(2. * M_PI * genrand64_real3());
}

// Gaussian random numbers N(mu, sigma^2)
double gaussian(double mu, double sigma)
{
	return box_muller() * sigma + mu;
}

// 3D Cartesian vector type
typedef struct {
	double x;
	double y;
	double z;
} vec3;

// constructor for vector
vec3 Vec3(double x, double y, double z)
{
	vec3 v;
	v.x = x;
	v.y = y;
	v.z = z;
	return v;
}

// print vector
double vec3_print(vec3 *a)
{
	printf("%g %g %g\n", a->x, a->y, a->z);
}

// length of vector
double vec3_norm(vec3 *a)
{
	return sqrt(a->x*a->x + a->y*a->y + a->z*a->z);
}

// add two vectors
vec3 vec3_add(vec3 *a, vec3* b)
{
	return Vec3(a->x+b->x, a->y+b->y, a->z+b->z);
}

// subtract two vectors
vec3 vec3_sub(vec3 *a, vec3* b)
{
	return Vec3(a->x-b->x, a->y-b->y, a->z-b->z);
}

// multiply vector with scalar
vec3 vec3_mul(vec3 *a, double s)
{
	return Vec3(a->x*s, a->y*s, a->z*s);
}

// generate uniformly distributed vector direction
vec3 vec3_random()
{
	double phi = 2. * M_PI * genrand64_real3(); // azimuth [0, 2 pi]
	double theta = acos(2. * genrand64_real3() - 1.); // inclination [-pi, pi]

	return Vec3(sin(theta) * cos(phi), // spherical to cartesian
			sin(theta) * sin(phi),
			cos(theta));
}

