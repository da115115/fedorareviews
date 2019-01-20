# Support for documentation installation As the %%doc macro erases the
# target directory ($RPM_BUILD_ROOT%%{_docdir}/%%{name}), manually
# installed documentation must be saved into a temporary dedicated
# directory.
# XXX note that as of rpm 4.9.1, this shouldn't be necessary anymore.
# We should be able to install directly.
%global boost_docdir __tmp_docdir
%global boost_examplesdir __tmp_examplesdir

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
 
%if 0%{?rhel} >= 7
%ifarch ppc64le
  %bcond_with mpich
%else
  %bcond_without mpich
%endif
%endif
%if 0%{?rhel} == 6
%ifarch %{arm} ppc64
  %bcond_with mpich
%else
  %bcond_without mpich
%endif
%endif
%if 0%{?rhel} >= 5
  %bcond_without mpich2
%endif

%if 0%{?rhel} >= 7
%ifarch s390 s390x ppc64le
  # No OpenMPI support on these arches
  %bcond_with openmpi
%else
  %bcond_without openmpi
%endif
%endif

%ifnarch %{ix86} x86_64 %{arm} ppc64 ppc64le
  %bcond_with context
%else
  %bcond_without context
%endif

%bcond_without python2
%bcond_without python3

%ifnarch %{ix86} x86_64
  %bcond_with quadmath
%else
  %bcond_without quadmath
%endif

Name: boost169
%global real_name boost
Summary: The free peer-reviewed portable C++ source libraries
Version: 1.69.0
%global version_enc 1_69_0
%global version_suffix 169
Release: 1%{?dist}
License: Boost and MIT and Python

%global toplev_dirname %{real_name}_%{version_enc}
URL: http://www.boost.org
Group: System Environment/Libraries

Source0: https://sourceforge.net/projects/boost/files/%{real_name}/%{version}/%{toplev_dirname}.tar.bz2
Source1: libboost_thread.so
Source2: ver.py

# Since Fedora 13, the Boost libraries are delivered with sonames
# equal to the Boost version (e.g., 1.41.0).
%global sonamever %{version}

# boost is an "umbrella" package that pulls in all boost shared library
# components, except for MPI and Python sub-packages.  Those are special
# in that there are alternative implementations to choose from
# (Open MPI and MPICH, and Python 2 and 3), and it's not a big burden
# to have interested parties install them explicitly.
# The subpackages that don't install shared libraries are also not pulled in
# (doc, doctools, examples, jam, static).
Requires: %{name}-atomic%{?_isa} = %{version}-%{release}
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-container%{?_isa} = %{version}-%{release}
Requires: %{name}-contract%{?_isa} = %{version}-%{release}
%if %{with context}
Requires: %{name}-context%{?_isa} = %{version}-%{release}
Requires: %{name}-coroutine%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-date-time%{?_isa} = %{version}-%{release}
%if %{with context}
Requires: %{name}-fiber%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-filesystem%{?_isa} = %{version}-%{release}
Requires: %{name}-graph%{?_isa} = %{version}-%{release}
Requires: %{name}-iostreams%{?_isa} = %{version}-%{release}
Requires: %{name}-locale%{?_isa} = %{version}-%{release}
Requires: %{name}-log%{?_isa} = %{version}-%{release}
Requires: %{name}-math%{?_isa} = %{version}-%{release}
Requires: %{name}-program-options%{?_isa} = %{version}-%{release}
Requires: %{name}-random%{?_isa} = %{version}-%{release}
Requires: %{name}-regex%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}
Requires: %{name}-stacktrace%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Requires: %{name}-test%{?_isa} = %{version}-%{release}
Requires: %{name}-thread%{?_isa} = %{version}-%{release}
Requires: %{name}-timer%{?_isa} = %{version}-%{release}
Requires: %{name}-type_erasure%{?_isa} = %{version}-%{release}
Requires: %{name}-wave%{?_isa} = %{version}-%{release}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc-c++
BuildRequires: m4
BuildRequires: libstdc++-devel
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
%if %{with python2}
BuildRequires: python-devel
BuildRequires: python2-numpy
%endif
%if %{with python3}
BuildRequires: python34-devel
BuildRequires: python34-numpy
%endif
BuildRequires: libicu-devel
%if %{with quadmath}
BuildRequires: libquadmath-devel
%endif

# https://svn.boost.org/trac/boost/ticket/6150
Patch4: boost-1.50.0-fix-non-utf8-files.patch

# Add a manual page for bjam, based on the on-line documentation:
# http://www.boost.org/boost-build2/doc/html/bbv2/overview.html
Patch5: boost-1.48.0-add-bjam-man-page.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=828856
# https://bugzilla.redhat.com/show_bug.cgi?id=828857
# https://svn.boost.org/trac/boost/ticket/6701
Patch15: boost-1.58.0-pool.patch

# https://svn.boost.org/trac/boost/ticket/5637
Patch25: boost-1.57.0-mpl-print.patch

# https://svn.boost.org/trac/boost/ticket/9038
Patch51: boost-1.58.0-pool-test_linking.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1102667
Patch61: boost-1.57.0-python-libpython_dep.patch
Patch62: boost-1.66.0-python-abi_letters.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1190039
Patch65: boost-1.66.0-build-optflags.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1318383
Patch82: boost-1.66.0-no-rpath.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1541035
Patch83: boost-1.66.0-bjam-build-flags.patch

