#!/bin/bash

# List of tasks
TASK_LIST_FILE=boost_deplist_pack_task_all.txt

#
if [ "$1" = "-h" -o "$1" = "--help" ]
then
	echo
	echo "Usage: $0 [<File with the list of Koji tasks to be queried, one by line>]"
	echo "  - Default file for the list of Koji tasks: '${TASK_LIST_FILE}'"
	echo
	exit
fi
if [ -n "$1" ]
then
	TASK_LIST_FILE=$1
fi

#
WS_DIR=workspace
if [ ! -d ${WS_DIR} ]
then
	mkdir -p ${WS_DIR}
fi

# Logging
LOG_FILE=boost_deplist_pack_task_allinfo.txt
rm -f ${LOGFILE} boost_deplist_pack_task_all_success.txt \
 boost_deplist_pack_task_all_failure.txt boost_deplist_pack_task_all_unfinished.txt
touch boost_deplist_pack_task_all_success.txt \
 boost_deplist_pack_task_all_failure.txt boost_deplist_pack_task_all_unfinished.txt

#
BOOST_DEP_TASKLIST=`cat ${TASK_LIST_FILE}`
for _task in ${BOOST_DEP_TASKLIST}
do
	echo "Querying the Koji task #${_task}..."
	KOJI_STATUS=`koji taskinfo ${_task}`
	echo "${KOJI_STATUS}" >> ${LOG_FILE}
	echo >> ${LOG_FILE}
	unset KOJI_FAILED
	echo "${KOJI_STATUS}" | grep "State: failed" && KOJI_FAILED=${_task}
	KOJI_PACK=`echo "${KOJI_STATUS}" | grep "Build: " | cut -d':' -f2 | cut -d' ' -f2`
	if [ -n "${KOJI_FAILED}" ]
	then
		echo "The Koji task #${_task} (http://koji.fedoraproject.org/koji/taskinfo?taskID=${_task}) for ${KOJI_PACK} failed." | tee -a boost_deplist_pack_task_all_failure.txt
		echo >> boost_deplist_pack_task_all_failure.txt
	else
		unset KOJI_CLOSED
		echo "${KOJI_STATUS}" | grep "State: closed" && KOJI_CLOSED=${_task}
		if [ -n "${KOJI_CLOSED}" ]
		then
			echo "The Koji task #${_task} (http://koji.fedoraproject.org/koji/taskinfo?taskID=${_task}) for ${KOJI_PACK} succeeded." | tee -a boost_deplist_pack_task_all_success.txt
			echo >> boost_deplist_pack_task_all_success.txt
		else
			echo "The Koji task #${_task} (http://koji.fedoraproject.org/koji/taskinfo?taskID=${_task}) for ${KOJI_PACK} has not finished yet." | tee -a boost_deplist_pack_task_all_unfinished.txt
			echo >> boost_deplist_pack_task_all_unfinished.txt
		fi
	fi
done

# Reporting
echo
echo "Queried all the build tasks."
echo "See ${LOG_FILE} and boost_deplist_pack_task_all_xxx.txt (where xxx = {success, failure, unfinished})."
wc -l boost_deplist_pack_task_all_success.txt boost_deplist_pack_task_all_failure.txt boost_deplist_pack_task_all_unfinished.txt
echo

