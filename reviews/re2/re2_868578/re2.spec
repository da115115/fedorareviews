Name:           re2
Version:        20130115
Release:        2%{?dist}

Summary:        C++ fast alternative to backtracking RE engines

Group:          System Environment/Libraries
License:        BSD
URL:            http://code.google.com/p/%{name}/
Source0:        http://re2.googlecode.com/files/%{name}-%{version}.tgz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
RE2 is a C++ library providing a fast, safe, thread-friendly alternative to
backtracking regular expression engines like those used in PCRE, Perl, and
Python.

Backtracking engines are typically full of features and convenient syntactic
sugar but can be forced into taking exponential amounts of time on even small
inputs.

In contrast, RE2 uses automata theory to guarantee that regular expression
searches run in time linear in the size of the input, at the expense of some
missing features (e.g back references and generalized assertions).

%package        devel
Summary:        C++ header files and library symbolic links for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains the C++ header files and symbolic links to the shared
libraries for %{name}. If you would like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n %{name}

%build
# The -pthread flag issue has been submitted upstream:
# http://groups.google.com/forum/?fromgroups=#!topic/re2-dev/bkUDtO5l6Lo
CXXFLAGS="${CXXFLAGS:-%optflags}"
LDFLAGS="${LDFLAGS:-%__global_ldflags} -pthread"
make %{?_smp_mflags} CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" includedir=%{_includedir} libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL="install -p" DESTDIR=$RPM_BUILD_ROOT includedir=%{_includedir} libdir=%{_libdir}

# Suppress the static library
find $RPM_BUILD_ROOT -name 'lib%{name}.a' -exec rm -f {} \;

%check
make %{?_smp_mflags} test

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS CONTRIBUTORS LICENSE README
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so


%changelog
* Sun Feb 17 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 20130115-2
- Took into account the feedback from review request (#868578).

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 20130115-1
- The download source comes now directly from the project.

* Thu Oct 25 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.0.0-2
- Took into account review request (#868578) feedback.

* Sat Oct 20 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.0.0-1
- RPM release for Fedora 18

