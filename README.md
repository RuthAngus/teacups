# teacups
Testing gyrochronology with Gaia comoving pairs


DATA
====
teacups/pairindices_cp1.fits is Semyeong's list of low probability pairs.

teacups/stacked_tgas.fits is TGAS where the indices correspond to above.

teacups/star1_kic_.csv = pair stars xmatched to Kepler

teacups/star2_kic_.csv = pair stars xmatched to Kepler

CODE
====
\rotation

measure_prots_of_comoving_pairs.py
A script specifically for downloading light curves and measuring rotation
periods of the comoving pair stars.
It saves .png and .csv results files to /pgram.

rotation.py
A module for measuring rotation periods.

kic_id_and_group_id.py: assigning group_ids
backwards.py: doing the same thing backwards to check.


TODO
====

* Organise and package code.
* Get a version of Jen's model working better.
* Get RVs.
