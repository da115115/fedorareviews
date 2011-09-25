Name:           deheader
Version:        0.6
Release:        1%{?dist}
Summary:        Find (optionally remove) unneeded includes in C or C++ source files

Group:          Development/Tools
License:        BSD
URL:            http://www.catb.org/~esr/deheader

Source0:        http://www.catb.org/~esr/deheader/%{name}-%{version}.tar.gz

Requires:       python2
BuildArch:      noarch


%description
deheader analyzes C and C++ files to determine which header inclusions can be
removed while still allowing them to compile.  This may result in substantial
improvements in compilation time, especially on large C++ projects; it also
sometimes exposes dependencies and cohesions of which developers were unaware.


%prep
%setup -q


%install
install -pD deheader %{buildroot}%{_bindir}/deheader
install -pD -m 644 deheader.1 %{buildroot}%{_mandir}/man1/deheader.1


%files
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Sat Feb 19 2011 Patryk Obara <dreamer.tan at gmail.com> - 0.6-1
- First release

