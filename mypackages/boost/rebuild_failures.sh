#!/bin/bash

#
WS_DIR=workspace
if [ ! -d ${WS_DIR} ]
then
	mkdir -p ${WS_DIR}
fi

# Logging
LOG_FILE=boost_rebuild_failures.log
rm -f ${WS_DIR}/${LOG_FILE}

#
BOOST_DEPLIST=`sed -e "s/^\(.\+\) for \(.\+\)-\([0-9]\+\).\([0-9a-z.]\+\)-\(.\+\)\.fc\([0-9]\+\)\(.*\) failed./\2/g" boost_deplist_pack_task_all_failure.txt | sed -e "/^$/d" | sort -u`
pushd ${WS_DIR}
for _pack in ${BOOST_DEPLIST}
do
	if [ -d ${_pack} ]
	then
		pushd ${_pack}
		echo "Build the ${_pack} Fedora package..."
		fedpkg build --nowait | tee -a ../${LOG_FILE}
		echo "... done"
		popd
	else
		echo "[Warning] For whatever reason, the ${_pack} Fedora package is supposed to have been cloned, but has not"	
	fi
done
popd

# Collect the task numbers:
grep "Created task" ${WS_DIR}/${LOG_FILE} | cut -d':' -f2 | cut -d' ' -f2 > boost_deplist_pack_task_rebuilt.txt

# Reporting
echo
echo "The rebuilding of all the dependent packages has been launched. See ${WS_DIR}/${LOG_FILE} for more details."
echo "The list of tasks is available in the boost_deplist_pack_task_rebuilt.txt file."
echo