%bcond_with tests
%bcond_with docs_generated

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been included in the C++ 2011 standard and
others have been proposed to the C++ Standards Committee for inclusion
in future standards.)

%package atomic
Summary: Run-time component of boost atomic library
Group: System Environment/Libraries

%description atomic

Run-time support for Boost.Atomic, a library that provides atomic data
types and operations on these data types, as well as memory ordering
constraints required for coordinating multiple threads through atomic
variables.

%package chrono
Summary: Run-time component of boost chrono library
Group: System Environment/Libraries
Requires: %{name}-system%{?_isa} = %{version}-%{release}

%description chrono

Run-time support for Boost.Chrono, a set of useful time utilities.

%package container
Summary: Run-time component of boost container library
Group: System Environment/Libraries

%description container

Boost.Container library implements several well-known containers,
including STL containers. The aim of the library is to offer advanced
features not present in standard containers or to offer the latest
standard draft features for compilers that comply with C++03.

%package contract
Summary: Run-time component of boost contract library
Group: System Environment/Libraries

%description contract

Run-time support for boost contract library.
Contract programming for C++. All contract programming features are supported:
Subcontracting, class invariants, postconditions (with old and return values),
preconditions, customizable actions on assertion failure (e.g., terminate
or throw), optional compilation and checking of assertions, etc,
from Lorenzo Caminiti.

%if %{with context}
%package context
Summary: Run-time component of boost context switching library
Group: System Environment/Libraries

%description context

Run-time support for Boost.Context, a foundational library that
provides a sort of cooperative multitasking on a single thread.

%package coroutine
Summary: Run-time component of boost coroutine library
Group: System Environment/Libraries

%description coroutine
Run-time support for Boost.Coroutine, a library that provides
generalized subroutines which allow multiple entry points for
suspending and resuming execution.

%endif

%package date-time
Summary: Run-time component of boost date-time library
Group: System Environment/Libraries

%description date-time

Run-time support for Boost Date Time, a set of date-time libraries based
on generic programming concepts.

%if %{with context}
%package fiber
Summary: Run-time component of boost fiber library
Group: System Environment/Libraries

%description fiber

Run-time support for the Boost Fiber library, a framework for
micro-/userland-threads (fibers) scheduled cooperatively.
%endif

%package filesystem
Summary: Run-time component of boost filesystem library
Group: System Environment/Libraries
Requires: %{name}-system%{?_isa} = %{version}-%{release}

%description filesystem

Run-time support for the Boost Filesystem Library, which provides
portable facilities to query and manipulate paths, files, and
directories.

%package graph
Summary: Run-time component of boost graph library
Group: System Environment/Libraries
Requires: %{name}-regex%{?_isa} = %{version}-%{release}

%description graph

Run-time support for the BGL graph library.  BGL interface and graph
components are generic, in the same sense as the Standard Template
Library (STL).

%package iostreams
Summary: Run-time component of boost iostreams library
Group: System Environment/Libraries

%description iostreams

Run-time support for Boost.Iostreams, a framework for defining streams,
stream buffers and i/o filters.

%package locale
Summary: Run-time component of boost locale library
Group: System Environment/Libraries
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Requires: %{name}-thread%{?_isa} = %{version}-%{release}

%description locale

Run-time support for Boost.Locale, a set of localization and Unicode
handling tools.

%package log
Summary: Run-time component of boost logging library
Group: System Environment/Libraries

%description log

Boost.Log library aims to make logging significantly easier for the
application developer.  It provides a wide range of out-of-the-box
tools along with public interfaces for extending the library.

%package math
Summary: Math functions for boost TR1 library
Group: System Environment/Libraries

%description math

Run-time support for C99 and C++ TR1 C-style Functions from the math
portion of Boost.TR1.

%if %{with python2}

%package numpy2
Summary: Run-time component of boost numpy library for Python 2
Group: System Environment/Libraries
Requires: %{name}-python2%{?_isa} = %{version}-%{release}
Requires: python2-numpy

%description numpy2

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes,
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for the NumPy extension of the Boost Python Library for Python 2.

%endif

%if %{with python3}

%package numpy3
Summary: Run-time component of boost numpy library for Python 3
Requires: %{name}-python3%{?_isa} = %{version}-%{release}
Requires: python34-numpy

%description numpy3

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes,
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for the NumPy extension of the Boost Python Library for Python 3.

%endif

%package program-options
Summary:  Run-time component of boost program_options library
Group: System Environment/Libraries

%description program-options

Run-time support of boost program options library, which allows program
developers to obtain (name, value) pairs from the user, via
conventional methods such as command-line and configuration file.

%if %{with python2}

%package python2
Summary: Run-time component of boost python library for Python 2
Group: System Environment/Libraries

%description python2

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes,
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for the Boost Python Library compiled for Python 2.

%package python2-devel
Summary: Shared object symbolic links for Boost.Python 2
Requires: %{name}-numpy2%{?_isa} = %{version}-%{release}
Requires: %{name}-python2%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description python2-devel

Shared object symbolic links for Python 2 variant of Boost.Python.

%endif

%if %{with python3}

%package python3
Summary: Run-time component of boost python library for Python 3
Group: System Environment/Libraries

%description python3

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes,
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for the Boost Python Library compiled for Python 3.

