# Support for documentation installation
# As the %%doc macro erases the target directory, namely
# $RPM_BUILD_ROOT%%{_docdir}/%%{name}-%%{version}, manually installed
# documentation must be saved into a temporary dedicated directory.
%define boost_docdir __tmp_docdir
%define boost_examplesdir __tmp_examplesdir

# Configuration of MPI back-ends
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
%if 0%{?rhel} == 5
%ifarch %{arm} ppc64
  %bcond_with mpich2
%else
  %bcond_without mpich2
%endif
%endif
%ifarch s390 s390x %{arm}
  # No OpenMPI support on these arches
  %bcond_with openmpi
%else
  %bcond_without openmpi
  # OpenMPI from RHEL 5 does not provide /etc/rpm/macros.openmpi-%{_arch}
  # Work around so far: http://fedoraproject.org/wiki/PackagingDrafts/MPI
  %if 0%{?rhel} == 5
    %define _openmpi_load \
      mpi-selector --set `mpi-selector --list | grep openmpi` \
      source %{_sysconfdir}/profile.d/mpi-selector.sh \
      export MPI_INCLUDE_PATH="%{_libdir}/openmpi/1.4-gcc/include" \
      export MPI_LIB="%{_libdir}/openmpi/1.4-gcc/lib" \
      export MPI_SUFFIX="_openmpi"
    %define _openmpi_unload \
      mpi-selector --unset \
      unset MPI_INCLUDE_PATH \
      unset MPI_LIB \
      unset MPI_SUFFIX
  %endif
%endif

Name: boost148
%define real_name boost
Summary: The free peer-reviewed portable C++ source libraries
Version: 1.48.0
%define version_enc 1_48_0
%define version_suffix 148
Release: 5%{?dist}
License: Boost and MIT and Python

# The CMake build framework (set of CMakeLists.txt and module.cmake files) is
# added on top of the official Boost release (http://www.boost.org), thanks to
# a dedicated patch. That CMake framework (and patch) is hosted and maintained
# on GitHub, for now in the following Git repository:
#   https://github.com/pocb/boost.git
# A clone also exists on Gitorious, where CMake-related work was formely done:
#   http://gitorious.org/boost/cmake
# Upstream work is synchronised thanks to the Ryppl's hosted Git clone:
#   https://github.com/ryppl/boost-svn/tree/trunk
%define toplev_dirname %{real_name}_%{version_enc}
URL: http://www.boost.org
Group: System Environment/Libraries
Source0: http://downloads.sourceforge.net/%{real_name}/%{toplev_dirname}.tar.bz2

# From the version 13 of Fedora, the Boost libraries are delivered
# with sonames equal to the Boost version (e.g., 1.41.0). On EPEL versions
# (e.g., EPEL 5), the Boost libraries are delivered with another scheme
# for sonames (e.g., a soname of 3 for EPEL 5).
# If for some reason you wish to set the sonamever yourself, you can do it here.
%define sonamever %{version}

# boost is an "umbrella" package that pulls in all other boost
# components, except for MPI sub-packages.  Those are "special": one
# does not necessarily need them and the more typical scenario, I
# think, will be that the developer wants to pick one MPI flavor.
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-date-time%{?_isa} = %{version}-%{release}
Requires: %{name}-filesystem%{?_isa} = %{version}-%{release}
Requires: %{name}-graph%{?_isa} = %{version}-%{release}
Requires: %{name}-iostreams%{?_isa} = %{version}-%{release}
Requires: %{name}-locale%{?_isa} = %{version}-%{release}
Requires: %{name}-math%{?_isa} = %{version}-%{release}
Requires: %{name}-program-options%{?_isa} = %{version}-%{release}
Requires: %{name}-python%{?_isa} = %{version}-%{release}
Requires: %{name}-random%{?_isa} = %{version}-%{release}
Requires: %{name}-regex%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}
Requires: %{name}-signals%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Requires: %{name}-test%{?_isa} = %{version}-%{release}
Requires: %{name}-thread%{?_isa} = %{version}-%{release}
Requires: %{name}-timer%{?_isa} = %{version}-%{release}
Requires: %{name}-wave%{?_isa} = %{version}-%{release}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: cmake
BuildRequires: libstdc++-devel%{?_isa}
BuildRequires: bzip2-devel%{?_isa}
BuildRequires: zlib-devel%{?_isa}
BuildRequires: python-devel%{?_isa}
BuildRequires: libicu-devel%{?_isa}
BuildRequires: chrpath

