%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# uncomment to enable ghelp/omf/scrollkeeper support
# not working as of version 0.8.7
#global scrollkeeper 1

Name:           gnash
Version:        0.8.8
Release:        2%{?dist}
Epoch:          1
Summary:        GNU flash movie player

Group:          Applications/Multimedia
License:        GPLv3+
URL:            http://www.gnu.org/software/gnash/
Source0:        http://ftp.gnu.org/gnu/gnash/%{version}/%{name}-%{version}.tar.bz2
Source1:        http://www.getgnash.org/gnash-splash.swf
Source2:        gnash.desktop

# register KComponentData properly in KDE 4 KPart
Patch0:         gnash-0.8.3-fix-kde4-port.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxml2-devel libpng-devel libjpeg-devel libogg-devel
BuildRequires:  boost-devel curl-devel freetype-devel fontconfig-devel
BuildRequires:  SDL-devel 
BuildRequires:  agg-devel 
BuildRequires:  kde-filesystem
BuildRequires:  kdelibs-devel
BuildRequires:  gtkglext-devel
BuildRequires:  docbook2X
BuildRequires:  %{_bindir}/docbook2pdf
BuildRequires:  gstreamer-devel >= 0.10
%if 0%{?scrollkeeper}
BuildRequires:  scrollkeeper
%endif
BuildRequires:  giflib-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  speex-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  pygtk2-devel
BuildRequires:  libtool-ltdl-devel

%if 0%{?scrollkeeper}
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
Gnash is capable of reading up to SWF v9 files and opcodes, but primarily
supports SWF v7, with better SWF v8 and v9 support under heavy development.
Gnash includes initial parser support for SWF v8 and v9. Not all 
ActionScript 2 classes are implemented yet, but all of the most heavily 
used ones are. Many ActionScript 2 classes are partially implemented; 
there is support for all of the commonly used methods of each
class.

%package plugin
Summary:   Web-client flash movie player plugin 
Requires:  %{name} = %{epoch}:%{version}-%{release}
Requires:  mozilla-filesystem%{?_isa} webclient
Group:     Applications/Internet

%description plugin
The gnash flash movie player plugin for firefox or mozilla.

%package klash
Summary:   Konqueror flash movie player plugin
Requires:  %{name} = %{epoch}:%{version}-%{release}
Group:     Applications/Multimedia

%description klash
The gnash flash movie player plugin for Konqueror.

%package cygnal
Summary:   Streaming media server
Requires:  %{name} = %{epoch}:%{version}-%{release}
Group:     Applications/Multimedia

%description cygnal
Cygnal is a streaming media server that's Flash aware.

%package devel
Summary:   Gnash header files
Requires:  %{name} = %{epoch}:%{version}-%{release}
Group:     Development/Libraries

%description devel
Gnash header files can be used to write external Gnash extensions or to embed
the Gnash GTK+ widget into a C/C++ application.

%package -n python-gnash
Summary:   Gnash Python bindings
Requires:  %{name} = %{epoch}:%{version}-%{release}
Group:     Applications/Multimedia

%description -n python-gnash
Python bindings for the Gnash widget. Can be used to embed Gnash into any PyGTK
application.

%prep
%setup -q
%patch0 -p1 -b .fix-kde4
# Hack as autoreconf breaks build
sed -i -e 's!kapp.h!kapplication.h!g' configure
sed -i -e 's!libkdeui.la!libkdeui.so!g' configure
# Currently kde4-gnash (from kde4 branch) links against various KDE libraries,
# but only needs Qt -- remove the superfluous linkage
sed -i -e 's!\$(KDE4_LIBS)!!g' gui/Makefile.in
# we don't want any builtin ltdl built, configure wants always either
# ltdl-install or ltdl-convenience, hack that out
sed -i -e 's/test x"\${enable_ltdl_convenience-no}" != xno/false/g' configure
# and don't build the loader part of libltdl either
sed -i -e 's/\$(LT_DLLOADERS)//g' libltdl/Makefile.in
# link to the system libltdl instead of the bundled one
# this is hardcoded in the makefiles, so --without-included-ltdl doesn't help
sed -i -e 's!\$(top_builddir)/libltdl/libltdlc.la!-lltdl!g' \
  */Makefile.in */*/Makefile.in
# delete bundled libltdl stuff to make sure it's not used
rm -f libltdl/*.[ch] libltdl/*/*.[ch]
# fix the check for the docbook2X tools being in Perl
sed -i -e 's/" perl "/"perl "/g' configure