%package python3-devel
Summary: Shared object symbolic links for Boost.Python 3
Group: System Environment/Libraries
Requires: %{name}-numpy3%{?_isa} = %{version}-%{release}
Requires: %{name}-python3%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description python3-devel

Shared object symbolic links for Python 3 variant of Boost.Python.

%endif

%package random
Summary: Run-time component of boost random library
Group: System Environment/Libraries

%description random

Run-time support for boost random library.

%package regex
Summary: Run-time component of boost regular expression library
Group: System Environment/Libraries

%description regex

Run-time support for boost regular expression library.

%package serialization
Summary: Run-time component of boost serialization library
Group: System Environment/Libraries

%description serialization

Run-time support for serialization for persistence and marshaling.

%package stacktrace
Summary: Run-time component of boost stacktrace library

%description stacktrace

Run-time component of the Boost stacktrace library.

%package system
Summary: Run-time component of boost system support library
Group: System Environment/Libraries

%description system

Run-time component of Boost operating system support library, including
the diagnostics support that is part of the C++11 standard library.

%package test
Summary: Run-time component of boost test library
Group: System Environment/Libraries

%description test

Run-time support for simple program testing, full unit testing, and for
program execution monitoring.

%package thread
Summary: Run-time component of boost thread library
Group: System Environment/Libraries
Requires: %{name}-system%{?_isa} = %{version}-%{release}

%description thread

Run-time component Boost.Thread library, which provides classes and
functions for managing multiple threads of execution, and for
synchronizing data between the threads or providing separate copies of
data specific to individual threads.

%package timer
Summary: Run-time component of boost timer library
Group: System Environment/Libraries
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}

%description timer

"How long does my C++ code take to run?"
The Boost Timer library answers that question and does so portably,
with as little as one #include and one additional line of code.

%package type_erasure
Summary: Run-time component of boost type erasure library
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}

%description type_erasure

The Boost.TypeErasure library provides runtime polymorphism in C++
that is more flexible than that provided by the core language.

%package wave
Summary: Run-time component of boost C99/C++ preprocessing library
Group: System Environment/Libraries
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-date-time%{?_isa} = %{version}-%{release}
Requires: %{name}-filesystem%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Requires: %{name}-thread%{?_isa} = %{version}-%{release}

%description wave

Run-time support for the Boost.Wave library, a Standards conforming,
and highly configurable implementation of the mandated C99/C++
preprocessor functionality.

%package devel
Summary: The Boost C++ headers and shared development libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libicu-devel%{?_isa}
%if %{with quadmath}
Requires: libquadmath-devel%{?_isa}
%endif

%description devel
Headers and shared object symbolic links for the Boost C++ libraries.

%package static
Summary: The Boost C++ static development libraries
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static Boost C++ libraries.

%package doc
Summary: HTML documentation for the Boost C++ libraries
Group: Documentation
%if 0%{?rhel} >= 6
BuildArch: noarch
%endif

%description doc
This package contains the documentation in the HTML format of the Boost C++
libraries. The documentation provides the same content as that on the Boost
web page (http://www.boost.org/doc/libs/%{version_enc}).

%package examples
Summary: Source examples for the Boost C++ libraries
Group: Documentation
%if 0%{?rhel} >= 6
BuildArch: noarch
%endif
Requires: %{name}-devel = %{version}-%{release}

%description examples
This package contains example source files distributed with boost.


%if %{with openmpi}

%package openmpi
Summary: Run-time component of Boost.MPI library
Group: System Environment/Libraries
BuildRequires: openmpi-devel
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}

%description openmpi

Run-time support for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-devel
Summary: Shared library symbolic links for Boost.MPI
Group: System Environment/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: %{name}-graph-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-devel

Devel package for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%if %{with python2}

%package openmpi-python2
Summary: Python 2 run-time component of Boost.MPI library
Group: System Environment/Libraries
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: %{name}-python2%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}

%description openmpi-python2

Python 2 support for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-python2-devel
Summary: Shared library symbolic links for Boost.MPI Python 2 component
Group: System Environment/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi-python2%{?_isa} = %{version}-%{release}

%description openmpi-python2-devel

Devel package for the Python 2 interface of Boost.MPI-OpenMPI, a library
providing a clean C++ API over the OpenMPI implementation of MPI.

%endif

%if %{with python3}

%package openmpi-python3
Summary: Python 3 run-time component of Boost.MPI library
Group: System Environment/Libraries
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: %{name}-python3%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}

%description openmpi-python3

Python 3 support for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-python3-devel
Summary: Shared library symbolic links for Boost.MPI Python 3 component
Group: System Environment/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-python3-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi-python3%{?_isa} = %{version}-%{release}

%description openmpi-python3-devel

Devel package for the Python 3 interface of Boost.MPI-OpenMPI, a library
providing a clean C++ API over the OpenMPI implementation of MPI.

%endif

%package graph-openmpi
Summary: Run-time component of parallel boost graph library
Group: System Environment/Libraries
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}

%description graph-openmpi

Run-time support for the Parallel BGL graph library.  The interface and
graph components are generic, in the same sense as the Standard
Template Library (STL).  This libraries in this package use OpenMPI
back-end to do the parallel work.

%endif


%if %{with mpich}

%package mpich
Summary: Run-time component of Boost.MPI library
Group: System Environment/Libraries
BuildRequires: mpich-devel
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}

%description mpich

Run-time support for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-devel
Summary: Shared library symbolic links for Boost.MPI
Group: System Environment/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: %{name}-graph-mpich%{?_isa} = %{version}-%{release}

