Name:           tclap
Summary:        Templatized Command Line Argument Parser
Version:        1.2.0
Release:        2%{?dist}
License:        MIT
URL:            http://tclap.sourceforge.net/
Source0:        http://downloads.sourceforge.net/tclap/tclap-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  doxygen graphviz pkgconfig

%description
%{summary}

%package devel
Summary:        Templatized Command Line Argument Parser
Group:          Development/Libraries
Provides:       %{name} = %{version}-%{release}

%description devel
This is a simple C++ library that facilitates parsing command line
arguments in a type independent manner.  It doesn't conform exactly
to either the GNU or POSIX standards, although it is close.


%package doc
Summary:        API Documentation for tclap
Group:          Documentation
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description doc
API documentation for the Templatized Command Line Argument Parser library


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%check
make check

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}


%files devel
%defattr(-,root,root,-)
%{_includedir}/tclap
%{_libdir}/pkgconfig/tclap.pc
%doc AUTHORS COPYING README

%files doc
%defattr(-,root,root,-)
%{_defaultdocdir}/tclap

%changelog
* Mon Jul 04 2011 Bruno Postle 1.2.0-2
- create -devel package without a base package

* Tue Mar 08 2011 Bruno Postle 1.2.0-1
- initial fedora package

