#! /usr/bin/env bash

for ii in VISHNew iSS iS osc2u urqmd
    do
    echo "Compiling " $ii " ..."
    (cd $ii 
     make distclean
     make
     make clean
    )
done

echo -e "\033[1;32m All programs have been compiled. Now let the fun begin!"