iconv -f latin1 -t utf8 < AUTHORS > AUTHORS.utf8
touch -r AUTHORS AUTHORS.utf8
mv AUTHORS.utf8 AUTHORS

%build
%configure --disable-static --with-npapi-plugindir=%{_libdir}/mozilla/plugins \
  --enable-docbook --enable-ghelp --enable-media=GST \
  --disable-dependency-tracking --disable-rpath \
  --enable-cygnal \
  --enable-sdkinstall \
  --enable-python \
  --enable-gui=gtk,kde4,sdl,fb \
  --with-kde4-prefix=%{_kde4_prefix} \
  --with-kde4-lib=%{_kde4_libdir}/kde4/devel \
  --with-kde4-incl=%{_kde4_includedir} \
  --without-included-ltdl
# make sure the Qt 4 moc etc. tools are found
export PATH=%{_qt4_prefix}/bin:$PATH
#doesn't work currently: %%{?_smp_mflags}
# override KDE4_LIBS because configure doesn't detect it properly
make KDE4_LIBS='-L%{_kde4_libdir}/kde4/devel -lkparts -lkdeui -lkdecore'

%install
rm -rf $RPM_BUILD_ROOT
make install install-plugins \
 DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' \
 KDE4_PLUGINDIR=%{_kde4_libdir}/kde4 \
 KDE4_SERVICESDIR=%{_kde4_datadir}/kde4/services \
 KDE4_CONFIGDIR=%{_kde4_configdir} \
 KDE4_APPSDATADIR=%{_kde4_appsdir}/klash
