#!/bin/sh

###
# See the end of that file for some comments and documentation
###

#
PACKAGE_NAME="wsdlpull"
PACKAGE_VERSION="1.23"
PRISTINE_NAME="${PACKAGE_NAME}-${PACKAGE_VERSION}"
PRISTINE_DIR="${PRISTINE_NAME}"
PRISTINE_TARBALL="${PRISTINE_DIR}.tar.gz"
PRISTINE_DOWNLOAD_URL="http://downloads.sourceforge.net/${PACKAGE_NAME}"
TARGET_SUFFIX="4-pack"
TARGET_NAME="${PRISTINE_DIR}_${TARGET_SUFFIX}"
TARGET_DIR="${TARGET_NAME}"
UNZIP="gunzip"
PATCH_ZIP_SUFFIX=".gz"
PATCH_SUFFIX=".patch"
PATCH_GCC43="${PRISTINE_NAME}_gcc43${PATCH_SUFFIX}"
PATCH_GCC43_ZIP="${PATCH_GCC43}${PATCH_ZIP_SUFFIX}"
PATCH_MAN="${PRISTINE_NAME}_man_pages${PATCH_SUFFIX}"
PATCH_MAN_ZIP="${PATCH_MAN}${PATCH_ZIP_SUFFIX}"
PATCH_MAKES="${PRISTINE_NAME}_makefiles${PATCH_SUFFIX}"
PATCH_MAKES_ZIP="${PATCH_MAKES}${PATCH_ZIP_SUFFIX}"

# Functions to generate patch and diff
FROM_DIR=${PRISTINE_DIR}
TO_DIR=${TARGET_DIR}
function generateStructureDiff() {
	echo "Generate diff file for the structure, between ${FROM_DIR} and ${TO_DIR}"
	diff -r --brief ${FROM_DIR} ${TO_DIR} > ${DIFF_FILE}
}

function generateFullPatch() {
	echo "Generate patch from ${FROM_DIR} to ${TO_DIR}"
	diff -Nur ${FROM_DIR} ${TO_DIR} > ${PATCH_FILE}
}

function applyPatchP1() {
# Sanity check
	if [ ! -f "${PATCH_GCC43_ZIP}" ]; then
		echo "The g++4.3-compilation patch (${PATCH_GCC43_ZIP}) should be present, but is not."
		exit -1
	fi

# Apply the patch
	echo "Apply the g++4.3-compilation patch (${PATCH_GCC43})"
	${UNZIP} ${PATCH_GCC43_ZIP}
	patch -p1 < ${PATCH_GCC43} && echo "Patch applied"

# Remove the patch
	rm -f ${PATCH_GCC43}
}

function applyPatchP2() {
# Sanity check
	if [ ! -f "${PATCH_MAN_ZIP}" ]; then
		echo "The build patch (${PATCH_MAN_ZIP}) should be present, but is not."
		exit -1
	fi

# Apply the patch
	echo "Apply the build patch (${PATCH_MAN})"
	${UNZIP} ${PATCH_MAN_ZIP}
	patch -p1 < ${PATCH_MAN} && echo "Patch applied"

# Remove the patch
	rm -f ${PATCH_MAN}
}

function applyPatchP3() {
# Sanity check
	if [ ! -f "${PATCH_MAKES_ZIP}" ]; then
		echo "The build patch (${PATCH_MAKES_ZIP}) should be present, but is not."
		exit -1
	fi

# Apply the patch
	echo "Apply the build patch (${PATCH_MAKES})"
	${UNZIP} ${PATCH_MAKES_ZIP}
	patch -p1 < ${PATCH_MAKES} && echo "Patch applied"

# Remove the patch
	rm -f ${PATCH_MAKES}
}


##
## Main
##

# Retrieve the pristine tar-ball
if [ ! -f ${PRISTINE_TARBALL} ]; then
	echo "Download pristine ${PACKAGE_NAME} tar-ball (${PRISTINE_TARBALL})"
	wget ${PRISTINE_DOWNLOAD_URL}/${PRISTINE_TARBALL}
fi

# (Remove former package and) un-pack the pristine tar-ball
# rm -rf ${PRISTINE_DIR}
if [ ! -d ${PRISTINE_DIR} ]; then
	echo "Creating ${PRISTINE_DIR} for extracting pristine tar-ball"
	mkdir -p ${PRISTINE_DIR}
