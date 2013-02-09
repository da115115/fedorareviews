#!/bin/bash

#
WS_DIR=workspace
if [ ! -d ${WS_DIR} ]
then
	mkdir -p ${WS_DIR}
fi

#
BOOST_DEPLIST=`cat boost_deplist_pack_uniq.txt`
pushd ${WS_DIR}
for _pack in ${BOOST_DEPLIST}
do
	echo "Cloning the ${_pack} Fedora package..."
	time fedpkg clone ${_pack}
	echo "... done"
done
popd

# Reporting
echo
echo "All the dependent package Git repositories have been cloned into the ${WS_DIR} directory"
echo

