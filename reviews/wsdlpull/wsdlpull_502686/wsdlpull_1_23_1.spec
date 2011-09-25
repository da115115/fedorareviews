##
# Original RPM Specification file from the Dries repository:
#   http://svn.rpmforge.net/svn/trunk/rpms/wsdlpull/wsdlpull.spec
# Original author: Dries Verachtert <dries@ulyssis.org>
##
#
%define mydocs __tmp_docdir
#
Summary: C++ Web Services client library
Name: wsdlpull
Version: 1.23
Release: 1%{?dist}
License: LGPLv2
Group: System Environment/Libraries
URL: http://%{name}.sourceforge.net
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# That patch will be submitted upstream
Patch0: wsdlpull-%{version}-1-fix-gcc43-compatibility.patch
# That patch will be submitted upstream
Patch1: wsdlpull-%{version}-1-fix-gnu-autotools-compatibility.patch
#BuildRequires:

%description
wsdlpull is a C++ web services client library. It includes a WSDL
Parser, a XSD Schema Parser and Validator and XML Parser and serializer
and an API and command line tool for dynamic WSDL inspection and
invocation.

wsdlpull comes with a generic web service client.Using wsdlpull's /wsdl/
tool you can invoke most web services from command line without writing
any code.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package doc
Summary: HTML documentation for the %{name} library
Group: Documentation
%if 0%{?fedora} >= 10
BuildArch: noarch
BuildRequires: texlive-latex
%endif
%if 0%{?fedora} < 10
BuildRequires: tetex-latex
%endif
%{?el5:BuildRequires: tetex-latex}
BuildRequires: doxygen
#BuildRequires: graphviz
#BuildRequires: ghostscript

%description doc
This package contains the documentation in the HTML format of the %{name}
library. The documentation is the same as at the %{name} web page.

%prep
%setup -q

# Apply the g++ 4.3 compatibility patch
%patch0 -p1

# Remove any CVS sub-directory (they should not be delivered with the tar-ball)
find . -name 'CVS' -print | xargs rm -rf

# Remove any a.out binary (they should not be delivered with the tar-ball)
find . -name 'a.out' -print | xargs rm -f

# Remove the generated HTML documentation (it should not be delivered
# with the tar-ball, as it is generated)
if [ -d docs/html ]; then
  rm -rf docs/html
fi

# Adapt a little bit the structure, so as to be more compliant with
# GNU Autotools
mkdir config
mv config.guess config.sub depcomp install-sh ltmain.sh missing config
mv config.h.in src

# Rename the standard documentation files
mv AUTHORS.txt AUTHORS
mv CHANGES.txt CHANGES
mv COPYING.txt COPYING
mv README.txt README

# Apply the GNU Autotools compatibility patch
%patch1 -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#%%find_lang %{name}
# remove unpackaged files from the buildroot
#rm -f $RPM_BUILD_ROOT%{_includedir}/%{name}/config.h
#rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
# chmod 644 doc/html/installdox doc/html/*.png doc/html/*.ico
rm -rf %{mydocs} && mkdir -p %{mydocs}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{mydocs}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES COPYING README
%{_bindir}/schema
%{_bindir}/wsdl
%{_libdir}/lib*.so.*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%doc AUTHORS CHANGES COPYING README
%{_includedir}/schemaparser
%{_includedir}/wsdlparser
%{_includedir}/xmlpull
%{_libdir}/lib*.so

%files doc
%defattr(-,root,root,-)
%doc %{mydocs}/html
%doc AUTHORS CHANGES COPYING README


%changelog
* Tue Jun 26 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 1.23-1
- Initial package, thanks to Dries Verachtert <dries@ulyssis.org>