fi
echo "Extracting pristine ${PACKAGE_NAME} tar-ball (${PRISTINE_TARBALL})"
tar zxf ${PRISTINE_TARBALL}

# Copy the pristine package into the target one
rm -rf ${TARGET_DIR}
echo "Create a copy of extracted sources (${PRISTINE_DIR}) into ${TARGET_DIR}"
cp -r ${PRISTINE_DIR} ${TARGET_DIR}

# Apply a patch for compatibility of compilation with version 4.3 onwards of g++
cp ${PATCH_GCC43_ZIP} ${TARGET_DIR}
cd ${TARGET_DIR}
applyPatchP1
cd ..

# Add man pages
# Apply a patch for compatibility of compilation with version 4.3 onwards of g++
cp ${PATCH_MAN_ZIP} ${TARGET_DIR}
cd ${TARGET_DIR}
mkdir man
applyPatchP2
cd ..

# Adapt the directory structure within the target
echo "Alter the structure of ${TARGET_DIR}"
cd ${TARGET_DIR}

# Remove any CVS sub-directory (they should not be delivered with the tar-ball)
find . -name 'CVS' -print | xargs -r rm -rf

# Remove any a.out binary (they should not be delivered with the tar-ball)
find . -name 'a.out' -print | xargs -r rm -f

# Remove the generated HTML documentation (it should not be delivered
# with the tar-ball, as it is generated)
if [ -d docs/html ]; then
	rm -rf docs/html
fi

# Rename the standard documentation files
mv AUTHORS.txt AUTHORS
sed -i -e 's/\r$//' AUTHORS
mv CHANGES.txt CHANGES
mv COPYING.txt COPYING
mv README.txt README

# Dedicated config sub-directory
mkdir config
mv config.guess config.sub depcomp install-sh ltmain.sh missing config
mv config.h.in src

#mv ChangeLog.txt ChangeLog
#mv COPYING.txt COPYING

# Rename the source code directory, so that the files (e.g, header
# files) can be exported correctly into {_standard_dir}/%{name}
#mv src ${PACKAGE_NAME}
cd ..

# Apply patch for full build
#cp ${PATCH_MAKES_ZIP} ${TARGET_DIR}
cd ${TARGET_DIR}
#applyPatchP3
cd ..

# Generate patch
PATCH_FILE="${TARGET_NAME}.patch"
#generateFullPatch
DIFF_FILE="${TARGET_NAME}.diff"
#generateStructureDiff


###
## Build (for Soci)
##
# cd ${TARGET_DIR}
# ./configure --enable-backend-mysql --enable-backend-postgresql --enable-backend-sqlite3 --enable-backend-oracle --with-oracle-include=/opt/oracle/app/oracle/product/11.1.0/db_1/rdbms/public --with-oracle-lib=/opt/oracle/app/oracle/product/11.1.0/db_1/lib
# cd ..


###
## Directory structure
##
# 1. wsdlpull-1.23        -- Upstream content, extracted from pristine tar-ball
# 2. wsdlpull-1.23_4-pack -- Working directory, initially copied from pristine 
#                            upstream. The patches are then applied into that
#                            temporary directory.
# 3. wsdlpull-1.23_extras123 -- Copy from the extras-wsdlpull sources, 
#                               extracted from the extras-wsdlpull generated 
#                               tar-ball.
# The final patch results from the comparison of both wsdlpull-1.23_4-pack and
# wsdlpull-1.23_extras123 directories.


###
## Patch 1 -- Temp for building g++-4.3 patch (to perform only very rarely)
##
# As build (or as darnaud)
# cdwsdlfedtmp (cd /home/build/dev/fedora/reviewsvn/wsdlpull_502686/extras-wsdlpull) (or cd /home/dan/dev/meijesvn/trunk/extras-wsdlpull)
# Add an "exit 0" line, just after applying the patch #1 (applyPatchP1 function)
# ./wsdlpull_adapt_structure_123.sh
# Alter the source code in wsdlpull-1.23_4-pack/src
# rm -f wsdlpull-1.23_gcc43.patch && diff -Nur wsdlpull-1.23 wsdlpull-1.23_4-pack > wsdlpull-1.23_gcc43.patch && gzip wsdlpull-1.23_gcc43.patch
# Remove the "exit 0"

