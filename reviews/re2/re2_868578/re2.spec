#
Name:           re2
Version:        20130115
Release:        1%{?dist}

Summary:        C++ fast alternative to backtracking RE engines

Group:          System Environment/Libraries 
License:        BSD
URL:            http://code.google.com/p/%{name}/
Source0:        http://re2.googlecode.com/files/%{name}-%{version}.tgz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
RE2 is a fast, safe, thread-friendly alternative to backtracking
regular expression engines like those used in PCRE, Perl, and
Python. It is a C++ library.

Backtracking engines are typically full of features and convenient
syntactic sugar but can be forced into taking exponential amounts of
time on even small inputs. RE2 uses automata theory to guarantee that
regular expression searches run in time linear in the size of the
input. RE2 implements memory limits, so that searches can be
constrained to a fixed amount of memory. RE2 is engineered to use a
small fixed C++ stack footprint no matter what inputs or regular
expressions it must process; thus RE2 is useful in multi-threaded
environments where thread stacks cannot grow arbitrarily large.

On large inputs, RE2 is often much faster than backtracking engines;
its use of automata theory lets it apply additional optimization that
the others cannot.

RE2 supports sub-match extraction, but not back references.

If you absolutely need backreferences and generalized assertions, then
RE2 is not for you, but you might be interested in irregexp, Google
Chrome's regular expression engine.

%package        devel
Summary:        Header files, libraries and development helper tools for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains the header files, shared libraries and
development helper tools for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.


%prep
%setup -q -n %{name}

%build
CXXFLAGS="${CXXFLAGS:-%optflags}"; export CXXFLAGS
LDFLAGS="${LDFLAGS:-%__global_ldflags}"; export LDFLAGS
make %{?_smp_mflags} CXXFLAGS='%optflags' LDFLAGS='%__global_ldflags' includedir=%{_includedir} libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT includedir=%{_includedir} libdir=%{_libdir}

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
%doc LICENSE README
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so


%changelog
* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 20130115-1
- The download source comes now directly from the project.

* Thu Oct 25 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.0.0-2
- Took into account review request (#868578) feedback.

* Sat Oct 20 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.0.0-1
- RPM release for Fedora 18