# CMake-related files (CMakeLists.txt and module.cmake files).
# That patch also contains Web-related documentation for the Trac Wiki
# devoted to "old" Boost-CMake (up-to-date until Boost-1.41.0).
Patch0: boost-1.48.0-cmakeify-full.patch
Patch1: boost-cmake-soname.patch

# The patch may break c++03, and there is therefore no plan yet to include
# it upstream: https://svn.boost.org/trac/boost/ticket/4999
Patch2: boost-1.48.0-signals-erase.patch

# https://svn.boost.org/trac/boost/ticket/5731
Patch3: boost-1.48.0-exceptions.patch

# https://svn.boost.org/trac/boost/ticket/6150
Patch4: boost-1.48.0-fix-non-utf8-files.patch

# Add a manual page for the sole executable, namely bjam, based on the
# on-line documentation:
# http://www.boost.org/boost-build2/doc/html/bbv2/overview.html
Patch5: boost-1.48.0-add-bjam-man-page.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=757385
# https://svn.boost.org/trac/boost/ticket/6182
Patch6: boost-1.48.0-lexical_cast-incomplete.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=756005
# https://svn.boost.org/trac/boost/ticket/6131
Patch7: boost-1.48.0-foreach.patch

# https://svn.boost.org/trac/boost/ticket/6165
Patch8: boost-1.48.0-gcc47-pthreads.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=781859
# https://svn.boost.org/trac/boost/ticket/6406 fixed
# https://svn.boost.org/trac/boost/ticket/6407 fixed
# https://svn.boost.org/trac/boost/ticket/6408
# https://svn.boost.org/trac/boost/ticket/6409 fixed
# https://svn.boost.org/trac/boost/ticket/6410
# https://svn.boost.org/trac/boost/ticket/6411 fixed
# https://svn.boost.org/trac/boost/ticket/6412 fixed
# https://svn.boost.org/trac/boost/ticket/6413
# https://svn.boost.org/trac/boost/ticket/6414 fixed
# https://svn.boost.org/trac/boost/ticket/6415
# https://svn.boost.org/trac/boost/ticket/6416 fixed
Patch9: boost-1.48.0-attribute.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=783660
# https://svn.boost.org/trac/boost/ticket/6459 fixed
Patch10: boost-1.48.0-long-double-1.patch
Patch11: boost-1.48.0-long-double.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=784654
Patch12: boost-1.48.0-polygon.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=807780
Patch13: boost-1.48.0-python3.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=824810
# https://svn.boost.org/trac/boost/ticket/6940
Patch14: boost-1.48.0-xtime.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=828856
# https://bugzilla.redhat.com/show_bug.cgi?id=828857
Patch15: boost-1.48.0-pool.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=832265
Patch16: boost-1.48.0-locale.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=907481
Patch17: boost-1.48.0-invalid-utf8.patch

%bcond_with tests
%bcond_with docs_generated

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been proposed for inclusion in the C++
Standards Committee''s upcoming C++ Standard Library Technical Report.)

%package chrono
Summary: Run-Time component of boost chrono library
Group: System Environment/Libraries

%description chrono

Run-Time support for Boost.Chrono, a set of useful time utilities.

%package date-time
Summary: Run-Time component of boost date-time library
Group: System Environment/Libraries

%description date-time

Run-Time support for Boost Date Time, set of date-time libraries based
on generic programming concepts.

%package filesystem
Summary: Run-Time component of boost filesystem library
Group: System Environment/Libraries

%description filesystem

Run-Time support for the Boost Filesystem Library, which provides
portable facilities to query and manipulate paths, files, and
directories.

%package graph
Summary: Run-Time component of boost graph library
Group: System Environment/Libraries

%description graph

Run-Time support for the BGL graph library.  BGL interface and graph
components are generic, in the same sense as the the Standard Template
Library (STL).

%package iostreams
Summary: Run-Time component of boost iostreams library
Group: System Environment/Libraries

%description iostreams

Run-Time support for Boost.IOStreams, a framework for defining streams,
stream buffers and i/o filters.

%package locale
Summary: Run-Time component of boost locale library
Group: System Environment/Libraries

%description locale

Run-Time support for Boost.Locale, a set of localization and Unicode
handling tools.

%package math
Summary: Math functions for boost TR1 library
Group: System Environment/Libraries

%description math

Run-Time support for C99 and C++ TR1 C-style Functions from math
portion of Boost.TR1.

%package program-options
Summary:  Run-Time component of boost program_options library
Group: System Environment/Libraries

%description program-options