# As build
# gunzip wsdlpull-1.23_gcc43.patch.gz && cp /home/build/dev/fedora/reviewsvn/wsdlpull_502686/extras-wsdlpull/wsdlpull-1.23_gcc43.patch /home/build/dev/packages/SOURCES/wsdlpull-1.23-fix-gcc43-compatibility.patch && gzip wsdlpull-1.23_gcc43.patch
# (or cd /home/build/dev/packages/SOURCES && cp /home/dan/dev/meijesvn/trunk/extras-wsdlpull/wsdlpull-1.23_gcc43.patch wsdlpull-1.23-fix-gcc43-compatibility.patch)



###
## Patch 2 -- Temp for building man pages patch (to perform only very rarely)
##
# As build (or as darnaud)
# cdwsdlfedtmp (cd /home/build/dev/fedora/reviewsvn/wsdlpull_502686/extras-wsdlpull) (or cd /home/dan/dev/meijesvn/trunk/extras-wsdlpull)
# Comment the applyPatchP1 line, and add an "exit 0" line, just after applying the patch #2 (applyPatchP2 function)
# ./wsdlpull_adapt_structure_123.sh
# Alter the man pages in wsdlpull-1.23_4-pack/man (if empty, just copy the files
# from wsdlpull-1.23_extras123/man/*)
# rm -f wsdlpull-1.23_man_pages.patch && diff -Nur wsdlpull-1.23 wsdlpull-1.23_4-pack > wsdlpull-1.23_man_pages.patch && gzip wsdlpull-1.23_man_pages.patch
# Remove the "exit 0" and uncomment the applyPatchP1

# As build
# gunzip wsdlpull-1.23_man_pages.patch.gz && cp /home/build/dev/fedora/reviewsvn/wsdlpull_502686/extras-wsdlpull/wsdlpull-1.23_man_pages.patch /home/build/dev/packages/SOURCES/wsdlpull-1.23-add-man-pages.patch && gzip wsdlpull-1.23_man_pages.patch
# (or cd /home/build/dev/packages/SOURCES && cp /home/dan/dev/meijesvn/trunk/extras-wsdlpull/wsdlpull-1.23_man_pages.patch wsdlpull-1.23-add-man-pages.patch)



###
## Patch 3 -- Temp for building GNU Autotools and burried headers patch
##
# As build
# ./configure && make dist && cp wsdlpull.spec ../../../packages/SPECS

# As build (or as darnaud)
# cdwsdlfedtmp (cd /home/build/dev/fedora/reviewsvn/wsdlpull_502686/extras-wsdlpull) (or cd /home/dan/dev/meijesvn/trunk/extras-wsdlpull)
# mv wsdlpull-1.23 wsdlpull-1.23.orig && tar zxf /home/build/dev/fedora/wsdlpull/wsdlpull123svn/wsdlpull-1.23.tar.gz && rm -rf wsdlpull-1.23_extras123 && mv wsdlpull-1.23 wsdlpull-1.23_extras123 && mv wsdlpull-1.23.orig wsdlpull-1.23
# ./wsdlpull_adapt_structure_123.sh
# diff -r --brief wsdlpull-1.23_4-pack wsdlpull-1.23_extras123 > wsdlpull-1.23_remaining.diff
# less wsdlpull-1.23_remaining.diff
# rm -f wsdlpull-1.23_to_extras123.patch && diff -Nur wsdlpull-1.23_4-pack wsdlpull-1.23_extras123 > wsdlpull-1.23_to_extras123.patch 
# gzip wsdlpull-1.23_to_extras123.patch

# As build
# gunzip wsdlpull-1.23_to_extras123.patch.gz && cp /home/build/dev/fedora/reviewsvn/wsdlpull_502686/extras-wsdlpull/wsdlpull-1.23_to_extras123.patch /home/build/dev/packages/SOURCES/wsdlpull-1.23-fix-gnu-autotools-compatibility.patch && gzip wsdlpull-1.23_to_extras123.patch
# (or cd /home/build/dev/packages/SOURCES && cp /home/dan/dev/meijesvn/trunk/extras-wsdlpull/wsdlpull-1.23_to_extras123.patch wsdlpull-1.23-fix-gnu-autotools-compatibility.patch)