%description mpich-devel

Devel package for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%if %{with python2}

%package mpich-python2
Summary: Python run-time component of Boost.MPI library
Group: System Environment/Libraries
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: %{name}-python2%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}

%description mpich-python2

Python 2 support for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-python2-devel
Summary: Shared library symbolic links for Boost.MPI Python 2 component
Group: System Environment/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-mpich-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-mpich-python2%{?_isa} = %{version}-%{release}

%description mpich-python2-devel

Devel package for the Python 2 interface of Boost.MPI-MPICH, a library
providing a clean C++ API over the MPICH implementation of MPI.

%endif

%if %{with python3}

%package mpich-python3
Summary: Python 3 run-time component of Boost.MPI library
Group: System Environment/Libraries
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: %{name}-python3%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}

%description mpich-python3

Python 3 support for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-python3-devel
Summary: Shared library symbolic links for Boost.MPI Python 3 component
Group: System Environment/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-python3-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-mpich-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-mpich-python3%{?_isa} = %{version}-%{release}

%description mpich-python3-devel

Devel package for the Python 3 interface of Boost.MPI-MPICH, a library
providing a clean C++ API over the MPICH implementation of MPI.

%endif

%package graph-mpich
Summary: Run-time component of parallel boost graph library
Group: System Environment/Libraries
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}

%description graph-mpich

Run-time support for the Parallel BGL graph library.  The interface and
graph components are generic, in the same sense as the Standard
Template Library (STL).  This libraries in this package use MPICH
back-end to do the parallel work.

%endif # with mpich

%package build
Summary: Cross platform build system for C++ projects
Group: Development/Tools
Requires: %{name}-jam
BuildArch: noarch

%description build
Boost.Build is an easy way to build C++ projects, everywhere. You name
your pieces of executable and libraries and list their sources.  Boost.Build
takes care about compiling your sources with the right options,
creating static and shared libraries, making pieces of executable, and other
chores -- whether you are using GCC, MSVC, or a dozen more supported
C++ compilers -- on Windows, OSX, Linux and commercial UNIX systems.

%package doctools
Summary: Tools for working with Boost documentation
Group: Applications/Publishing
Requires: docbook-dtds
Requires: docbook-style-xsl

%description doctools

Tools for working with Boost documentation in BoostBook or QuickBook format.

%package jam
Summary: A low-level build tool
Group: Development/Tools

%description jam
Boost.Jam (BJam) is the low-level build engine tool for Boost.Build.
Historically, Boost.Jam is based on on FTJam and on Perforce Jam but has grown
a number of significant features and is now developed independently.

%prep
%setup -q -n %{toplev_dirname}
find ./boost -name '*.hpp' -perm /111 | xargs chmod a-x

%patch4 -p1
%patch5 -p1
%patch15 -p0
%patch25 -p1
%patch51 -p1
%patch61 -p1
%patch62 -p1
%patch65 -p1
%patch82 -p1
%patch83 -p1

%build
# Dump the versions being used into the build logs.
%if %{with python2}
%global python2_version %(/usr/bin/python2 %{SOURCE2})
: PYTHON2_VERSION=%{python2_version}
%endif
%if %{with python3}
%global python3_version %(/usr/bin/python3 %{SOURCE2})
%global python3_abiflags %(/usr/bin/python3-config --abiflags)
: PYTHON3_VERSION=%{python3_version}
: PYTHON3_ABIFLAGS=%{python3_abiflags}
%endif

# There are many strict aliasing warnings, and it's not feasible to go
# through them all at this time.
# There are also lots of noisy but harmless unused local typedef warnings.
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-unused-local-typedefs -Wno-deprecated-declarations"
export RPM_LD_FLAGS

cat > ./tools/build/src/user-config.jam << "EOF"
import os ;
local RPM_OPT_FLAGS = [ os.environ RPM_OPT_FLAGS ] ;
local RPM_LD_FLAGS = [ os.environ RPM_LD_FLAGS ] ;

using gcc : : : <compileflags>$(RPM_OPT_FLAGS) <linkflags>$(RPM_LD_FLAGS) ;
%if %{with openmpi} || %{with mpich}
using mpi ;
%endif
%if %{with python2}
using python : %{python2_version} : /usr/bin/python2 : /usr/include/python%{python2_version} : : : : ;
%endif
EOF

./bootstrap.sh --with-toolset=gcc --with-icu

# N.B. When we build the following with PCH, parts of boost (math
# library in particular) end up being built second time during
# installation.  Unsure why that is, but all sub-builds need to be
# built with pch=off to avoid this.

echo ============================= build serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
%if !%{with context}
	--without-context --without-coroutine \
	--without-fiber \
%endif
%if !%{with python2}
	--without-python \
%endif
	variant=release threading=multi debug-symbols=on pch=off \
%if %{with python2}
	python=%{python2_version} \
%endif
	stage

# See libs/thread/build/Jamfile.v2 for where this file comes from.
if [ $(find serial -type f -name has_atomic_flag_lockfree \
		-print -quit | wc -l) -ne 0 ]; then
	DEF=D
else
	DEF=U
fi

m4 -${DEF}HAS_ATOMIC_FLAG_LOCKFREE -DVERSION=%{version} \
	%{SOURCE1} > $(basename %{SOURCE1})

%if %{with python3}

