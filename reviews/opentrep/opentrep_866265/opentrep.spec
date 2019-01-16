#
%global mydocs __tmp_docdir

# Build -python subpackage
%bcond_without python

# See also http://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Private_Libraries
%if %{with python}
%global _privatelibs libpy%{name}[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$
%endif

#
Name:           opentrep
Version:        0.07.1
Release:        1%{?dist}

Summary:        C++ library providing a clean API for parsing travel-focused requests

# The entire source code is LGPLv2+ except opentrep/basic/float_utils_google.hpp,
# which is BSD
License:        LGPLv2+ and BSD
URL:            http://github.com/trep/%{name}
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

Requires:       %{name}-data = %{version}-%{release}

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  python3-devel
BuildRequires:  boost-devel
BuildRequires:  boost-python3-devel
BuildRequires:  readline-devel
BuildRequires:  soci-mysql-devel
BuildRequires:  soci-sqlite3-devel
BuildRequires:  xapian-core-devel
BuildRequires:  sqlite-devel
BuildRequires:  mariadb-devel
BuildRequires:  libicu-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-compiler

%description
%{name} aims at providing a clean API, and the corresponding C++
implementation, for parsing travel-focused requests.
It powers the http://search-travel.org Web site.

%{name} uses Xapian (http://www.xapian.org) for the Information Retrieval part,
on freely available travel-related data (e.g., country names and codes,
city names and codes, airline names and codes, etc.), mainly to be found in
the OpenTravelData project (http://github.com/opentraveldata/opentraveldata):
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
as to be found in the following file: http://bit.ly/1DXIjWE
A good complementary tool is GeoBase (http://opentraveldata.github.io/geobases),
a Python-based software able to access to any travel-related data source.


%package        devel
Summary:        Header files, libraries and development helper tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains the header files, shared libraries and
development helper tools for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.

%package        data
Summary:        Referential data for the %{name} library
Group:          Applications/Databases
License:        CC-BY-SA
BuildArch:      noarch

%description    data
OpenTREP uses Xapian (http://www.xapian.org) for the Information Retrieval
part, on freely available travel-related data (e.g., country names and codes,
city names and codes, airline names and codes, etc.), mainly to be found in
the OpenTravelData project (http://github.com/opentraveldata/opentraveldata):
http://github.com/opentraveldata/opentraveldata/tree/trunk/opentraveldata


%package        doc
Summary:        HTML documentation for the %{name} library
Group:          Documentation
BuildArch:      noarch
BuildRequires:  tex(latex), tex(sectsty.sty), tex(tocloft.sty), tex(xtab.sty)
BuildRequires:  texlive-collection-langcyrillic, texlive-cyrillic
BuildRequires:  doxygen
BuildRequires:  ghostscript

%description    doc
This package contains HTML pages for %{name}. All that documentation
is generated thanks to Doxygen (http://doxygen.org). The content is
the same as what can be browsed online (http://opentrep.sourceforge.net).
Note that the PDF form of the reference manual is mainly available online
(http://opentrep.sourceforge.net/refman.pdf), as the one present in that
package is usually corrupted: it depends on the building conditions,
and it is therefore not reliable.

%if %{with python}
%package        -n python3-%{name}
Summary:        Python bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-protobuf
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
This package contains Python libraries for %{name}
%endif


%prep
%setup -q -n %{name}-%{name}-%{version}


%build
%cmake .
%make_build

%install
%make_install

# From rpm version > 4.9.1, it may no longer be necessary to move the
# documentation out of the docdir path, as the %%doc macro no longer
# deletes the full directory before installing files into it.
mkdir -p %{mydocs}
mv %{buildroot}%{_docdir}/%{name}/html %{mydocs}
rm -f %{mydocs}/html/installdox

# Remove additional documentation files (those files are already available
# in the project top directory)
rm -f %{buildroot}%{_docdir}/%{name}/{NEWS,README.md,AUTHORS}

%if %{with python}
# (Pure) Python OpenTREP executable
install -d %{buildroot}%{python3_sitearch}/py%{name}
install -pm 0755 %{buildroot}%{_bindir}/py%{name} %{buildroot}%{python3_sitearch}/py%{name}/
rm -f %{buildroot}%{_bindir}/py%{name}
chmod a-x %{buildroot}%{python3_sitearch}/py%{name}/Travel_pb2.py
%endif


#check
#ctest


%files
%doc AUTHORS ChangeLog COPYING NEWS README.md
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
%files -n python3-%{name}
%{python3_sitearch}/py%{name}/
%{_mandir}/man1/py%{name}.1.*
%endif


%changelog
* Wed Jan 16 2019 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.07.1-1
- Upstream update

* Tue Oct 16 2018 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.07.0-1
- Upstream update

* Sun Apr 19 2015 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.6.6-1
- Upstream update

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

