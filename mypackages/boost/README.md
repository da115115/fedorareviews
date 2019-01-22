
## References
* [This README on GitHub Fedora Packaging project](https://github.com/fedorapackaging/fedorareviews/tree/trunk/mypackages/boost)
* [Boost section on Denis Arnaud's Fedora page](https://fedoraproject.org/wiki/User:Denisarnaud#Boost)
* [Koji tags and package organization](https://fedoraproject.org/wiki/Using_the_Koji_build_system#Koji_tags_and_packages_organization)
* [Boost-1.69 on Fedora 30](https://fedoraproject.org/wiki/Changes/F30Boost169#Scope)

## Clone the support tools themselves
```bash
$ git clone http://github.com/denisarnaud/fedorareviews.git fedorareviewsgit
$ cd fedorareviewsgit/mypackages/boost
```

## Calculate the packages depending on Boost
```bash
$ ./calculate_boost_dep_list.sh
```

## Clone the Fedora Git repositories
```bash
$ ./clone_dep.sh
```

## Details about the build tag
```bash
$ koji list-targets --name f30-boost
Name                           Buildroot                      Destination                   
---------------------------------------------------------------------------------------------
f30-boost                      f30-boost                      f30-boost                     
```

## Clone and build Boost itself with the build tag
```bash
$ cd workspace && fedpkg clone boost && cd boost
$ fedpkg build --nowait --target 'f30-boost' --srpm
$ cd ../..
```

## Bump the RPM specification files
```bash
$ ./bump_spec.sh
```

## Re-tag Boost for Rawhide
```bash
$ koji tag-pkg f30 boost-1.69.0-1.f30
```

## Wait that the new Boost land into Rawhide
When the following command returns, Boost is in the Rawhide repository:
```bash
$ koji wait-repo --build=boost-1.69.0-1.f30 f30-build
```
The Fedora Rawhide repository is rebuilt and can be tracked with a task
such as http://koji.fedoraproject.org/koji/taskinfo?taskID=4943763


## Commit the RPM specification files
```bash
$ ./commit_spec.sh
```

## Rebuild the packages
```bash
$ ./rebuild_spec.sh
```

## Query the status of the builds
Wait a few hours and check the status of the Koji building tasks:
```bash
$ ./query_status.sh
```

## Rebuild the failed builds
The above Shell script creates the `boost_deplist_pack_task_all_failure.txt`
file, giving the details (package name, task ID) on the Koji tasks
of all the builds having failed. The following Shell script launches
a rebuild for each of those packages:
```bash
$ ./rebuild_failures.sh
```

## Query the status of the rebuilds ##
Wait a few hours and check the status of the Koji building tasks:
```bash
$ ./query_status.sh boost_deplist_pack_task_rebuilt.txt
```