# Previously, we built python 2.x and 3.x interfaces simultaneously.
# However, this does not work once trying to build other Python components
# such as libboost_numpy.  Therefore, we build for each separately, while
# minimizing duplicate compilation as much as possible.

cat > python3-config.jam << "EOF"
import os ;
local RPM_OPT_FLAGS = [ os.environ RPM_OPT_FLAGS ] ;
local RPM_LD_FLAGS = [ os.environ RPM_LD_FLAGS ] ;

using gcc : : : <compileflags>$(RPM_OPT_FLAGS) <linkflags>$(RPM_LD_FLAGS) ;
%if %{with openmpi} || %{with mpich}
using mpi ;
%endif
EOF

cat >> python3-config.jam << EOF
using python : %{python3_version} : /usr/bin/python3 : /usr/include/python%{python3_version}%{python3_abiflags} : : : : %{python3_abiflags} ;
EOF

echo ============================= build serial-py3 ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-python --build-dir=serial-py3 \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

%endif

# Build MPI parts of Boost with OpenMPI support

%if %{with openmpi} || %{with mpich}
# First, purge all modules so that user environment does not conflict
# with the build.
module purge ||:
%endif

%if %{with openmpi}
%{_openmpi_load}
%if %{with python2}
echo ============================= build $MPI_COMPILER ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python2_version} stage
%endif

%if %{with python3}
echo ============================= build $MPI_COMPILER-py3 ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER-py3 \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage
%endif

%{_openmpi_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

# Build MPI parts of Boost with MPICH support
%if %{with mpich}
%{_mpich_load}
%if %{with python2}
echo ============================= build $MPI_COMPILER ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python2_version} stage
%endif

%if %{with python3}
echo ============================= build $MPI_COMPILER-py3 ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER-py3 \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage
%endif

%{_mpich_unload}
export PATH=/bin${PATH:+:}$PATH
%endif # with mpich

echo ============================= build Boost.Build ==================
(cd tools/build
 ./bootstrap.sh --with-toolset=gcc)

%check
:


%install
rm -rf $RPM_BUILD_ROOT
cd %{_builddir}/%{toplev_dirname}

%if %{with openmpi} || %{with mpich}
# First, purge all modules so that user environment does not conflict
# with the build.
module purge ||:
%endif

%if %{with openmpi}
%{_openmpi_load}
# XXX We want to extract this from RPM flags
# b2 instruction-set=i686 etc.
%if %{with python2}
echo ============================= install $MPI_COMPILER ==================
./b2 -q %{?_smp_mflags} \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER \
	--stagedir=${RPM_BUILD_ROOT}${MPI_HOME} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python2_version} stage

# Move Python module to proper location for automatic loading
mkdir -p ${RPM_BUILD_ROOT}%{python2_sitearch}/openmpi/boost
touch ${RPM_BUILD_ROOT}%{python2_sitearch}/openmpi/boost/__init__.py
mv ${RPM_BUILD_ROOT}${MPI_HOME}/lib/mpi.so \
   ${RPM_BUILD_ROOT}%{python2_sitearch}/openmpi/boost/
%endif

%if %{with python3}
echo ============================= install $MPI_COMPILER-py3 ==================
./b2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER-py3 \
	--stagedir=${RPM_BUILD_ROOT}${MPI_HOME} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

# Move Python module to proper location for automatic loading
mkdir -p ${RPM_BUILD_ROOT}%{python3_sitearch}/openmpi/boost
touch ${RPM_BUILD_ROOT}%{python3_sitearch}/openmpi/boost/__init__.py
mv ${RPM_BUILD_ROOT}${MPI_HOME}/lib/mpi.so \
   ${RPM_BUILD_ROOT}%{python3_sitearch}/openmpi/boost/
%endif

# Remove generic parts of boost that were built for dependencies.
rm -f ${RPM_BUILD_ROOT}${MPI_HOME}/lib/libboost_{python,{w,}serialization}*

%{_openmpi_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

%if %{with mpich}
%{_mpich_load}
%if %{with python2}
echo ============================= install $MPI_COMPILER ==================
./b2 -q %{?_smp_mflags} \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER \
	--stagedir=${RPM_BUILD_ROOT}${MPI_HOME} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python2_version} stage

# Move Python module to proper location for automatic loading
mkdir -p ${RPM_BUILD_ROOT}%{python2_sitearch}/mpich/boost
touch ${RPM_BUILD_ROOT}%{python2_sitearch}/mpich/boost/__init__.py
mv ${RPM_BUILD_ROOT}${MPI_HOME}/lib/mpi.so \
   ${RPM_BUILD_ROOT}%{python2_sitearch}/mpich/boost/
%endif

%if %{with python3}
echo ============================= install $MPI_COMPILER-py3 ==================
./b2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER-py3 \
	--stagedir=${RPM_BUILD_ROOT}${MPI_HOME} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

# Move Python module to proper location for automatic loading
mkdir -p ${RPM_BUILD_ROOT}%{python3_sitearch}/mpich/boost
touch ${RPM_BUILD_ROOT}%{python3_sitearch}/mpich/boost/__init__.py
mv ${RPM_BUILD_ROOT}${MPI_HOME}/lib/mpi.so \
   ${RPM_BUILD_ROOT}%{python3_sitearch}/mpich/boost/
%endif

