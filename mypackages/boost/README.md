
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

## Commit the RPM specification files ##
```shell
./commit_and_build_spec.sh
```

