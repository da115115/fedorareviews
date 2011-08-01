#!/bin/sh

GNASH_ORIG_DIR="gnash-0.8.8-pristine"
GNASH_RECONF_DIR="gnash-0.8.8-working-reconf"
GNASH_PATCH_STRUCTURE_FILE="gnash-088-fix-configure.patch.txt"
GNASH_PATCH_FILE="gnash-088-fix-configure.patch"

echo ""
echo "Calculating structure of the configuration patch"
diff -rc --brief --exclude=.deps --exclude=Makefile --exclude=config.* \
	--exclude=autom4te.cache --exclude=Doxyfile --exclude=*rc \
	--exclude=*.orig --exclude=libtool --exclude=stamp-h1 \
	--exclude=gnash* --exclude=*.plist \
	${GNASH_ORIG_DIR} ${GNASH_RECONF_DIR} > ${GNASH_PATCH_STRUCTURE_FILE}
echo "Done"

echo ""
echo "Calculating the configuration patch"
diff -Nur --exclude=.deps --exclude=Makefile --exclude=config.* \
	--exclude=autom4te.cache --exclude=Doxyfile --exclude=*rc \
	--exclude=*.orig --exclude=libtool --exclude=stamp-h1 \
	--exclude=gnash* --exclude=*.plist \
	${GNASH_ORIG_DIR} ${GNASH_RECONF_DIR} > ${GNASH_PATCH_FILE}
echo "Done"
echo ""