# Remove generic parts of boost that were built for dependencies.
rm -f ${RPM_BUILD_ROOT}${MPI_HOME}/lib/libboost_{python,{w,}serialization}*

%{_mpich_unload}
export PATH=/bin${PATH:+:}$PATH
%endif # with mpich

echo ============================= install serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
%if !%{with context}
	--without-context --without-coroutine \
	--without-fiber \
%endif
%if !%{with python2}
	--without-python \
%endif
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--libdir=$RPM_BUILD_ROOT%{_libdir} \
	variant=release threading=multi debug-symbols=on pch=off \
%if %{with python2}
	python=%{python2_version} \
%endif
	install

# Override DSO symlink with a linker script.  See the linker script
# itself for details of why we need to do this.
[ -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so ] # Must be present
rm -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so
install -p -m 644 $(basename %{SOURCE1}) $RPM_BUILD_ROOT%{_libdir}/

%if %{with python3}
echo ============================= install serial-py3 ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--user-config=python3-config.jam \
	--with-python --build-dir=serial-py3 \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--libdir=$RPM_BUILD_ROOT%{_libdir} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} install

%endif

echo ============================= install Boost.Build ==================
(cd tools/build
 ./b2 --prefix=$RPM_BUILD_ROOT%{_prefix} install
 # Fix some permissions
 chmod -x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/build/alias.py
 chmod -x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/kernel/boost-build.jam
 chmod -x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/options/help.jam
 chmod +x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxproc.py
 # Fix shebang using unversioned python
 sed -i '1s@^#!/usr/bin.python$@&3@' $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxproc.py
 # We don't want to distribute this
 rm -f $RPM_BUILD_ROOT%{_bindir}/b2
 # Not a real file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/src/build/project.ann.py
 # Empty file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxygen/windows-paths-check.hpp
 # Install the manual page
 %{__install} -p -m 644 v2/doc/bjam.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/bjam.1
)

echo ============================= install Boost.QuickBook ==================
(cd tools/quickbook
 ../build/b2 --prefix=$RPM_BUILD_ROOT%{_prefix}
 %{__install} -p -m 755 ../../dist/bin/quickbook $RPM_BUILD_ROOT%{_bindir}/
 cd ../boostbook
 find dtd -type f -name '*.dtd' | while read tobeinstalledfiles; do
   install -p -m 644 $tobeinstalledfiles -D $RPM_BUILD_ROOT%{_datadir}/boostbook/$tobeinstalledfiles
 done
 find xsl -type f | while read tobeinstalledfiles; do
   install -p -m 644 $tobeinstalledfiles -D $RPM_BUILD_ROOT%{_datadir}/boostbook/$tobeinstalledfiles
 done
)

# Install documentation files (HTML pages) within the temporary place
echo ============================= install documentation ==================
# Prepare the place to temporarily store the generated documentation
rm -rf %{boost_docdir} && %{__mkdir_p} %{boost_docdir}/html
DOCPATH=%{boost_docdir}
DOCREGEX='.*\.\(html?\|css\|png\|gif\)'

find libs doc more -type f -regex $DOCREGEX \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories

sed "s:^:$DOCPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d

cat tmp-doc-directories | while read tobeinstalleddocdir; do
    find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -regex $DOCREGEX -print0 \
    | xargs -P 0 -0 %{__install} -p -m 644 -t $DOCPATH/$tobeinstalleddocdir
done
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $DOCPATH LICENSE_1_0.txt index.htm index.html boost.png rst.css boost.css

echo ============================= install examples ==================
# Fix a few non-standard issues (DOS and/or non-UTF8 files)
sed -i -e 's/\r//g' libs/geometry/example/ml02_distance_strategy.cpp
for tmp_doc_file in flyweight/example/Jamfile.v2 \
 format/example/sample_new_features.cpp multi_index/example/Jamfile.v2 \
 multi_index/example/hashed.cpp serialization/example/demo_output.txt
do
  mv libs/${tmp_doc_file} libs/${tmp_doc_file}.iso8859
  iconv -f ISO8859-1 -t UTF8 < libs/${tmp_doc_file}.iso8859 > libs/${tmp_doc_file}
  touch -r libs/${tmp_doc_file}.iso8859 libs/${tmp_doc_file}
  rm -f libs/${tmp_doc_file}.iso8859
done

# Prepare the place to temporarily store the examples
rm -rf %{boost_examplesdir} && mkdir -p %{boost_examplesdir}/html
EXAMPLESPATH=%{boost_examplesdir}
find libs -type d -name example -exec find {} -type f \; \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories
sed "s:^:$EXAMPLESPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d
rm -f tmp-doc-files-to-be-installed && touch tmp-doc-files-to-be-installed
cat tmp-doc-directories | while read tobeinstalleddocdir
do
  find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -type f \
    >> tmp-doc-files-to-be-installed
done
cat tmp-doc-files-to-be-installed | while read tobeinstalledfiles
do
  if test -s $tobeinstalledfiles
  then
    tobeinstalleddocdir=`dirname $tobeinstalledfiles`
    %{__install} -p -m 644 -t $EXAMPLESPATH/$tobeinstalleddocdir $tobeinstalledfiles
  fi
done
rm -f tmp-doc-files-to-be-installed
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $EXAMPLESPATH LICENSE_1_0.txt

