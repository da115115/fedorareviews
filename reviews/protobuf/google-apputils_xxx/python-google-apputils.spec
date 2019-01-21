%global srcname google-apputils
%global _docdir_fmt %{name}

Name:           python-%{srcname}
Version:        0.4.2
Release:        14%{?dist}
Summary:        Google Application Utilities for Python

License:        ASL 2.0
URL:            https://github.com/google/%{srcname}
Source0:        https://pypi.python.org/packages/source/g/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-dateutil
BuildRequires:  python2-gflags
BuildRequires:  python2-pytz
BuildRequires:  /usr/bin/2to3
# For tests
BuildRequires:  python2-mox

%global _description\
This project is a small collection of utilities for building Python\
applications. It includes some of the same set of utilities used to build and\
run internal Python apps at Google.\
\
Features:\
\
* Simple application startup integrated with python-gflags.\
* Subcommands for command-line applications.\
* Option to drop into pdb on uncaught exceptions.\
* Helper functions for dealing with files.\
* High-level profiling tools.\
* Timezone-aware wrappers for datetime.datetime classes.\
* Improved TestCase with the same methods as unittest2, plus helpful flags for\
  test startup.\
* google_test setuptools command for running tests.\
* Helper module for creating application stubs.

%description %_description

%package -n python2-%{srcname}
Summary: %summary
Requires:       python2-dateutil
Requires:       python2-gflags
Requires:       python2-pytz
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname} %_description

%package -n python3-%{srcname}
Summary:        Google Application Utilities for Python 3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python2-tools
BuildRequires:  python3-dateutil
BuildRequires:  python3-gflags
BuildRequires:  python3-pytz
# For tests
# python-mox doesn't work with python3
# https://bugzilla.redhat.com/show_bug.cgi?id=1209203
#BuildRequires:  python3-mox
Requires:       python3-dateutil
Requires:       python3-gflags
Requires:       python3-pytz

%description -n python3-%{srcname}
This project is a small collection of utilities for building Python 3
applications. It includes some of the same set of utilities used to build and
run internal Python apps at Google.

Features:

* Simple application startup integrated with python-gflags.
* Subcommands for command-line applications.
* Option to drop into pdb on uncaught exceptions.
* Helper functions for dealing with files.
* High-level profiling tools.
* Timezone-aware wrappers for datetime.datetime classes.
* Improved TestCase with the same methods as unittest2, plus helpful flags for
  test startup.
* google_test setuptools command for running tests.
* Helper module for creating application stubs.


%prep
%setup -qc
mv %{srcname}-%{version} python2
# Strip shbang
find -name \*.py | xargs sed -i '/^#!\/usr\/bin\/.*python/d'
# setup cannot handle pytz versioning
sed -i -e 's/pytz>.*"/pytz"/' python2/setup.py
cp -a python2 python3
2to3 --write --nobackups python3


%build
pushd python2
%{__python2} setup.py build
popd
pushd python3
%{__python3} setup.py build
popd


%install
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
popd

pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
popd


%check
pushd python2
%{__python2} setup.py test
popd
# python-mox doesn't work with python3 
#pushd python3
#%{__python3} setup.py test
#popd

 
%files -n python2-%{srcname}
%license python2/LICENSE
%doc python2/README
%{python2_sitelib}/*

%files -n python3-%{srcname}
%license python3/LICENSE
%doc python3/README
%{python3_sitelib}/*


%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.2-13
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.4.2-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.4.2-10
- Python 2 binary package renamed to python2-google-apputils
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.2-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 21 2015 Orion Poplawski <orion@cora.nwra.com> - 0.4.2-2
- Use _docdir_fmt macro
- Fix changelog
- Strip shbang from python library files

* Mon Apr  6 2015 Orion Poplawski <orion@cora.nwra.com> - 0.4.2-1
- Initial package
