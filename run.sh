#!/bin/sh

nruns=10
# 150 vacancies and interstitials, 1µs, average 10 runs
# 500 K, r_rec = 4
echo "Running 500 K ${nruns} times..."
./vikmc 150 150 500 4 1.e9 100000 ${nruns} > out.log
grep -e fraction -e ratio out.log > fr500.log
echo "Running 1500 K ${nruns} times..."
# 1500 K
./vikmc 150 150 1500 4 1.e9 100000 ${nruns} > out.log
grep -e fraction -e ratio out.log > fr1500.log
echo "Running 2500 K ${nruns} times..."
# 2500 K
./vikmc 150 150 2500 4 1.e9 100000 ${nruns} > out.log
grep -e fraction -e ratio out.log > fr2500.log

echo "Running with r_rec=10 at 1500 K ${nruns} times..."
# 1500 K, r_rec = 10
./vikmc 150 150 1500 10 1.e9 100000 ${nruns} > out.log
grep -e fraction -e ratio out.log > fr10.log

# plot
echo "Doing 3 runs for plotting at 500 K..."
./vikmc 150 150 500 4 1.e9 1000 1 > out500_1.log
./vikmc 150 150 500 4 1.e9 1000 1 > out500_2.log
./vikmc 150 150 500 4 1.e9 1000 1 > out500_3.log
cp vi.xyz vi500.xyz
echo "Doing 3 runs for plotting at 1500 K..."
./vikmc 150 150 1500 4 1.e9 1000 1 > out1500_1.log
./vikmc 150 150 1500 4 1.e9 1000 1 > out1500_2.log
./vikmc 150 150 1500 4 1.e9 1000 1 > out1500_3.log
cp vi.xyz vi1500.xyz
echo "Doing 3 runs for plotting at 2500 K..."
./vikmc 150 150 2500 4 1.e9 1000 1 > out2500_1.log
./vikmc 150 150 2500 4 1.e9 1000 1 > out2500_2.log
./vikmc 150 150 2500 4 1.e9 1000 1 > out2500_3.log
cp vi.xyz vi2500.xyz
./plot_log.py
./plot_xyz.py vi500.xyz
cp msd.pdf msd500.pdf
./plot_xyz.py vi1500.xyz
cp msd.pdf msd1500.pdf
./plot_xyz.py vi2500.xyz
cp msd.pdf msd2500.pdf

