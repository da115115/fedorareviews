# Documentation package/directory
%global mydocs __tmp_docdir

# Build -python subpackage
%bcond_without python
%if %{with python}
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
# See also http://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Private_Libraries
%global _privatelibs libpy%{name}[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$
%endif

#
Name:           opentrep
Version:        0.6.5
Release:        1%{?dist}

Summary:        C++ library providing a clean API for parsing travel-focused requests

Group:          System Environment/Libraries
# The entire source code is LGPLv2+ except opentrep/basic/float_utils_google.hpp,
# which is BSD
License:        LGPLv2+ and BSD
URL:            http://%{name}.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:       %{name}-data = %{version}-%{release}
BuildRequires:  cmake, xapian-core-devel, readline-devel
BuildRequires:  python2-devel
BuildRequires:  sqlite-devel, mariadb-devel, soci-sqlite3-devel, soci-mysql-devel
BuildRequires:  boost-devel, libicu-devel, protobuf-devel, protobuf-compiler

%description
%{name} aims at providing a clean API, and the corresponding C++
implementation, for parsing travel-focused requests.
It powers the http://search-travel.org Web site.

%{name} uses Xapian (http://www.xapian.org) for the Information Retrieval part,
on freely available travel-related data (e.g., country names and codes,
city names and codes, airline names and codes, etc.), mainly to be found
in the OpenTravelData project (http://github.com/opentraveldata/optd):
http://github.com/opentraveldata/opentraveldata/tree/trunk/opentraveldata

%{name} exposes a simple, clean and object-oriented, API. For instance,
the OPENTREP::interpretTravelRequest() method takes, as input, a string
containing the travel request, and yields, as output, the list of the
recognized terms as well as their corresponding types.
As an example, the travel request
'Washington DC Beijing Monday a/r +AA -UA 1 week 2 adults 1 dog' would give
the following list:
 * Origin airport: Washington, DC, USA
 * Destination airport: Beijing, China
 * Date of travel: next Monday
 * Date of return: 1 week after next Monday
 * Preferred airline: American Airlines; non-preferred airline: United Airlines
 * Number of travelers: 2 adults and a dog

The output can then be used by other systems, for instance to book the
corresponding travel or to visualize it on a map and calendar and to
share it with others.

%{name} makes an extensive use of existing open-source libraries for
increased functionality, speed and accuracy. In particular the
Boost (C++ Standard Extensions: http://www.boost.org) and
SOCI (http://soci.sourceforge.net) libraries are used.

Note that %{name} currently only recognizes points of reference (POR),
as to be found in the following file:
http://github.com/opentraveldata/opentraveldata/blob/trunk/opentraveldata/optd_por_public.csv
A good complementary tool is GeoBase (http://opentraveldata.github.io/geobases),
a Python-based software able to access to any travel-related data source.


%package        devel
Summary:        Header files, libraries and development helper tools for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 5
Requires:       pkgconfig
%endif

%description    devel
This package contains the header files, shared libraries and
development helper tools for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.

%package        data
Summary:        Referential data for the %{name} library
Group:          Applications/Databases
License:        CC-BY-SA
%if 0%{?fedora} || 0%{?rhel} > 5
BuildArch:      noarch
%endif

%description    data
OpenTREP uses Xapian (http://www.xapian.org) for the Information Retrieval
part, on freely available travel-related data (e.g., country names and codes,
city names and codes, airline names and codes, etc.), mainly to be found in
the OpenTravelData project (http://github.com/opentraveldata/opentraveldata):
http://github.com/opentraveldata/opentraveldata/tree/trunk/opentraveldata


%package        doc
Summary:        HTML documentation for the %{name} library
Group:          Documentation
%if 0%{?fedora} || 0%{?rhel} > 5
BuildArch:      noarch
%endif
BuildRequires:  tex(latex), tex(sectsty.sty), tex(tocloft.sty), tex(xtab.sty)
BuildRequires:  texlive-collection-langcyrillic, texlive-cyrillic
BuildRequires:  doxygen, ghostscript

%description    doc
This package contains HTML pages for %{name}. All that documentation
is generated thanks to Doxygen (http://doxygen.org). The content is
the same as what can be browsed online (http://opentrep.sourceforge.net).
Note that the PDF form of the reference manual is mainly available online
(http://opentrep.sourceforge.net/refman.pdf), as the one present in that
package is usually corrupted: it depends on the building conditions,
and it is therefore not reliable.

%if %{with python}
%package        python
Summary:        Python bindings for %{name}
Group:          Development/Languages
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       protobuf-python

%description python
This package contains Python libraries for %{name}
%endif


%prep
%setup -q


%build
%cmake .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# From rpm version > 4.9.1, it may no longer be necessary to move the
# documentation out of the docdir path, as the %%doc macro no longer
# deletes the full directory before installing files into it.
mkdir -p %{mydocs}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/html %{mydocs}
rm -f %{mydocs}/html/installdox

# Remove additional documentation files (those files are already available
# in the project top directory)
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}/{NEWS,README,AUTHORS}

%if %{with python}
# (Pure) Python OpenTREP executable
install -d $RPM_BUILD_ROOT%{python2_sitearch}/libpy%{name}
install -pm 0755 $RPM_BUILD_ROOT%{_bindir}/py%{name} $RPM_BUILD_ROOT%{python2_sitearch}/libpy%{name}/
rm -f $RPM_BUILD_ROOT%{_bindir}/py%{name}
# (Pure) Python Protobuf module
install -pm 0644 $RPM_BUILD_ROOT%{_libdir}/python/%{name}/*.py* $RPM_BUILD_ROOT%{python2_sitearch}/libpy%{name}/
rm -f $RPM_BUILD_ROOT%{_libdir}/python/%{name}/*.py*
# (ELF) Binary Python module (library)
mv $RPM_BUILD_ROOT%{_libdir}/python/%{name}/libpy%{name}.so* $RPM_BUILD_ROOT%{python2_sitearch}/libpy%{name}/
%endif


%check
#ctest

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/%{name}-indexer
%{_bindir}/%{name}-searcher
%{_bindir}/%{name}-dbmgr
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}-indexer.1.*
%{_mandir}/man1/%{name}-searcher.1.*
%{_mandir}/man1/%{name}-dbmgr.1.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/data
%dir %{_datadir}/%{name}/data/por
%{_datadir}/%{name}/data/por/create_trep_user_and_db.sql
%{_datadir}/%{name}/data/por/create_trep_tables_sqlite3.sql
%{_datadir}/%{name}/data/por/create_trep_tables_mysql.sql
%{_datadir}/%{name}/data/por/optd_por_public_4_test.csv
%{_datadir}/%{name}/data/por/test_optd_por_public.csv
%{_datadir}/%{name}/data/por/test_optd_por_public_schema.sql
%{_datadir}/%{name}/data/por/test_world_schedule.csv

%files devel
%{_includedir}/%{name}
%{_bindir}/%{name}-config
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/aclocal/%{name}.m4
%{_datadir}/%{name}/CMake
%{_mandir}/man1/%{name}-config.1.*
%{_mandir}/man3/%{name}-library.3.*

%files data
%doc %{_datadir}/%{name}/data/por/README.md
%{_datadir}/%{name}/data/por/optd_por_public.csv

%files doc
%doc %{mydocs}/html
%doc COPYING

%if %{with python}
%files python
%{python2_sitearch}/libpy%{name}/
%{_mandir}/man1/py%{name}.1.*
%endif


%changelog
* Sun Apr 19 2015 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.6.5-1
- Upstream update

* Sun Apr 13 2014 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.6.1-1
- Upstream update
- The Python-related files are now packaged within a dedicated sub-package

* Sun Feb 02 2014 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.6.0-1
- Upstream update

* Mon Aug 12 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.5.3-3
- Took into account a part of the feedbacks from review request (BZ#866265):
  opentrep-config now supports multilib (32 and 64bit versions).
- Upstream update

* Mon Jul 29 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.5.3-2
- Fixed the docdir issue, following the F20 System Wide Change
- Rebuild for boost 1.54.0

* Sun Mar 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.5.3-1
- Upstream update

* Sun Feb 17 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.5.2-1
- Upstream update

* Thu Oct 25 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.5.0-2
- Took into account review request #866265 feedback

* Sun Oct 14 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.5.0-1
- Upstream update

* Tue Nov 01 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.4.0-1
- The build system is now based on CMake (instead of the GNU Autotools)

* Sun Mar 29 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.3.0-1
- Now relies on the new SOCI RPM

* Sun Mar 22 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.2.0-1
- RPM release for Fedora 10

