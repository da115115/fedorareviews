Name:           extracc
Version:        0.5.0
Release:        2%{?dist}

Summary:        CruiseControlisator for C++ library (CppUnit) unit tests

Group:          System Environment/Libraries 
License:        LGPLv2+
URL:            http://sourceforge.net/projects/%{name}/
Source0:        http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.bz2
%{?el5:BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)}

BuildRequires:  cppunit-devel

%description
That project aims at providing tools and code to be used in C++ projects
relying on CppUnit (http://apps.sourceforge.net/mediawiki/cppunit) and/or
Trac (http://trac.edgewall.org), to allow for easy integration with
CruiseControl (http://cruisecontrol.sourceforge.net).

%package        devel
Summary:        Header files, libraries and development documentation for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains the header files, static libraries and
development documentation for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.


%prep
%setup -q
# Fix some permissions and formats
rm -f INSTALL
chmod -x AUTHORS ChangeLog COPYING NEWS README
find . -type f -name '*.[hc]pp' -exec chmod 644 {} \;

%build
%configure --disable-static
make %{?_smp_mflags}

%install
# On Fedora, the BuildRoot is automatically cleaned. Which is not the case for
# RedHat. See: https://fedoraproject.org/wiki/Packaging/Guidelines#BuildRoot_tag
%if 0%{?rhel}
rm -rf $RPM_BUILD_ROOT
%endif
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove unpackaged files from the buildroot
rm -rf $RPM_BUILD_ROOT%{_includedir}/%{name}
rm -f $RPM_BUILD_ROOT%{_libdir}/libextracppunit.la

# Set the executable bit of the Python scripts
chmod +x $RPM_BUILD_ROOT%{_datadir}/%{name}/tools/*.py

# The clean section is no longer needed.
# See: https://fedoraproject.org/wiki/Packaging/Guidelines#.25clean
%if 0%{?fedora} < 13
%clean
rm -rf $RPM_BUILD_ROOT
%endif


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libextracppunit.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/extracppunit/
%{_bindir}/%{name}-config
%{_libdir}/libextracppunit.so
%{_datadir}/aclocal/%{name}.m4
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/extracppunit/
%{_datadir}/%{name}/build/
%{_datadir}/%{name}/tools/
%{_mandir}/man1/%{name}-config.1.*


%changelog
* Mon Aug 21 2010 Christophe Lacombe <clacombe@amadeus.com> 0.5.0-2
- Integrated comments from the package review (#616881)

* Mon Jun 10 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.5.0-1
- Upstream integration

* Mon Jun 10 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.4.0-1
- Upstream integration

* Mon Sep 07 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.3.0-1
- Upstream integration

* Mon Sep 07 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.2.0-1
- RPM release for Fedora 11