##
# Perform the necessary renaming according to package renaming
# Build Tools
mv -f $RPM_BUILD_ROOT%{_datadir}/{%{real_name}-build,%{name}-build}
mv -f $RPM_BUILD_ROOT%{_bindir}/{bjam,bjam%{version_suffix}}
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/{bjam.1,bjam%{version_suffix}.1}

# MPI
mkdir -p $RPM_BUILD_ROOT{%{_includedir},%{_libdir}/{.,{mpich,mpich2,openmpi}/lib}}/%{name}
mv -f $RPM_BUILD_ROOT%{_includedir}/{%{real_name},%{name}}
mv -f $RPM_BUILD_ROOT%{_libdir}/{*.a,%{name}}
for library in $RPM_BUILD_ROOT%{_libdir}/*.so
do
  rm -f $library
  ln -s ../$(basename $library).%{sonamever} $RPM_BUILD_ROOT%{_libdir}/%{name}/$(basename $library)
done

%if %{with mpich}
mv -f $RPM_BUILD_ROOT%{_libdir}/mpich/lib/{*.a,%{name}}
#mv -f $RPM_BUILD_ROOT%%{python2_sitearch}/mpich/boost/{mpi.so,%%{name}}
for library in $RPM_BUILD_ROOT%{_libdir}/mpich/lib/*.so
do
  rm -f $library
  ln -s ../$(basename $library).%{sonamever} $RPM_BUILD_ROOT%{_libdir}/mpich/lib/%{name}/$(basename $library)
done
%endif # with mpich

%if %{with openmpi}
	%if 0%{?rhel} == 5
		mv -f $RPM_BUILD_ROOT%{_libdir}/openmpi/{1.4-gcc/lib/*,lib}
	%endif
mv -f $RPM_BUILD_ROOT%{_libdir}/openmpi/lib/{*.a,%{name}}
#mv -f $RPM_BUILD_ROOT%%{python2_sitearch}/openmpi/boost/{mpi.so,%%{name}}
for library in $RPM_BUILD_ROOT%{_libdir}/openmpi/lib/*.so
do
  rm -f $library
  ln -s ../$(basename $library).%{sonamever} $RPM_BUILD_ROOT%{_libdir}/openmpi/lib/%{name}/$(basename $library)
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT


# MPI subpackages don't need the ldconfig magic.  They are hidden by
# default, in MPI back-end-specific directory, and only show to the
# user after the relevant environment module has been loaded.
# rpmlint will report that as errors, but it is fine.

%post atomic -p /sbin/ldconfig

%postun atomic -p /sbin/ldconfig

%post chrono -p /sbin/ldconfig

%postun chrono -p /sbin/ldconfig

%post container -p /sbin/ldconfig

%postun container -p /sbin/ldconfig

%post contract -p /sbin/ldconfig

%postun contract -p /sbin/ldconfig

%if %{with context}
%post context -p /sbin/ldconfig

%postun context -p /sbin/ldconfig

%post coroutine -p /sbin/ldconfig

%postun coroutine -p /sbin/ldconfig
%endif

%post date-time -p /sbin/ldconfig

%postun date-time -p /sbin/ldconfig

%post filesystem -p /sbin/ldconfig

%postun filesystem -p /sbin/ldconfig

%post graph -p /sbin/ldconfig

%postun graph -p /sbin/ldconfig

%post iostreams -p /sbin/ldconfig

%postun iostreams -p /sbin/ldconfig

%post locale -p /sbin/ldconfig

%postun locale -p /sbin/ldconfig

%post log -p /sbin/ldconfig

%postun log -p /sbin/ldconfig

%post math -p /sbin/ldconfig

%postun math -p /sbin/ldconfig

%post program-options -p /sbin/ldconfig

%postun program-options -p /sbin/ldconfig

%if %{with python2}
%post python2 -p /sbin/ldconfig

%postun python2 -p /sbin/ldconfig
%endif

%if %{with python3}
%post python3 -p /sbin/ldconfig

%postun python3 -p /sbin/ldconfig
%endif

%post random -p /sbin/ldconfig

%postun random -p /sbin/ldconfig

%post regex -p /sbin/ldconfig

%postun regex -p /sbin/ldconfig

%post serialization -p /sbin/ldconfig

%postun serialization -p /sbin/ldconfig

%post system -p /sbin/ldconfig

%postun system -p /sbin/ldconfig

%post test -p /sbin/ldconfig

%postun test -p /sbin/ldconfig

%post thread -p /sbin/ldconfig

%postun thread -p /sbin/ldconfig

%post timer -p /sbin/ldconfig

%postun timer -p /sbin/ldconfig

%post type_erasure -p /sbin/ldconfig

%postun type_erasure -p /sbin/ldconfig

%post wave -p /sbin/ldconfig

%postun wave -p /sbin/ldconfig

%post doctools
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://www.boost.org/tools/boostbook/dtd" \
 "file://%{_datadir}/boostbook/dtd" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://www.boost.org/tools/boostbook/dtd" \
 "file://%{_datadir}/boostbook/dtd" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://www.boost.org/tools/boostbook/xsl" \
 "file://%{_datadir}/boostbook/xsl" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://www.boost.org/tools/boostbook/xsl" \
 "file://%{_datadir}/boostbook/xsl" $CATALOG

%postun doctools
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_datadir}/boostbook/dtd" $CATALOG
  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_datadir}/boostbook/xsl" $CATALOG
fi


%files
%defattr(-, root, root, -)
%license LICENSE_1_0.txt

%files atomic
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_atomic*.so.%{sonamever}

%files chrono
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_chrono*.so.%{sonamever}

%files container
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_container*.so.%{sonamever}

%if %{with context}

%files context
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_context*.so.%{sonamever}

%files coroutine
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_coroutine*.so.%{sonamever}

%endif

%files date-time
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_date_time*.so.%{sonamever}

%if %{with context}
%files fiber
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
#%%{_libdir}/libboost_fiber*.so.%%{sonamever}
%endif

%files filesystem
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_filesystem*.so.%{sonamever}

%files graph
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_graph*.so.%{sonamever}

%files iostreams
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_iostreams*.so.%{sonamever}

%files locale
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_locale*.so.%{sonamever}

%files log
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_log*.so.%{sonamever}

%files math
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_math_c99.so.%{sonamever}
%{_libdir}/libboost_math_c99f*.so.%{sonamever}
%{_libdir}/libboost_math_c99l*.so.%{sonamever}
%{_libdir}/libboost_math_tr1.so.%{sonamever}
%{_libdir}/libboost_math_tr1f*.so.%{sonamever}
%{_libdir}/libboost_math_tr1l*.so.%{sonamever}

%if %{with python2}
%files numpy2
%license LICENSE_1_0.txt
%{_libdir}/libboost_numpy2*.so.%{sonamever}
%endif

%if %{with python3}
%files numpy3
%license LICENSE_1_0.txt
%{_libdir}/libboost_numpy3*.so.%{sonamever}
%endif

%files test
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_prg_exec_monitor*.so.%{sonamever}
%{_libdir}/libboost_unit_test_framework*.so.%{sonamever}

%files program-options
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_program_options*.so.%{sonamever}

%if %{with python2}
%files python2
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_python2*.so.%{sonamever}

%files python2-devel
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
#%%{_libdir}/libboost_numpy2*.so
#%%{_libdir}/libboost_python2*.so
%endif

%if %{with python3}
%files python3
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_python3*.so.%{sonamever}

%files python3-devel
%license LICENSE_1_0.txt
#%%{_libdir}/libboost_numpy3*.so
#%%{_libdir}/libboost_python3*.so
%endif

%files random
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_random*.so.%{sonamever}

%files regex
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_regex*.so.%{sonamever}

%files serialization
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_serialization*.so.%{sonamever}
%{_libdir}/libboost_wserialization*.so.%{sonamever}

%files stacktrace
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_stacktrace_addr2line*.so.%{sonamever}
%{_libdir}/libboost_stacktrace_basic*.so.%{sonamever}
%{_libdir}/libboost_stacktrace_noop*.so.%{sonamever}

%files system
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_system*.so.%{sonamever}

%files thread
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_thread*.so.%{sonamever}

%files timer
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_timer*.so.%{sonamever}

%files type_erasure
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_type_erasure*.so.%{sonamever}

%files wave
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_wave*.so.%{sonamever}

%files contract
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/libboost_contract*.so.%{sonamever}

%files doc
%defattr(-, root, root, -)
%doc %{boost_docdir}/*

%files examples
%defattr(-, root, root, -)
%doc %{boost_examplesdir}/*

%files devel
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_includedir}/%{name}
%{_libdir}/%{name}/libboost_*.so

%files static
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/%{name}/*.a
%if %{with mpich}
%{_libdir}/mpich/lib/%{name}/*.a
%endif # with mpich
%if %{with openmpi}
%{_libdir}/openmpi/lib/%{name}/*.a
%endif

# OpenMPI packages
%if %{with openmpi}

%files openmpi
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi*.so.%{sonamever}

%files openmpi-devel
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/%{name}/libboost_*.so

%if %{with python2}

%files openmpi-python2
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi_python2*.so.%{sonamever}
%{python2_sitearch}/openmpi/boost/

%files openmpi-python2-devel
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/%{name}/libboost_mpi_python2*.so

%endif

%if %{with python3}

%files openmpi-python3
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi_python3*.so.%{sonamever}
%{python3_sitearch}/openmpi/boost/

%files openmpi-python3-devel
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/%{name}/libboost_mpi_python3*.so

%endif

%files graph-openmpi
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_graph_parallel*.so.%{sonamever}

%endif

# MPICH packages
%if %{with mpich}

%files mpich
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi*.so.%{sonamever}

%files mpich-devel
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/%{name}/libboost_*.so

%if %{with python2}

%files mpich-python2
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi_python2*.so.%{sonamever}
%{python2_sitearch}/mpich/boost/

%files mpich-python2-devel
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/%{name}/libboost_mpi_python2*.so

%endif

%if %{with python3}

%files mpich-python3
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi_python3*.so.%{sonamever}
%{python3_sitearch}/mpich/boost/

%files mpich-python3-devel
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/%{name}/libboost_mpi_python3*.so

%endif

%files graph-mpich
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_graph_parallel*.so.%{sonamever}

%endif # with mpich

%files build
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_datadir}/%{name}-build/

%files doctools
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_bindir}/quickbook
%{_datadir}/boostbook/

%files jam
%defattr(-, root, root, -)
%license LICENSE_1_0.txt
%{_bindir}/bjam%{version_suffix}
%{_mandir}/man1/bjam%{version_suffix}.1*

%changelog
* Sat Jan 19 2019 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.69.0-1
- Transformed boost-1.69.0-1 into boost169-1.69.0-1 (BZ#xxx)