rm $RPM_BUILD_ROOT%{_libdir}/gnash/*.la
# KDE 4 doesn't need the .la file anymore, thankfully
rm $RPM_BUILD_ROOT%{_kde4_libdir}/kde4/libklashpart.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

rm -rf __dist_docs
mkdir __dist_docs
mv $RPM_BUILD_ROOT%{_datadir}/doc/gnash/* __dist_docs/
rmdir $RPM_BUILD_ROOT%{_datadir}/doc/gnash

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/gnash/

mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
# a wrapper to avoid gnash erroring out if there is no argument.
# Instead open gnash-splash.swf.
# this should not be needed in the next version.
# FIXME: Do we still need this with 0.8.7?
cat > $RPM_BUILD_ROOT%{_libexecdir}/gnash-wrapper << EOF
#! /bin/sh
if [ "z\$1" = 'z' ]; then
 gnash %{_datadir}/gnash/gnash-splash.swf
else
 gnash "\$@"
fi
EOF

chmod a+x $RPM_BUILD_ROOT%{_libexecdir}/gnash-wrapper

sed -e 's;/usr/libexec;%{_libexecdir};' %{SOURCE2} > gnash.desktop
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor="fedora" \
 --dir=$RPM_BUILD_ROOT%{_datadir}/applications/ \
 gnash.desktop

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
cp -p ./gui/images/GnashG.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%post 
/sbin/ldconfig
%if 0%{?scrollkeeper}
scrollkeeper-update -q -o %{_datadir}/omf/%{name} || :
%endif
/sbin/install-info %{_infodir}/gnash_ref.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gnash_user.info %{_infodir}/dir || :

update-desktop-database &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gnash_ref.info %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gnash_user.info %{_infodir}/dir || :
fi

%postun
/sbin/ldconfig
%if 0%{?scrollkeeper}
scrollkeeper-update -q || :
%endif

update-desktop-database &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS 
%doc __dist_docs/*
%config(noreplace) %{_sysconfdir}/gnashpluginrc
%config(noreplace) %{_sysconfdir}/gnashrc
%{_bindir}/fb-gnash
%{_bindir}/flvdumper
%{_bindir}/gtk-gnash
%{_bindir}/rtmpget
%{_bindir}/sdl-gnash
%{_bindir}/soldumper
%{_bindir}/gnash
%{_bindir}/gprocessor
%{_bindir}/findmicrophones
%{_bindir}/findwebcams
%dir %{_libdir}/gnash
%{_libdir}/gnash/*.so*
%{_mandir}/man1/gnash.1*
%{_mandir}/man1/gprocessor.1*
%{_mandir}/man1/soldumper.1*
%{_mandir}/man1/flvdumper.1*
%{_mandir}/man1/findmicrophones.1*
%{_mandir}/man1/findwebcams.1*
%{_mandir}/man1/gtk-gnash.1*
%{_infodir}/gnash*
%{_datadir}/gnash/
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/applications/*.desktop
%{_libexecdir}/gnash-wrapper
%if 0%{?scrollkeeper}
%{_datadir}/omf/gnash/
%endif

%files plugin
%defattr(-,root,root,-)
%{_libdir}/mozilla/plugins/libgnashplugin.so

%files klash
%defattr(-,root,root,-)
%{_kde4_bindir}/kde4-gnash
%{_kde4_libdir}/kde4/libklashpart.so
%{_kde4_appsdir}/klash/
%{_kde4_datadir}/kde4/services/klash_part.desktop
%{_mandir}/man1/kde4-gnash.1*

%files cygnal
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/cygnalrc
%{_bindir}/cygnal
%{_mandir}/man1/cygnal.1*
%{_mandir}/man1/rtmpget.1*
%dir %{_libdir}/cygnal
%{_libdir}/cygnal/plugins/*.so*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gnash/
%{_libdir}/pkgconfig/gnash.pc

%files -n python-gnash
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/*

%changelog
* Fri Aug 27 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.8-2
- fix the check for the docbook2X tools being in Perl (fixes FTBFS)

* Wed Aug 25 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.8-1.1
- rebuild for the official release of Boost 1.44.0 (silent ABI change)

* Mon Aug 23 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.8-1
- update to 0.8.8 (#626352, #574100, #606170)
- update file list (patch by Jeff Smith)

* Thu Jul 29 2010 Bill Nottingham <notting@redhat.com> - 1:0.8.7-5
- Rebuilt for boost-1.44, again

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 1:0.8.7-4
- Rebuilt for boost-1.44

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1:0.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 08 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.7-2
- -plugin: avoid file (directory) dependency (#601942)

* Sat Feb 27 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.7-1
- update to 0.8.7 (#568971)
- make scrollkeeper a conditional (still disabled as it's not working)
- drop gnash-0.8.3-manual.patch, should no longer be needed
- drop gnash-0.8.6-python-install-dir.patch, fixed upstream

* Fri Feb 12 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-13
- delete bundled libltdl stuff to make sure it's not used

* Thu Feb 11 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-12
- don't build libltdlc.a

* Thu Feb 11 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-11
- --without-included-ltdl (CVE-2009-3736)

* Fri Jan 22 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-10
- Rebuild for new Boost (1.41.0)

* Sat Jan 02 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-9
- Add missing Epoch to Requires

* Sat Jan 02 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-8
- Install icon to the correct place (#551621)

* Wed Dec 30 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-7
- One more try at using the correct dir

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-6
- Patch was reversed

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-5
- Patch Makefile.in, not Makefile.am

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-4
- Pick up python modules from the right dir

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-3
- Install python modules in the right dir

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-2
- Add cygnal plugins

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-1
- Update to 0.8.6, increase epoch.

* Thu Sep 10 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.8.20090910bzr11506
- update to HEAD

* Thu Sep 10 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.7.20090910bzr11505
- update to HEAD

* Mon Aug 10 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.0-0.6.20090809bzr11401
- don't package headers in -widget, only in -devel (no duplicate files)
- own %%{_includedir}/gnash/ in -devel
- add missing %%defattr for -devel and -widget
- make -devel and -widget require the main package (with exact VR)
- fix -devel group and description
- rename gnash-widget to python-gnash as per the naming guidelines

* Sun Aug 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.0-0.5.20090809bzr11401
- use %%{_includedir}, not %%{_prefix}/include

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.4.20090809bzr11401
- Install the python module in the sitearch dir

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.3.20090809bzr11401
- One more 64bit fix

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.3.20090809bzr11400
- Fix the packaging in 64bits

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.2.20090809bzr11400
- upload the .swf file

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.1.20090809bzr11400
- merge upstream changes into the spec

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.5-4
- rebuild for new Boost

* Fri Mar 06 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.5-3
- explicitly link the KlashPart against the libraries it uses

* Fri Mar 06 2009 Jaroslav Reznik <jreznik@redhat.com> 0.8.5-2
- add missing speex-devel and gstreamer-plugins-base-devel BR
 
* Fri Mar 06 2009 Jaroslav Reznik <jreznik@redhat.com> 0.8.5-1
- update to 0.8.5
- remove use_kde3_executable_hack
- remove autoreconf

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.8.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.4-6
- rebuild for new boost

* Thu Nov 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.4-5
- add missing portions of KDE 4 port from upstream kde4 branch

* Thu Nov 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.4-4
- add 3 more patches from bero to fix the KDE 4 viewer executable
- disable use_kde3_executable hack

* Sun Oct 19 2008 Patrice Dumas <pertusus@free.fr> 0.8.4-3
- add a desktop file

* Sat Oct 18 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.4-2
- update KDE 4 patch (undo the backporting and use original patch)
- patch to make autoreconf work
- add missing BR giflib-devel, gettext
- omit unrecognized --with-qtdir

* Sat Oct 18 2008 Patrice Dumas <pertusus@free.fr> 0.8.4-1
- update to 0.8.4

* Thu Oct  4 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.3-6
- use the KDE 3 executable with the KDE 4 KPart for now (making this conditional
  so it can easily be disabled or removed once the KDE 4 executable is fixed)

* Thu Oct  4 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.3-5
- register KComponentData properly in KDE 4 KPart

* Wed Oct  3 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.3-4
- KDE 4 port of klash by Benjamin Wolsey and Bernhard Rosenkränzer

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> 0.8.3-3
- include %%_libdir/gnash directory

* Wed Jun 25 2008 Patrice Dumas <pertusus@free.fr> 0.8.3-2
- add glib in the link, thanks Daniel Drake (#452767)

* Sun Jun 22 2008 Patrice Dumas <pertusus@free.fr> 0.8.3-1
- update to 0.8.3

* Wed Apr  9 2008 Patrice Dumas <pertusus@free.fr> 0.8.2-3
- ship libklashpart (#441601)

* Mon Mar 10 2008 Patrice Dumas <pertusus@free.fr> 0.8.2-2
- don't ship libltdl.so.3 (#436725)

* Fri Mar  7 2008 Patrice Dumas <pertusus@free.fr> 0.8.2-1
- update to 0.8.2

* Sat Oct 27 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-6
- add patch from Martin Stransky to fix wrapped plugin #281061

* Thu Sep 20 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-5
- info files are empty, don't install them

* Thu Sep 20 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-4
- omf/scrollkeeper doc is broken, remove it

* Fri Sep  7 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-3
- better documentation generation

* Wed Sep  5 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-2
- update to 0.8.1
- agg is now the default renderer

* Fri Aug  3 2007 Patrice Dumas <pertusus@free.fr> 0.8.0-2
- rebuild for boost soname change

* Sun Jun 17 2007 Patrice Dumas <pertusus@free.fr> 0.8.0-1
- update to 0.8.0

* Wed May  9 2007 Patrice Dumas <pertusus@free.fr> 0.7.2-2
- fix CVE-2007-2500 (fix 239213)

* Sat Nov  6 2006 Patrice Dumas <pertusus@free.fr> 0.7.2-1
- update for 0.7.2 release.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.7.1-9
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 24 2006 Patrice Dumas <pertusus@free.fr> 0.7.1-8
- plugin requires %%{_libdir}/mozilla/plugins. Fix (incompletly and 
  temporarily, but there is no better solution yet) #207613

* Sun Aug 27 2006 Patrice Dumas <pertusus@free.fr> - 0.7.1-7
- add defattr for klash
- add warnings in the description about stability

* Mon Aug 21 2006 Patrice Dumas <pertusus@free.fr> - 0.7.1-6
- remove superfluous buildrequires autoconf
- rename last patch to gnash-plugin-tempfile-dir.patch
- add README.fedora to plugin to explain tmpdirs

* Wed Aug 16 2006 Jens Petersen <petersen@redhat.com> - 0.7.1-5
- source qt.sh and configure --with-qtdir (Dominik Mierzejewski)
- add plugin-tempfile-dir.patch for plugin to use a safe tempdir

* Fri Jul 28 2006 Jens Petersen <petersen@redhat.com> - 0.7.1-4
- buildrequire autotools (Michael Knox)

* Fri Jun  2 2006 Patrice Dumas <pertusus@free.fr> - 0.7.1-3
- add gnash-continue_on_info_install_error.patch to avoid
- buildrequire libXmu-devel

* Wed May 17 2006 Jens Petersen <petersen@redhat.com> - 0.7.1-2
- configure with --disable-rpath
- buildrequire docbook2X
- remove devel files

* Sun May  7 2006 Jens Petersen <petersen@redhat.com> - 0.7.1-1
- update to 0.7.1 alpha release

* Sat Apr  22 2006 Rob Savoye <rob@welcomehome.org> - 0.7-1
- install the info file. Various tweaks for my system based on
Patrice's latest patch,

* Fri Feb  3 2006 Patrice Dumas <dumas@centre-cired.fr> - 0.7-1
- initial packaging
