Name:           openturns 
Version:        0.15
Release:        1%{?dist}
Summary:        Uncertainty treatment library
Group:          System Environment/Libraries
License:        LGPLv2 
URL:            http://www.openturns.org
Source0:        http://downloads.sourceforge.net/openturns/openturns/openturns-0.15.tar.bz2
Patch0:         %{name}-%{version}-obs.patch
Patch1:         %{name}-%{version}-leastsquaresstrategy_constructor.patch
Patch2:         %{name}-%{version}-compute_cdf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  gcc-c++, bison, flex, automake, libtool, autoconf, doxygen
BuildRequires:  libxml2-devel
BuildRequires:  tbb-devel
BuildRequires:  R-rot
%if 0%{?suse_version}
BuildRequires:  lapack
BuildRequires:  gcc-fortran
BuildRequires:  -post-build-checks
BuildRequires:  fdupes
%else
BuildRequires:  lapack-devel
BuildRequires:  gcc-gfortran
%endif
%if 0%{?rhel_version} || 0%{?centos_version}
BuildRequires:  blas-devel
%endif
%if 0%{?fedora} || 0%{?suse_version} || 0%{?mdkversion}
BuildRequires:  graphviz
%endif
BuildRequires:  python-devel
BuildRequires:  swig &gt;= 1.3.35
%if 0%{?fedora}
BuildRequires:  PyQt4
# choices: atlas / atlas-sse2
BuildRequires:  atlas
BuildRequires:  rpy
%endif
%if 0%{?fedora} &gt;= 15
# choices: sane-backends-libs / sane-backends-libs-gphoto2
BuildRequires:  sane-backends-libs
%endif
%if 0%{?suse_version} || 0%{?mdkversion}
BuildRequires:  python-qt4
%endif
%if 0%{?suse_version}
BuildRequires:  python-rpy2
%endif
%if 0%{?fedora}
BuildRequires:  numpy
%else
BuildRequires:  python-numpy
%endif
Requires:       lib%{name}0

%description
Open TURNS is a scientific C++ library including an internal data model
and algorithms dedicated to the treatment of uncertainties.

%package -n lib%{name}0
Summary:        Uncertainty treatment library
Group:          System Environment/Libraries
%if 0%{?mdkversion}
%ifarch x86_64
Requires:       lib64lapack3
%else
Requires:       liblapack3
%endif
%else
Requires:       lapack
%endif
Requires:       tbb
Requires:       R-rot

%description -n lib%{name}0
Open TURNS is a scientific C++ library including an internal data model
and algorithms dedicated to the treatment of uncertainties.
This package contains the shared library of Open TURNS.

%package devel
Summary:        Open TURNS development files
Group:          Development/Libraries/C and C++
Requires:       lib%{name}0 = %{version}
Requires:       libxml2-devel
Requires:       tbb-devel
%if 0%{?suse_version}
%else
Requires:       lapack-devel
%endif
%if 0%{?rhel_version} || 0%{?centos_version}
BuildRequires:  blas-devel
%endif

%description devel
Development files for OpenTURNS uncertainty library

%package examples
Summary:        Open TURNS examples
Group:          Productivity/Scientific/Math
Requires:       python-%{name}

%description examples
OpenTURNS python examples

%package validation
Summary:        Open TURNS validation files
Group:          Productivity/Scientific/Math
Requires:       lib%{name}0

%description validation
OpenTURNS validation text files

%package -n python-%{name}
Summary:        Uncertainty treatment library
Group:          Productivity/Scientific/Math
Requires:       lib%{name}0
%if 0%{?suse_version}
Requires:       python-base
%else
Requires:       python
%endif
%if 0%{?fedora}
Requires:       PyQt4
Requires:       atlas
Requires:       rpy
%endif
%if 0%{?suse_version} || 0%{?mdkversion}
Requires:       python-qt4
%endif
%if 0%{?suse_version}
Requires:       python-rpy2
%endif

%description -n python-%{name}
Python textual interface to OpenTURNS uncertainty library

%package -n python-%{name}-devel
Summary:        Uncertainty treatment library
Group:          Productivity/Scientific/Math
Requires:       python-%{name} = %{version}
Requires:       %{name}-devel = %{version}
Requires:       python-devel

%description -n python-%{name}-devel
Python textual interface to OpenTURNS uncertainty library development

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0

%build
%configure --disable-static --without-tbb
%if 0%{?mdkversion}
  grep -lr &quot;\\-Wl,\\-\\-no\\-undefined&quot; . | xargs sed -i 's/-Wl,--no-undefined//g'
  grep -lr &quot;\\-no\\-undefined&quot; . | xargs sed -i 's/-no-undefined/-v/g'
%endif
%{__make} %{?_smp_mflags} -C lib
%{__make}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/%{name}/*.la
rm %{buildroot}%{_libdir}/%{name}/wrappers/*.la
rm %{buildroot}%{python_sitearch}/%{name}/*.la
rm %{buildroot}%{_datadir}/%{name}/WrapperTemplates/*/NEWS
rm %{buildroot}%{_datadir}/%{name}/WrapperTemplates/*/INSTALL
chmod a+x %{buildroot}%{_datadir}/%{name}/WrapperTemplates/*/bootstrap
chmod a+x %{buildroot}%{_datadir}/%{name}/WrapperTemplates/*/customize
rm -r %{buildroot}%{_datadir}/%{name}/doc
cd %{buildroot}%{_datadir}/%{name}/examples
ls | grep -v .cxx$ |grep -v .py$ | xargs rm -rf
chmod a+x *.py
%if 0%{?suse_version}
  %fdupes %{buildroot}
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir}/%{name} %{__make} check
LD_LIBRARY_PATH=%{buildroot}%{_libdir}/%{name} PYTHONPATH=%{buildroot}%{python_sitearch} %{__python} -c &quot;import openturns as ot; u=ot.Normal(); print(u)&quot;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README

%files -n lib%{name}0
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/%{name}.conf
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so.*
%dir %{_datadir}/%{name}
%dir %{_libdir}/%{name}/wrappers
%{_libdir}/%{name}/wrappers/wrapper*.dtd
%{_libdir}/%{name}/wrappers/generic.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/%{name}/*.so
%{_bindir}/%{name}-config
%{_bindir}/%{name}-module
%{_datadir}/%{name}/m4/
%{_datadir}/%{name}/WrapperTemplates/

%files examples
%defattr(-,root,root,-)
%{_datadir}/%{name}/examples/
%{_libdir}/%{name}/wrappers/external_code_threads*
%{_libdir}/%{name}/wrappers/minimal_wrapper*
%{_libdir}/%{name}/wrappers/poutre*
%{_libdir}/%{name}/wrappers/testwrapper*
%{_libdir}/%{name}/wrappers/Test*
%{_libdir}/%{name}/wrappers/wrapper.xml

%files validation
%defattr(-,root,root,-)
%{_datadir}/%{name}/validation/

%files -n python-%{name}
%defattr(-,root,root,-)
%{_datadir}/%{name}/examples/*.py
%{python_sitearch}/%{name}/

%files -n python-%{name}-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/swig/

%changelog
* Sat Jul 30 2011 Julien Schueller &lt;schueller at phimeca dot com&gt; 0.15-1
- New upstream release

* Sat Apr 9 2011 Julien Schueller &lt;schueller at phimeca dot com&gt; 0.14.0-1
- New upstream release

* Sat Oct 9 2010 Julien Schueller &lt;schueller at phimeca dot com&gt; 0.13.2-1
- New upstream release

* Mon Nov 26 2007 Remy Pagniez 0.11.1-1
- Initial package creation

