#
%define verSuf	1
#
Name:		newmat
Version:	11
Release:	1%{?dist}
Summary:	C++ matrix library

Group:		System Environment/Libraries
License:	Public Domain
URL:		http://www.robertnz.net/nm_intro.htm
Source0:	http://www.robertnz.net/ftp/%{name}%{version}.tar.gz
Patch0:		%{name}-%{version}-fix-exit-issue.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
%{name} is a C++ library is intended for scientists and engineers who need to 
manipulate a variety of types of matrices using standard matrix 
operations. Emphasis is on the kind of operations needed in statistical
calculations such as least squares, linear equation solve and 
eigenvalues.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -c %{name}-%{version} -n %{name}-%{version}
%patch0 -p1


%build
echo 'lib%{name}.so.%{version}.%{verSuf}:   $(%{name}_lobj)' >> nm_gnu.mak
echo '	$(CXX) $(LDFLAGS) -shared -Wl,-soname,lib%{name}.so.%{version} -o $@ $^' >> nm_gnu.mak 
make -f nm_gnu.mak %{?_smp_mflags} CXXFLAGS="%{optflags} -fPIC" lib%{name}.so.%{version}.%{verSuf}

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_libdir}
install -p -D -m 0755 lib%{name}.so.%{version}.%{verSuf} %{buildroot}%{_libdir}/

cd  %{buildroot}%{_libdir}
ln -s lib%{name}.so.%{version}.%{verSuf} lib%{name}.so.%{version}
ln -s lib%{name}.so.%{version}.%{verSuf} lib%{name}.so
cd -

install -d %{buildroot}%{_includedir}/%{name}/
install -m 0644 -p *.h %{buildroot}%{_includedir}/%{name}/

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc nm%{version}.htm readme.txt
%{_libdir}/lib%{name}.so.*

%files	devel
%defattr(-,root,root,-)
%doc nm%{version}.htm readme.txt
%dir %{_includedir}/%{name}/
%{_includedir}/%{name}/*.h
%{_libdir}/lib%{name}.so

%changelog
* Sat Jun 13 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 11-1
- Integrated the new upstream version (11)

* Fri Feb 06 2009 Pascal < pascal22p at parois.net > - 10D-2
- Correction of soname

* Sat Jan 10 2009 Pascal < pascal22p at parois.net > - 10D-1
- Fisrt spec file

