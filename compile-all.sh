#! /usr/bin/env bash

./check_prerequisites.py

# superMC
echo -e "\033[1;35m Compiling superMC ... \033[0m"
(
    cd superMC
    rm -fr data
    mkdir data
    mkdir build
    cd build
    cmake ..
    make
    make install
)
rm -fr centrality_cut_tables
cp -r superMC/scripts/centrality_cut_tables .


# VISHNew
echo -e "\033[1;35m Compiling VISHNew ... \033[0m"
(
    cd VISHNew
    mkdir build
    cd build
    cmake ..
    make
    make install
)


# iSS
echo -e "\033[1;35m Compiling iSS ... \033[0m"
(
    cd iSS
    mkdir build
    cd build
    cmake ..
    make
    make install
)

for ii in iS urqmd_afterburner
do
    echo -e "\033[1;35m Compiling " $ii " ... \033[0m"
    (cd $ii
     make distclean
     make
     make clean
    )
done

mv urqmd_afterburner/osc2u ./
mv urqmd_afterburner/urqmd ./

echo -e "\033[1;32m All programs have been compiled. Now let the fun begin! \033[0m"
