#! /usr/bin/env bash

FC=`which h5fc`
if [ "$FC" == "" ]; then
   FC="../hdf5_support/hdf5/bin/h5fc";
fi
echo $FC
