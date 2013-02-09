#!/bin/bash

echo
echo "Calculating the list of packages depending on Boost..."

# Extract all the dependent packages
BOOST_DEPLIST=`repoquery --whatrequires boost\* --source | uniq`

# Extract the names of the packages, removing the version and
# extra packaging information
rm -f boost_deplist_pack.txt
for _pack in $BOOST_DEPLIST
do
	echo ${_pack} | sed -e "s/^\(.\+\)-\([0-9]\+\).\([0-9a-z.]\+\)-\(.\+\)\.fc\([0-9]\+\)\(.*\)\.src\.rpm$/\1/g" >> boost_deplist_pack.txt
	done
uniq boost_deplist_pack.txt > boost_deplist_pack_uniq.txt
rm -f boost_deplist_pack.txt
NB_PACKS=`wc -l boost_deplist_pack_uniq.txt| cut -d' ' -f1`

# Reporting
echo "... done."
echo "To browse the list of (${NB_PACKS}) packages depending on Boost, just do:"
echo "less boost_deplist_pack_uniq.txt"
echo