Run-Time support of boost program options library, which allows program
developers to obtain (name, value) pairs from the user, via
conventional methods such as command line and configuration file.

%package python
Summary: Run-Time component of boost python library
Group: System Environment/Libraries

%description python

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for Boost Python Library.

%package random
Summary: Run-Time component of boost random library
Group: System Environment/Libraries

%description random

Run-Time support for boost random library.

%package regex
Summary: Run-Time component of boost regular expression library
Group: System Environment/Libraries

%description regex

Run-Time support for boost regular expression library.

%package serialization
Summary: Run-Time component of boost serialization library
Group: System Environment/Libraries

%description serialization

Run-Time support for serialization for persistence and marshaling.

%package signals
Summary: Run-Time component of boost signals and slots library
Group: System Environment/Libraries

%description signals

Run-Time support for managed signals & slots callback implementation.

%package system
Summary: Run-Time component of boost system support library
Group: System Environment/Libraries

%description system

Run-Time component of Boost operating system support library, including
the diagnostics support that will be part of the C++0x standard
library.

%package test
Summary: Run-Time component of boost test library
Group: System Environment/Libraries

%description test

Run-Time support for simple program testing, full unit testing, and for
program execution monitoring.

%package thread
Summary: Run-Time component of boost thread library
Group: System Environment/Libraries

%description thread

Run-Time component Boost.Thread library, which provides classes and
functions for managing multiple threads of execution, and for
synchronizing data between the threads or providing separate copies of
data specific to individual threads.

%package timer
Summary: Run-Time component of boost timer library
Group: System Environment/Libraries

%description timer

"How long does my C++ code take to run?"
The Boost Timer library answers that question and does so portably,
with as little as one #include and one additional line of code.

%package wave
Summary: Run-Time component of boost C99/C++ pre-processing library
Group: System Environment/Libraries

%description wave

Run-Time support for the Boost.Wave library, a Standards conforming,
and highly configurable implementation of the mandated C99/C++
pre-processor functionality.

%package devel
Summary: The Boost C++ headers and shared development libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: %{name}-python-devel = %{version}-%{release}
# for %%_datadir/cmake ownership, can consider making cmake-filesystem
# if this dep is a problem
#Requires: cmake

%description devel
Headers and shared object symbolic links for the Boost C++ libraries.

%package static
Summary: The Boost C++ static development libraries
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-devel-static < 1.34.1-14
Provides: %{name}-devel-static = %{version}-%{release}

%description static
Static Boost C++ libraries.

%package doc
Summary: HTML documentation for the Boost C++ libraries
Group: Documentation
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildArch: noarch
%endif
Provides: %{name}-python-docs = %{version}-%{release}

%description doc
This package contains the documentation in the HTML format of the Boost C++
libraries. The documentation provides the same content as that on the Boost
web page (http://www.boost.org/doc/libs/1_40_0).

%package examples
Summary: Source examples for the Boost C++ libraries
Group: Documentation
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildArch: noarch
%endif
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description examples
This package contains example source files distributed with boost.


%if %{with openmpi}

%package openmpi
Summary: Run-Time component of Boost.MPI library
Group: System Environment/Libraries
Requires: openmpi
BuildRequires: openmpi-devel

%description openmpi

Run-Time support for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-devel
Summary: Shared library symbolic links for Boost.MPI
Group: System Environment/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi-python%{?_isa} = %{version}-%{release}
Requires: %{name}-graph-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-devel

Devel package for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-python
Summary: Python run-time component of Boost.MPI library
Group: System Environment/Libraries
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-python

Python support for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package graph-openmpi
Summary: Run-Time component of parallel boost graph library
Group: System Environment/Libraries
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}

%description graph-openmpi

Run-Time support for the Parallel BGL graph library.  The interface and
graph components are generic, in the same sense as the the Standard
Template Library (STL).  This libraries in this package use OpenMPI
back-end to do the parallel work.

%endif


%if %{with mpich}

%package mpich
Summary: Run-Time component of Boost.MPI library
Group: System Environment/Libraries
Requires: mpich%{?_isa}
BuildRequires: mpich-devel
Requires: boost-serialization%{?_isa} = %{version}-%{release}
Provides: boost-mpich2 = %{version}-%{release}
Obsoletes: boost-mpich2 < 1.53.0-9

%description mpich

