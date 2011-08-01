#
##
# Default values are --with mysql --with postgresql --without oracle 
# Note that, for Oracle, when enabled, the following options should
# also be given:
# --with-oracle-include=/opt/oracle/app/oracle/product/11.1.0/db_1/rdbms/public
# --with-oracle-lib=/opt/oracle/app/oracle/product/11.1.0/db_1/lib
# If the macros are defined, redefine them with the correct compilation flags.
%bcond_without mysql
%bcond_without postgresql
%bcond_with oracle

%define _default_oracle_dir /opt/oracle/app/oracle/product/11.1.0/db_1
%{!?_with_oracle_incdir: %define _with_oracle_incdir --with-oracle-include=%{_default_oracle_dir}/rdbms/public}
%{!?_with_oracle_libdir: %define _with_oracle_libdir --with-oracle-lib=%{_default_oracle_dir}/lib}
#
##
#
Name:           soci
Version:        3.0.0
Release:        22%{?dist}

Summary:        The database access library for C++ programmers

Group:          System Environment/Libraries
License:        Boost
URL:            http://%{name}.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# This issue has been fixed upstream, e.g., see:
#  http://soci.git.sourceforge.net/git/gitweb.cgi?p=soci/soci;a=commitdiff;h=9e467b5a4ab4cdda6cd801fb76b2d853340dc5d7):
Patch0:         %{name}-%{version}-gcc46-compatibility.patch
# This patch is being submitted upstream. A decision about whether and how
# burying headers) should be taken after the release of version 3.1.0):
Patch1:         %{name}-%{version}-buried-headers.patch
# Just add standard documentation, from upstream documents:
Patch2:         %{name}-%{version}-add-doc.patch
# This patch is temporary, for the 3.0.0 version, as:
#  * it allows to build cleanly with the GNU Autotools;
#  * whereas upstream now uses CMake.
Patch3:         %{name}-%{version}-gnu-autotools-compatibility.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  boost-devel
BuildRequires:  libtool

%description
%{name} is a C++ database access library that provides the
illusion of embedding SQL in regular C++ code, staying entirely within
the C++ standard.


%{?with_mysql:%package        mysql
Summary:        MySQL back-end for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
BuildRequires:  mysql-devel >= 5.0

%description    mysql
This package contains the MySQL back-end for SOCI, i.e.,
dynamic library specific to the MySQL database. If you would like to
use SOCI in your programs with MySQL, you will need to
install %{name}-mysql.}

%{?with_postgresql:%package        postgresql
Summary:        PostGreSQL back-end for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
BuildRequires:  postgresql-devel >= 7.1

%description    postgresql
This package contains the PostGreSQL back-end for SOCI, i.e.,
dynamic library specific to the PostGreSQL database. If you would like
to use SOCI in your programs with PostGreSQL, you will need to
install %{name}-postgresql.}

%{?with_oracle:%package        oracle
Summary:        Oracle back-end for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    oracle
This package contains the Oracle back-end for SOCI, i.e.,
dynamic library specific to the Oracle database. If you would like to
use SOCI in your programs with Oracle, you will need to install
%{name}-oracle.}


%package        devel
Summary:        Header files, libraries and development documentation for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains the header files, dynamic libraries and
development documentation for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.

%{?with_mysql:%package        mysql-devel
Summary:        MySQL back-end for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-mysql = %{version}-%{release}
Requires:       mysql-devel >= 5.0

%description    mysql-devel
This package contains the MySQL back-end for %{name}, i.e., header
files and dynamic libraries specific to the MySQL database. If you
would like to develop programs using %{name} and MySQL, you will need
to install %{name}-mysql.}

%{?with_postgresql:%package        postgresql-devel
Summary:        PostGreSQL back-end for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-postgresql = %{version}-%{release}
Requires:       postgresql-devel >= 7.1

%description    postgresql-devel
This package contains the PostGreSQL back-end for %{name}, i.e., header
files and dynamic libraries specific to the PostGreSQL database. If
you would like to develop programs using %{name} and PostGreSQL, you
will need to install %{name}-postgresql.}

%{?with_oracle:%package        oracle-devel
Summary:        Oracle back-end for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-oracle = %{version}-%{release}

%description    oracle-devel
This package contains the Oracle back-end for %{name}, i.e., header
files and dynamic libraries specific to the Oracle database. If you
would like to develop programs using %{name} and Oracle, you will need
to install %{name}-oracle.}


%package doc
Summary:        HTML documentation for the SOCI library
Group:          Documentation
%if 0%{?fedora} >= 10
BuildArch:      noarch
#BuildRequires:  texlive-latex, texlive-dvips
%endif
#BuildRequires:  tetex-latex, tetex-dvips
#BuildRequires:  doxygen, ghostscript

%description doc
This package contains the documentation in the HTML format of the SOCI
library. The documentation is the same as at the SOCI web page.


%prep
%setup -q

# Apply the g++ 4.6 compatibility patch
%patch0 -p1

# Rename change-log and license file, so that they comply with
# packaging standard
mv CHANGES ChangeLog
mv LICENSE_1_0.txt COPYING
rm -f INSTALL

