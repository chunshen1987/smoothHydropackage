SmoothHydropackage
==================

This package perform single shot hydro or hybrid simulations for relativistic heavy-ion
collisions.

Setup
======

You can download all the code packages using `get_code_packages.sh`. Then you can run
`compile-all.sh` to compile all the code packages.


Running Simulations
===================

To run the simulation package, you need to start with `runHydro.py` script. You can view the help
message by typing `./runHydro.py -help`.

In the case you want to run simulations at a new collision energy or for a new collision system,
you need to generate the centrality cut tables before running `runHydro.py`. In order to do this,
you need to use the help scripts in the `superMC/scripts/`. The script
`generate_minbiasEcc_jobs_WSUGrid.py` can help to setup simulations to generate the minimum bias
database on a cluster. Once the simulations finish, you can use the script
`collect_minbiasEcc_results.sh` to collect all the data to a hdf5 database. After the database is
generated, you can run `centrality_cut_h5.py` to generate the centrality cut table for the new
collision system.
