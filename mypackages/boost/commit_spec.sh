#!/bin/bash

#
WS_DIR=workspace
if [ ! -d ${WS_DIR} ]
then
	mkdir -p ${WS_DIR}
fi

# Logging
LOG_FILE=boost_bump_versions.log
rm -f ${WS_DIR}/${LOG_FILE}

#
pushd ${WS_DIR}
BOOST_DEPLIST=`find . -type 'd' -maxdepth 1`
for _pack in ${BOOST_DEPLIST}
do
	if [ -d ${_pack} ]
	then
		pushd ${_pack}
		echo "Commit changes (bumped version) in the ${_pack} Fedora package..."
		fedpkg commit --clog -p | tee -a ../${LOG_FILE}
		echo "... done"
		popd
	else
		echo "[Warning] For whatever reason, the ${_pack} Fedora package is supposed to have been cloned, but has not"	
	fi
done
popd

# Reporting
echo
echo "The version of the RPM specification files has been dumped. See ${WS_DIR}/${LOG_FILE} for more details."
echo

