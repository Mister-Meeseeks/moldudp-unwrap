#!/bin/bash -eu

scriptDir=$(dirname $0)

if [[ $# -eq 0 ]] ; then
    destBinDir=/usr/local/bin/
else
    destBinDir=$1
fi

sourceBin=$scriptDir/bin/moldudp
destBin=$destBinDir/moldudp

if [[ -e $destBin ]] ; then
    rm $destBin
elif [[ -L $destBin ]] ; then
    unlink $destBin
fi

ln -s $sourceBin $destBin

