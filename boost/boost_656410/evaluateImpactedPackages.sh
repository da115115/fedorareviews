#!/bin/sh

RAW_BOOST_PACKAGES_FILE=boost_raw_packs.txt
RAW_BOOST_PACKAGES=`repoquery --qf '%{name}' --whatrequires libboost\* --whatrequires boost\*`

# 1. Get the list of packages dependent on Boost
echo "${RAW_BOOST_PACKAGES}" > ${RAW_BOOST_PACKAGES_FILE}

# 2. Eliminate duplicates and lemmatize package names (foo-devel->foo)
cat ${RAW_BOOST_PACKAGES_FILE} \
 | while read a; do if repoquery -R $a\* | grep boost \
 | fgrep -q 'so.1.41.0'; then :; else echo $a; fi; done

# 3. Remove packages that were already built against the new boost:
cat ${RAW_BOOST_PACKAGES_FILE} \
 | while read a; do if repoquery -R $a\* | grep boost \
 | fgrep -q 'so.1.41.0'; then :; else echo $a; fi; done

# 4. Of that, packages that depend on older libboost and need a rebuild:
cat no_41 | while read a; do if repoquery -R $a\* \
 | fgrep -q libboost; then echo $a; fi; done
 