Run-Time support for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-devel
Summary: Shared library symbolic links for Boost.MPI
Group: System Environment/Libraries
Requires: boost-devel%{?_isa} = %{version}-%{release}
Requires: boost-mpich%{?_isa} = %{version}-%{release}
Requires: boost-mpich-python%{?_isa} = %{version}-%{release}
Requires: boost-graph-mpich%{?_isa} = %{version}-%{release}
Provides: boost-mpich2-devel = %{version}-%{release}
Obsoletes: boost-mpich2-devel < 1.53.0-9

%description mpich-devel

Devel package for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-python
Summary: Python run-time component of Boost.MPI library
Group: System Environment/Libraries
Requires: boost-mpich%{?_isa} = %{version}-%{release}
Requires: boost-python%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}
Provides: boost-mpich2-python = %{version}-%{release}
Obsoletes: boost-mpich2-python < 1.53.0-9

%description mpich-python

Python support for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package graph-mpich
Summary: Run-Time component of parallel boost graph library
Group: System Environment/Libraries
Requires: boost-mpich%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}
Provides: boost-graph-mpich2 = %{version}-%{release}
Obsoletes: boost-graph-mpich2 < 1.53.0-9

%description graph-mpich

Run-Time support for the Parallel BGL graph library.  The interface and
graph components are generic, in the same sense as the the Standard
Template Library (STL).  This libraries in this package use MPICH
back-end to do the parallel work.

%endif

%if %{with mpich2}

%package mpich2
Summary: Run-Time component of Boost.MPI library
Group: System Environment/Libraries
Requires: mpich2%{?_isa}
BuildRequires: mpich2-devel
Requires: boost-serialization%{?_isa} = %{version}-%{release}

%description mpich2

Run-Time support for Boost.MPI-MPICH2, a library providing a clean C++
API over the MPICH2 implementation of MPI.

%package mpich2-devel
Summary: Shared library symbolic links for Boost.MPI
Group: System Environment/Libraries
Requires: boost-devel%{?_isa} = %{version}-%{release}
Requires: boost-mpich2%{?_isa} = %{version}-%{release}
Requires: boost-mpich2-python%{?_isa} = %{version}-%{release}
Requires: boost-graph-mpich2%{?_isa} = %{version}-%{release}

%description mpich2-devel

Devel package for Boost.MPI-MPICH2, a library providing a clean C++
API over the MPICH2 implementation of MPI.

%package mpich2-python
Summary: Python run-time component of Boost.MPI library
Group: System Environment/Libraries
Requires: boost-mpich2%{?_isa} = %{version}-%{release}
Requires: boost-python%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}

%description mpich2-python

Python support for Boost.MPI-MPICH2, a library providing a clean C++
API over the MPICH2 implementation of MPI.

%package graph-mpich2
Summary: Run-Time component of parallel boost graph library
Group: System Environment/Libraries
Requires: boost-mpich2%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}

%description graph-mpich2

Run-Time support for the Parallel BGL graph library.  The interface and
graph components are generic, in the same sense as the the Standard
Template Library (STL).  This libraries in this package use MPICH2
back-end to do the parallel work.

%endif

%package build
Summary: Cross platform build system for C++ projects
Group: Development/Tools
Requires: %{name}-jam
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildArch: noarch
%endif

%description build
Boost.Build is an easy way to build C++ projects, everywhere. You name
your pieces of executable and libraries and list their sources.  Boost.Build
takes care about compiling your sources with the right options,
creating static and shared libraries, making pieces of executable, and other
chores -- whether you''re using GCC, MSVC, or a dozen more supported
C++ compilers -- on Windows, OSX, Linux and commercial UNIX systems.

%package jam
Summary: A low-level build tool
Group: Development/Tools

%description jam
Boost.Jam (BJam) is the low-level build engine tool for Boost.Build.
Historically, Boost.Jam is based on on FTJam and on Perforce Jam but has grown
a number of significant features and is now developed independently

%prep
%setup -q -n %{toplev_dirname}

# CMake framework (CMakeLists.txt, *.cmake and documentation files)
%patch0 -p1
sed 's/_FEDORA_SONAME/%{sonamever}/' %{PATCH1} | %{__patch} -p0 --fuzz=0

# Fixes
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p2
%patch8 -p0
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p3
%patch13 -p1
%if 0%{?rhel} >= 7
%patch14 -p1
%endif
%patch15 -p0
%patch16 -p1
%patch17 -p0

# Update path to boost-build 
sed -i "s,BOOST_BUILD_PATH = /usr/share/boost-build,BOOST_BUILD_PATH = %{_datadir}/%{name}-build,g" \
    tools/build/v2/engine/jambase.c tools/build/v2/engine/Jambase

