#!/bin/bash

#
BOOST_VERSION="1.69.0"

#
WS_DIR="workspace"
if [ ! -d ${WS_DIR} ]
then
	mkdir -p ${WS_DIR}
fi

#
BOOST_DEPLIST=$(ls ${WS_DIR})
pushd ${WS_DIR}
for _pack in ${BOOST_DEPLIST}
do
	if [ -d ${_pack} ]
	then
		echo "Bumping the RPM specification file for the ${_pack} Fedora package..."
		rpmdev-bumpspec --comment="- Rebuild for Boost-${BOOST_VERSION}" ${_pack}/${_pack}.spec
		echo "... done"
	else
		echo "[Warning] For whatever reason, the ${_pack} Fedora package is supposed to have been cloned, but has not"
	fi
done
popd

# Reporting
echo
echo "The RPM specification files of all the dependent packages have been bumped."
echo


