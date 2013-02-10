
## Clone the support tools themselves ##
```shell
git clone http://github.com/denisarnaud/fedorareviews.git fedorareviewsgit
cd fedorareviewsgit/mypackages/boost
```

## Calculate the packages depending on Boost ##
```shell
./calculate_boost_dep_list.sh
```

## Clone the Fedora Git repositories ##
```shell
./clone_dep.sh
```

## Bump the RPM specification files ##
```shell
./bump_spec.sh
```

## Re-tag Boost for Rawhide ##
```shell
koji tag-pkg f19 boost-1.53.0-1.fc19
```

## Wait that the new Boost land into Rawhide ##
When the following command returns, Boost is in the Rawhide repository:
```shell
koji wait-repo --build=boost-1.53.0-1.fc19 f19-build
```
The Fedora Rawhide repository is rebuilt and can be tracked with a task
such as http://koji.fedoraproject.org/koji/taskinfo?taskID=4943763


## Commit the RPM specification files ##
```shell
./commit_and_build_spec.sh
```

## Query the status of the builds ##
Wait a few hours and check the status of the Koji building tasks:
```shell
./query_status.sh
```

