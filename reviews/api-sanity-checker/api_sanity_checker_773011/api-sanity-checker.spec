Name:           api-sanity-checker
Version:        1.12.9
Release:        1%{?dist}
Summary:        An automatic generator of basic unit tests for a shared C/C++ library.

License:        GPL+ or LGPLv2+
URL:            http://forge.ispras.ru/projects/api-sanity-autotest
Source0:        http://forge.ispras.ru/attachments/download/1278/%{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       binutils

%{?perl_default_filter}

%description
API Sanity Checker (ASC) is an automatic generator of basic unit tests for
shared C/C++ libraries. It is able to generate reasonable (in most, but
unfortunately not all, cases) input data for parameters and compose simple
("sanity" or "shallow"-quality) test cases for every function in the API through
the analysis of declarations in header files. The quality of generated tests
allows to check absence of critical errors in simple use cases. The tool is able
to build and execute generated tests and detect crashes (segfaults), aborts, all
kinds of emitted signals, non-zero program return code and program hanging. It
may be considered as a tool for out-of-the-box low-cost sanity checking
(fuzzing) of the library API or as a test development framework for initial
generation of templates for advanced tests. Also it supports universal format of
tests, random test generation mode, specialized data types and other useful
features.


%prep
%setup -q
chmod -x LICENSE.txt


%build
# Nothing to build.


%install
mkdir -p %{buildroot}%{_bindir}
perl ./Makefile.pl -install --destdir=%{buildroot} --prefix=%{_prefix}


%files
%doc LICENSE.txt doc/*
%{_bindir}/%{name}


%changelog
* Tue Jan 10 2012 Richard Shaw <hobbes1069@gmail.com> - 1.12.9-1
- Initial release.
