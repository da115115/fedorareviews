#!/bin/bash

#
WS_DIR=workspace
if [ ! -d ${WS_DIR} ]
then
	mkdir -p ${WS_DIR}
fi

#
LOG_FILE=rebuild_for_boost.log
rm -f ${WS_DIR}/${LOG_FILE}

#
BOOST_DEPLIST=`ls ${WS_DIR}`
pushd ${WS_DIR}
for _pack in ${BOOST_DEPLIST}
do
	if [ -d ${_pack} ]
	then
		pushd ${_pack}
		echo "Commit and build the ${_pack} Fedora package..."
		fedpkg commit --clog -p | tee ../${LOG_FILE}
		fedpkg build --nowait | tee ../${LOG_FILE}
		echo "... done"
		popd
	else
		echo "[Warning] For whatever reason, the ${_pack} Fedora package is supposed to have been cloned, but has not"	
	fi
done
popd

# Reporting
echo
echo "The rebuilding of all the dependent packages has been launched. See ${WS_DIR}/${LOG_FILE} for more details."
echo "grep http ${WS_DIR}/${LOG_FILE}"
echo