# Remove MacOSX compatibility building files
rm -f build/unix/._*.tcl
rm -f ._Makefile ._configure
rm -f src/core/._*.h src/core/._*.cpp
rm -f src/backends/postgresql/._*.h
rm -f doc/._*.html

# Rename the source code directory, so that the files (e.g, header
# files) can be exported correctly into {_standard_dir}/%%{name}
mv src %{name}

# Apply the buried headers patch
%patch1 -p1

# Add standard documentation
%patch2 -p1

# Apply the GNU Autotools compatibility patch
%patch3 -p1

# Fix some permissions and formats
find ./doc -type f -perm 755 -exec chmod 644 {} \;
chmod -x AUTHORS ChangeLog COPYING NEWS README
# find . -type f -name '*.[hc]pp' -exec chmod 644 {} \;


%build
%configure --disable-static \
%{?with_mysql:--enable-backend-mysql} \
%{?with_postgresql:--enable-backend-postgresql} \
%{?with_oracle:--enable-backend-oracle %{?_with_oracle_incdir} %{?_with_oracle_libdir}}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
##
#  Remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_includedir}/%{name}/config.h
rm -f $RPM_BUILD_ROOT%{_libdir}/lib%{name}_*.la
##
##
#  Duplicate the header files, so as to keep the compatibility, for
#  developers using the SOCI library, with the non-packaged version of
#  that library.
for header_file in $RPM_BUILD_ROOT%{_includedir}/%{name}/core/*.h; do
  cp ${header_file} $RPM_BUILD_ROOT%{_includedir}/%{name}
done
%{?with_mysql:cp $RPM_BUILD_ROOT%{_includedir}/%{name}/backends/mysql/soci-mysql.h $RPM_BUILD_ROOT%{_includedir}/%{name}}
%{?with_postgresql:cp $RPM_BUILD_ROOT%{_includedir}/%{name}/backends/postgresql/soci-postgresql.h $RPM_BUILD_ROOT%{_includedir}/%{name}}
%{?with_oracle:cp $RPM_BUILD_ROOT%{_includedir}/%{name}/backends/oracle/soci-oracle.h $RPM_BUILD_ROOT%{_includedir}/%{name}}


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%{?with_mysql:%post mysql -p /sbin/ldconfig

%postun mysql -p /sbin/ldconfig}

%{?with_postgresql:%post postgresql -p /sbin/ldconfig

%postun postgresql -p /sbin/ldconfig}

%{?with_oracle:%post oracle -p /sbin/ldconfig

%postun oracle -p /sbin/ldconfig}



%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib%{name}_core.so.*

%{?with_mysql:%files mysql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib%{name}_mysql.so.*}

%{?with_postgresql:%files postgresql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib%{name}_postgresql.so.*}

%{?with_oracle:%files oracle
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib%{name}_oracle.so.*}


%files devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}/core
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/core/*.h
%{_includedir}/%{name}/core/test
%{_bindir}/%{name}-config
%{_libdir}/lib%{name}_core.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/aclocal/%{name}.m4
%{_mandir}/man1/%{name}-config.1.*

%{?with_mysql:%files mysql-devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/backends/mysql
%{_libdir}/lib%{name}_mysql.so}

%{?with_postgresql:%files postgresql-devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/backends/postgresql
%{_libdir}/lib%{name}_postgresql.so}

%{?with_oracle:%files oracle-devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/backends/oracle
%{_libdir}/lib%{name}_oracle.so}


%files doc
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README doc


%changelog
* Sun Jul 03 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.0.0-22
- Now links with the multi-threaded versions of the Boost libraries

* Mon Apr 25 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.0.0-21
- Rebuild for Boost-1.46.1-2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-19
- Fixed a compilation error with g++ 4.6 on default constructor definition
- Split the big patch into smaller pieces

* Tue Sep 07 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-18
- Fixed bug #631175 (https://bugzilla.redhat.com/show_bug.cgi?id=631175)

* Sat Jan 23 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-16
- Added a missing cstring header include for g++-4.4 compatibility

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 3.0.0-15
- Rebuild for Boost soname bump

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 09 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-13
- Introduced distinct dependencies for different distributions

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-12
- Removed the dependency on the version of Boost, and on CPPUnit

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-11
- Removed the dependency on Latex for documentation delivery

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-10
- Burried the Boost Fusion header include for core/test/common-tests.h

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-9
- Added a missing cstdio header include for g++-4.4 compatibility

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-8
- Added missing cstdio header includes for g++-4.4 compatibility

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-7
- Added a missing cstdio header include for g++-4.4 compatibility

* Sat May 02 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-6
- Removed the unused build conditionals

* Tue Apr 28 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-5
- Simplified the conditional build rules within the RPM specification file

* Sat Apr 18 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-4
- Fixed an issue about OPTFLAGS compilation

* Tue Apr 14 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-3
- Restarted from pristine version 3.0.0 of upstream (SOCI) project

* Sat Apr  4 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-2
- Specific RPM for each backend

* Fri Mar 27 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-1
- First RPM release