%build
# Support for building tests.
%define boost_testflags -DBUILD_TESTS="NONE"
%if %{with tests}
  %define boost_testflags -DBUILD_TESTS="ALL"
%endif

( echo ============================= build serial ==================
  mkdir serial
  cd serial
  export CXXFLAGS="-DBOOST_IOSTREAMS_USE_DEPRECATED %{optflags}"
  %cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo %{boost_testflags} \
         -DENABLE_SINGLE_THREADED=YES -DINSTALL_VERSIONED=OFF \
         -DWITH_MPI=OFF \
         ..
  make VERBOSE=1 %{?_smp_mflags}
)

# Build MPI parts of Boost
%if %{with openmpi} || %{with mpich} || %{with mpich2}
# First, purge all modules so that user environment doesn't conflict
# with the build.
module purge ||:
%endif

# Build MPI parts of Boost with OpenMPI support
%if %{with openmpi}
%{_openmpi_load}
# Work around the bug: https://bugzilla.redhat.com/show_bug.cgi?id=560224
MPI_COMPILER=openmpi-%{_arch}
export MPI_COMPILER
( echo ============================= build $MPI_COMPILER ==================
  mkdir $MPI_COMPILER
  cd $MPI_COMPILER
  %cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo %{boost_testflags} \
         -DENABLE_SINGLE_THREADED=YES -DINSTALL_VERSIONED=OFF \
         -DBUILD_PROJECTS="serialization;python;mpi;graph_parallel" \
         -DBOOST_LIB_INSTALL_DIR=$MPI_LIB ..
  make VERBOSE=1 %{?_smp_mflags}
)
%{_openmpi_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

# Build MPI parts of Boost with MPICH support
%if %{with mpich}
%{_mpich_load}
( echo ============================= build $MPI_COMPILER ==================
  mkdir $MPI_COMPILER
  cd $MPI_COMPILER
  %cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo %{boost_testflags} \
         -DENABLE_SINGLE_THREADED=YES -DINSTALL_VERSIONED=OFF \
         -DBUILD_PROJECTS="serialization;python;mpi;graph_parallel" \
         -DBOOST_LIB_INSTALL_DIR=$MPI_LIB ..
  make VERBOSE=1 %{?_smp_mflags}
)
%{_mpich_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

# Build MPI parts of Boost with MPICH2 support
%if %{with mpich2}
%{_mpich2_load}
( echo ============================= build $MPI_COMPILER ==================
  mkdir $MPI_COMPILER
  cd $MPI_COMPILER
  %cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo %{boost_testflags} \
         -DENABLE_SINGLE_THREADED=YES -DINSTALL_VERSIONED=OFF \
         -DBUILD_PROJECTS="serialization;python;mpi;graph_parallel" \
         -DBOOST_LIB_INSTALL_DIR=$MPI_LIB ..
  make VERBOSE=1 %{?_smp_mflags}
)
%{_mpich2_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

# Build Boost Jam
echo ============================= build Jam ==================
pushd tools/build/v2/engine/
export CFLAGS="%{optflags}"
./build.sh
popd

%check
%if %{with tests}
cd build

# Standard test with CMake, depends on installed boost-test.
ctest --verbose --output-log testing.log
if [ -f testing.log ]; then
  echo "" >> testing.log
  echo `date` >> testing.log
  echo "" >> testing.log
  echo `uname -a` >> testing.log
  echo "" >> testing.log
  echo `g++ --version` >> testing.log
  echo "" >> testing.log
  testdate=`date +%Y%m%d`
  testarch=`uname -m`
  email=benjamin.kosnik@gmail.com
  bzip2 -f testing.log
  echo "sending results starting"
  echo | mutt -s "$testdate boost test $testarch" -a testing.log.bz2 $email
  echo "sending results finished"
else
  echo "error with results"
fi
cd %{_builddir}/%{toplev_dirname}
%endif


%install
rm -rf $RPM_BUILD_ROOT

cd %{_builddir}/%{toplev_dirname}

%if %{with openmpi} || %{with mpich} || %{with mpich2}
# First, purge all modules so that user environment doesn't conflict
# with the build.
module purge ||:
%endif

%if %{with openmpi}
%{_openmpi_load}
# Work around the bug: https://bugzilla.redhat.com/show_bug.cgi?id=560224
MPI_COMPILER=openmpi-%{_arch}
export MPI_COMPILER
echo ============================= install $MPI_COMPILER ==================
DESTDIR=$RPM_BUILD_ROOT make -C $MPI_COMPILER VERBOSE=1 install
# Remove parts of boost that we don't want installed in MPI directory.
rm -f $RPM_BUILD_ROOT/$MPI_LIB/libboost_{python,{w,}serialization}*
# Suppress the mpi.so python module, as it not currently properly
# generated (some dependencies are missing. It is temporary until
# upstream Boost-CMake fixes that (see
# http://lists.boost.org/boost-cmake/2009/12/0859.php for more
# details)
rm -f $RPM_BUILD_ROOT/$MPI_LIB/mpi.so
# Kill any debug library versions that may show up un-invited.
rm -f $RPM_BUILD_ROOT/$MPI_LIB/*-d.*
# Remove cmake configuration files used to build the Boost libraries
find $RPM_BUILD_ROOT/$MPI_LIB -name '*.cmake' -exec rm -f {} \;
%{_openmpi_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

%if %{with mpich}
%{_mpich_load}
echo ============================= install $MPI_COMPILER ==================
DESTDIR=$RPM_BUILD_ROOT make -C $MPI_COMPILER VERBOSE=1 install
# Remove parts of boost that we don't want installed in MPI directory.
rm -f $RPM_BUILD_ROOT/$MPI_LIB/libboost_{python,{w,}serialization}*
# Suppress the mpi.so python module, as it not currently properly
# generated (some dependencies are missing. It is temporary until
# upstream Boost-CMake fixes that (see
# http://lists.boost.org/boost-cmake/2009/12/0859.php for more
# details)
rm -f $RPM_BUILD_ROOT/$MPI_LIB/mpi.so
# Kill any debug library versions that may show up un-invited.
rm -f $RPM_BUILD_ROOT/$MPI_LIB/*-d.*
# Remove cmake configuration files used to build the Boost libraries
find $RPM_BUILD_ROOT/$MPI_LIB -name '*.cmake' -exec rm -f {} \;
%{_mpich_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

%if %{with mpich2}
%{_mpich2_load}
echo ============================= install $MPI_COMPILER ==================
DESTDIR=$RPM_BUILD_ROOT make -C $MPI_COMPILER VERBOSE=1 install
# Remove parts of boost that we don't want installed in MPI directory.
rm -f $RPM_BUILD_ROOT/$MPI_LIB/libboost_{python,{w,}serialization}*
# Suppress the mpi.so python module, as it not currently properly
# generated (some dependencies are missing. It is temporary until
# upstream Boost-CMake fixes that (see
# http://lists.boost.org/boost-cmake/2009/12/0859.php for more
# details)
rm -f $RPM_BUILD_ROOT/$MPI_LIB/mpi.so
# Kill any debug library versions that may show up un-invited.
rm -f $RPM_BUILD_ROOT/$MPI_LIB/*-d.*
# Remove cmake configuration files used to build the Boost libraries
find $RPM_BUILD_ROOT/$MPI_LIB -name '*.cmake' -exec rm -f {} \;
%{_mpich2_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

echo ============================= install serial ==================
DESTDIR=$RPM_BUILD_ROOT make -C serial VERBOSE=1 install
# Kill any debug library versions that may show up un-invited.
rm -f $RPM_BUILD_ROOT/%{_libdir}/*-d.*
# Remove cmake configuration files used to build the Boost libraries
find $RPM_BUILD_ROOT/%{_libdir} -name '*.cmake' -exec rm -f {} \;

echo ============================= install jam ==================
mkdir -p $RPM_BUILD_ROOT%{_bindir}
pushd tools/build/v2/engine/
%{__install} -m 755 bin.linux*/bjam $RPM_BUILD_ROOT%{_bindir}/bjam%{version_suffix}
popd
# Install the manual page
%{__install} -p -m 644 tools/build/v2/doc/bjam.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/bjam%{version_suffix}.1

echo ============================= install build ==================
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-build
pushd tools/build/v2
# Fix some permissions
chmod -x build/alias.py
chmod +x tools/doxproc.py
# Empty file
rm -f tools/doxygen/windows-paths-check.hpp
# Not a real file
rm -f build/project.ann.py
# Move into a dedicated location
cp -a boost-build.jam bootstrap.jam build-system.jam build/ kernel/ options/ tools/ util/ user-config.jam $RPM_BUILD_ROOT%{_datadir}/%{name}-build/
popd

# Install documentation files (HTML pages) within the temporary place
echo ============================= install documentation ==================
cd %{_builddir}/%{toplev_dirname}
# Prepare the place to temporary store the generated documentation
rm -rf %{boost_docdir} && %{__mkdir_p} %{boost_docdir}/html
DOCPATH=%{boost_docdir}
find libs doc more -type f \( -name \*.htm -o -name \*.html \) \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories
sed "s:^:$DOCPATH/:" tmp-doc-directories \
    | xargs --no-run-if-empty %{__install} -d
cat tmp-doc-directories | while read tobeinstalleddocdir; do
    find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -name \*.htm\* \
    | xargs %{__install} -p -m 644 -t $DOCPATH/$tobeinstalleddocdir
done
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $DOCPATH LICENSE_1_0.txt index.htm index.html

echo ============================= install examples ==================
# Fix a few non-standard issues (DOS and/or non-UTF8 files)
sed -i -e 's/\r//g' libs/geometry/example/ml02_distance_strategy.cpp
sed -i -e 's/\r//g' libs/geometry/example/ml02_distance_strategy.vcproj
for tmp_doc_file in flyweight/example/Jamfile.v2 \
 format/example/sample_new_features.cpp multi_index/example/Jamfile.v2 \
 multi_index/example/hashed.cpp serialization/example/demo_output.txt \
 test/example/cla/wide_string.cpp
do
  mv libs/${tmp_doc_file} libs/${tmp_doc_file}.iso8859
  iconv -f ISO8859-1 -t UTF8 < libs/${tmp_doc_file}.iso8859 > libs/${tmp_doc_file}
  touch -r libs/${tmp_doc_file}.iso8859 libs/${tmp_doc_file}
  rm -f libs/${tmp_doc_file}.iso8859
done

# Prepare the place to temporary store the examples
rm -rf %{boost_examplesdir} && mkdir -p %{boost_examplesdir}/html
EXAMPLESPATH=%{boost_examplesdir}
find libs -type d -name example -exec find {} -type f \; \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories
sed "s:^:$EXAMPLESPATH/:" tmp-doc-directories \
    | xargs --no-run-if-empty %{__install} -d
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

# Remove scripts used to generate include files
find $RPM_BUILD_ROOT%{_includedir}/ \( -name '*.pl' -o -name '*.sh' \) -exec rm -f {} \;

# boost support of cmake needs some tuning.  For the time being, leave
# the files out, and rely on cmake's FindBoost to DTRT, as it had been
# doing in pre-cmake-boost times.  For further info, see:
#   https://bugzilla.redhat.com/show_bug.cgi?id=597020
rm -Rfv $RPM_BUILD_ROOT%{_datadir}/%{real_name}-%{version}
rm -Rfv $RPM_BUILD_ROOT%{_datadir}/cmake/%{real_name}

# Perform the necessary renaming according to package renaming
mkdir -p $RPM_BUILD_ROOT{%{_includedir},%{_libdir}/{.,{mpich,openmpi}/lib}}/%{name}
mv -f $RPM_BUILD_ROOT%{_includedir}/{%{real_name},%{name}}
mv -f $RPM_BUILD_ROOT%{_libdir}/{*.a,%{name}}
for library in $RPM_BUILD_ROOT%{_libdir}/*.so
do
  rm -f $library
  ln -s ../$(basename $library).%{sonamever} $RPM_BUILD_ROOT%{_libdir}/%{name}/$(basename $library)
done

%if %{with mpich} || %{with mpich2}
mv -f $RPM_BUILD_ROOT%{_libdir}/mpich/lib/{*.a,%{name}}
for library in $RPM_BUILD_ROOT%{_libdir}/mpich/lib/*.so
do
  rm -f $library
  ln -s ../$(basename $library).%{sonamever} $RPM_BUILD_ROOT%{_libdir}/mpich/lib/%{name}/$(basename $library)
done
%endif

%if %{with openmpi}
	%if 0%{?rhel} == 5
		mv -f $RPM_BUILD_ROOT%{_libdir}/openmpi/{1.4-gcc/lib/*,lib}
	%endif
mv -f $RPM_BUILD_ROOT%{_libdir}/openmpi/lib/{*.a,%{name}}
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

%post chrono -p /sbin/ldconfig

%postun chrono -p /sbin/ldconfig

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

%post math -p /sbin/ldconfig

%postun math -p /sbin/ldconfig

%post program-options -p /sbin/ldconfig

%postun program-options -p /sbin/ldconfig

%post python -p /sbin/ldconfig

%postun python -p /sbin/ldconfig

%post random -p /sbin/ldconfig

%postun random -p /sbin/ldconfig

%post regex -p /sbin/ldconfig

%postun regex -p /sbin/ldconfig

%post serialization -p /sbin/ldconfig

%postun serialization -p /sbin/ldconfig

%post signals -p /sbin/ldconfig

%postun signals -p /sbin/ldconfig

%post system -p /sbin/ldconfig

%postun system -p /sbin/ldconfig

%post test -p /sbin/ldconfig

%postun test -p /sbin/ldconfig

%post thread -p /sbin/ldconfig

%postun thread -p /sbin/ldconfig

%post timer -p /sbin/ldconfig

%postun timer -p /sbin/ldconfig

%post wave -p /sbin/ldconfig

%postun wave -p /sbin/ldconfig



%files
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt

%files chrono
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_chrono*.so.%{sonamever}

%files date-time
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_date_time*.so.%{sonamever}

%files filesystem
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_filesystem*.so.%{sonamever}

%files graph
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_graph.so.%{sonamever}
%{_libdir}/libboost_graph-mt.so.%{sonamever}

%files iostreams
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_iostreams*.so.%{sonamever}

%files locale
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_locale*.so.%{sonamever}

%files math
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_math*.so.%{sonamever}

%files test
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_prg_exec_monitor*.so.%{sonamever}
%{_libdir}/libboost_unit_test_framework*.so.%{sonamever}

%files program-options
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_program_options*.so.%{sonamever}

%files python
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_python*.so.%{sonamever}

%files random
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_random*.so.%{sonamever}

%files regex
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_regex*.so.%{sonamever}

%files serialization
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_serialization*.so.%{sonamever}
%{_libdir}/libboost_wserialization*.so.%{sonamever}

%files signals
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_signals*.so.%{sonamever}

%files system
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_system*.so.%{sonamever}

%files thread
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_thread*.so.%{sonamever}

%files timer
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_timer*.so.%{sonamever}

%files wave
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_wave*.so.%{sonamever}

%files doc
%defattr(-, root, root, -)
%doc %{boost_docdir}/*

%files examples
%defattr(-, root, root, -)
%doc %{boost_examplesdir}/*

%files devel
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_includedir}/%{name}
%{_libdir}/%{name}/libboost_*.so

%files static
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/%{name}/*.a
%if %{with mpich} || %{with mpich2}
%{_libdir}/mpich/lib/%{name}/*.a
%endif
%if %{with openmpi}
%{_libdir}/openmpi/lib/%{name}/*.a
%endif

# OpenMPI packages
%if %{with openmpi}

%files openmpi
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi.so.%{sonamever}
%{_libdir}/openmpi/lib/libboost_mpi-mt.so.%{sonamever}

%files openmpi-devel
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/openmpi/lib/%{name}/libboost_*.so

%files openmpi-python
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi_python*.so.%{sonamever}

%files graph-openmpi
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_graph_parallel.so.%{sonamever}
%{_libdir}/openmpi/lib/libboost_graph_parallel-mt.so.%{sonamever}

%endif

# MPICH packages
%if %{with mpich} || %{with mpich2}

%files mpich
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi.so.%{sonamever}
%{_libdir}/mpich/lib/libboost_mpi-mt.so.%{sonamever}

%files mpich-devel
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/mpich/lib/%{name}/libboost_*.so

%files mpich-python
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi_python*.so.%{sonamever}

%files graph-mpich
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_graph_parallel.so.%{sonamever}
%{_libdir}/mpich/lib/libboost_graph_parallel-mt.so.%{sonamever}

%endif

%files build
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_datadir}/%{name}-build/

%files jam
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_bindir}/bjam%{version_suffix}
%{_mandir}/man1/bjam%{version_suffix}.1*

%changelog
* Sat Apr 11 2015 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-5
- Included -math subpackage into umbrella package
- Added missing /sbin/ldconfig for -math subpackage

* Thu Mar 21 2013 Radu Greab <radu@yx.ro> - 1.48.0-4
- Add boost version to the files from the build and jam subpackages

* Wed Mar 20 2013 Radu Greab <radu@yx.ro> - 1.48.0-3
- Set noarch for package boost148-build only on supported systems,
  otherwise the debuginfo package is not built

* Tue Mar 19 2013 Radu Greab <radu@yx.ro> - 1.48.0-2
- Really remove the .cmake files from the build root
- The devel libraries are in versioned directories
- boost148-devel: does not require cmake
- boost148-devel: require boost148, not boost

* Wed Mar 13 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-1
- Transformed boost-1.48.0-14 into boost148-1.48.0-1 (#921134)
