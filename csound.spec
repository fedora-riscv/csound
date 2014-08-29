Summary:       A sound synthesis language and library
Name:          csound
Version:       6.03.1
Release:       1%{?dist}
URL:           http://csound.github.io/
License:       LGPLv2+

Source0: http://downloads.sourceforge.net/csound/Csound%{version}.tar.gz
Source1: http://downloads.sourceforge.net/csound/manual_src.tar.gz
# Put plugins in _libdir/csound/plugins on all platforms
Patch0:  %{name}-6.03-64-bit-plugin-path.patch
# Rename some binaries to avoid name conflicts
Patch1:  %{name}-6.03-fix-conflicts.patch
# Default to using pulseaudio instead of portaudio
Patch2:  %{name}-6.03-default-pulse.patch
# Do not use SSE2 on non-x86_64 platforms
Patch3:  %{name}-6.03-sse2.patch
# Adapt to the way portmidi/porttime is packaged in Fedora
Patch4:  %{name}-6.03-porttime.patch
# Use xdg-open to open a browser to view the manual
Patch5:  %{name}-6.03-xdg-open.patch

BuildRequires: bison
BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: CUnit-devel
BuildRequires: docbook-style-xsl
BuildRequires: dssi-devel
BuildRequires: eigen3-static
BuildRequires: flex
BuildRequires: fltk-fluid
BuildRequires: fluidsynth-devel
BuildRequires: gettext-devel
BuildRequires: gmm-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: libcurl-devel
BuildRequires: liblo-devel
BuildRequires: libpng-devel
BuildRequires: libsndfile-devel
BuildRequires: libvorbis-devel
BuildRequires: libxslt
BuildRequires: lua-devel
BuildRequires: luajit-devel
BuildRequires: portaudio-devel
BuildRequires: portmidi-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: python2-devel
BuildRequires: stk-devel
BuildRequires: swig
BuildRequires: tkinter

# The fltk and tcl/tk frontends were removed in version 6.  These obsoletes
# can be removed once Fedora 20 reaches EOL.
Obsoletes: %{name}-gui < 6.0-1%{?dist}
Provides:  %{name}-gui = 6.0-1%{?dist}
Obsoletes: %{name}-tk  < 6.0-1%{?dist}
Provides:  %{name}-tk  = 6.0-1%{?dist}

%global luaver %(lua -v | sed -r 's/Lua ([[:digit:]]+\\.[[:digit:]]+).*/\\1/')

%description
Csound is a sound and music synthesis system, providing facilities for
composition and performance over a wide range of platforms. It is not
restricted to any style of music, having been used for many years in
at least classical, pop, techno, ambient...

%package devel
Summary: Csound development files and libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Contains headers and libraries for developing applications that use Csound.

%package python
Summary: Python Csound development files and libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python

%description python
Contains Python language bindings for developing Python applications that
use Csound.

%package python-devel
Summary: Csound python development files and libraries
Requires: %{name}-python%{?_isa} = %{version}-%{release}

%description python-devel
Contains libraries for developing against csound-python.

%package java
Summary: Java Csound support
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: java-headless
Requires: jpackage-utils

%description java
Contains Java language bindings for developing and running Java
applications that use Csound.

%package javadoc
Summary: API documentation for Java Csound support
BuildArch: noarch

%description javadoc
API documentation for the %{name}-java package.

%package lua
Summary: Lua Csound support
Requires: %{name}%{?_isa} = %{version}-%{release}

%description lua
Contains Lua language bindings for developing and running Lua
applications that use Csound.

%package csoundac
Summary: An FLTK and python frontend for Csound
Requires: %{name}-python%{?_isa} = %{version}-%{release}
Requires: xdg-utils

%description csoundac
Contains an FLTK and python frontend for Csound

%package fltk
Summary: FLTK plugins for Csound
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: fltk

%description fltk
Contains FLTK plugins for csound

%package jack
Summary: Jack Audio plugins for Csound
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: jack-audio-connection-kit

%description jack
Contains Jack Audio plugins for Csound

%package fluidsynth
Summary: Fluidsyth soundfont plugin for Csound
Requires: %{name}%{?_isa} = %{version}-%{release}

%description fluidsynth
Contains Fluidsynth soundfont plugin for Csound.

%package dssi
Summary: Disposable Soft Synth Interface (DSSI) plugin for Csound
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: dssi

%description dssi
Disposable Soft Synth Interface (DSSI) plugin for Csound

%package osc
Summary: Open Sound Control (OSC) plugin for Csound
Requires: %{name}%{?_isa} = %{version}-%{release}

%description osc
Open Sound Control (OSC) plugin for Csound

%package portaudio
Summary: PortAudio plugin for Csound
Requires: %{name}%{?_isa} = %{version}-%{release}

%description portaudio
PortAudio plugin for Csound

%package stk
Summary: STK (Synthesis ToolKit in C++) plugin for Csound
Requires: %{name}%{?_isa} = %{version}-%{release}

%description stk
STK (Synthesis ToolKit in C++) plugin for Csound

%package virtual-keyboard
Summary: Virtual MIDI keyboard plugin for Csound
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: fltk

%description virtual-keyboard
A virtual MIDI keyboard plugin for Csound

%package manual
Summary: Csound manual
License: GFDL
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description manual
Canonical Reference Manual for Csound.


%prep
%setup -q -n Csound%{version}
%setup -q -n Csound%{version} -T -D -a 1

%patch0 -b .64-bit-plugin-path
%patch1 -b .fix-conflicts
%patch2 -b .default-pulse
%ifnarch x86_64
%patch3 -b .sse2
%endif
%patch4 -b .porttime
%patch5 -b .xdg-open

# Fix python, lua, and java install paths
sed -e 's,\(set(PYTHON_MODULE_INSTALL_DIR \).*,\1"%{python_sitearch}"),' \
    -e 's,\(set(JAVA_MODULE_INSTALL_DIR.*\)),\1/csound/java),' \
    -e 's,\(set(LUA_MODULE_INSTALL_DIR.*\)),\1/lua/%{luaver}),' \
    -i CMakeLists.txt

# Fix end of line encodings
%define fix_line_encoding() \
  sed -i.orig 's/\\r\\n/\\n/;s/\\r/\\n/g' %1; \
  touch -r %1.orig %1; \
  rm -f %1.orig;

for csd in $(find manual6/examples -name \*.csd); do
  %fix_line_encoding $csd
done
%fix_line_encoding examples/c/pvsbus.csd
%fix_line_encoding examples/cplusplus/fl_controller.dev
%fix_line_encoding examples/csoundapi_tilde/csoundapi-osx.pd
%fix_line_encoding examples/lua/csound_ffi.lua
%fix_line_encoding examples/opcode_demos/band.csd
%fix_line_encoding examples/opcode_demos/sdft.csd
%fix_line_encoding manual6/examples/128,8-torus
%fix_line_encoding manual6/examples/128-spiral-8,16,128,2,1over2
%fix_line_encoding manual6/examples/128-stringcircular
%fix_line_encoding manual6/examples/string-128.matrix

# Fix spurious executable bits
chmod a-x examples/csoundapi_tilde/csoundapi-osx.pd \
          examples/csoundapi_tilde/csoundapi.pd \
          examples/lua/lua_example.lua \
          manual6/examples/128*

%build
%if %{__isa_bits} == 64
  %cmake -DUSE_LIB64:BOOL=ON -DUSE_DOUBLE:BOOL=ON
%else
  %cmake -DUSE_LIB64:BOOL=OFF -DUSE_DOUBLE:BOOL=OFF
%endif

make %{?_smp_mflags} V=1

# Generate javadoc
(cd interfaces; mkdir apidocs; javadoc -d apidocs *.java)

# Make the manual
make -C manual6 html-dist \
  XSL_BASE_PATH=%{_datadir}/sgml/docbook/xsl-stylesheets

%install
make install

# Fix the Java installation
install -dm 755 %{buildroot}%{_javadir}
(cd %{buildroot}%{_javadir}; ln -s %{_libdir}/%{name}/java/csnd.jar .)
mv %{buildroot}%{_libdir}/%{name}/java/lib_jcsound6.so %{buildroot}%{_libdir}

# Install Javadocs
install -dm 755 %{buildroot}%{_javadocdir}
cp -a interfaces/apidocs %{buildroot}%{_javadocdir}/%{name}-java

# Help the debuginfo generator
ln -s ../csound_orclex.c Engine/csound_orclex.c
ln -s ../csound_prelex.c Engine/csound_prelex.c

%find_lang %{name}6

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post python -p /sbin/ldconfig

%postun python -p /sbin/ldconfig

%post csoundac -p /sbin/ldconfig

%postun csoundac -p /sbin/ldconfig

%check
make csdtests

%files -f %{name}6.lang
%doc COPYING ChangeLog README.md Release_Notes
%{_bindir}/atsa
%{_bindir}/cs
%{_bindir}/csanalyze
%{_bindir}/csb64enc
%{_bindir}/csbeats
%{_bindir}/csdebugger
%{_bindir}/csound
%{_bindir}/cvanal
%{_bindir}/dnoise
%{_bindir}/cs-envext
%{_bindir}/cs-extract
%{_bindir}/cs-extractor
%{_bindir}/het_export
%{_bindir}/het_import
%{_bindir}/hetro
%{_bindir}/lpanal
%{_bindir}/lpc_export
%{_bindir}/lpc_import
%{_bindir}/makecsd
%{_bindir}/cs-mixer
%{_bindir}/pvanal
%{_bindir}/pv_export
%{_bindir}/pv_import
%{_bindir}/pvlook
%{_bindir}/cs-scale
%{_bindir}/scope
%{_bindir}/cs-scot
%{_bindir}/scsort
%{_bindir}/sdif2ad
%{_bindir}/cs-sndinfo
%{_bindir}/cs-srconv
%{_libdir}/lib%{name}64.so.6.0
%dir %{_libdir}/%{name}/plugins-6.0
%{_libdir}/%{name}/plugins-6.0/csladspa.so
%{_libdir}/%{name}/plugins-6.0/libampmidid.so
%{_libdir}/%{name}/plugins-6.0/libcellular.so
%{_libdir}/%{name}/plugins-6.0/libchua.so
%{_libdir}/%{name}/plugins-6.0/libcontrol.so
%{_libdir}/%{name}/plugins-6.0/libcs_date.so
%{_libdir}/%{name}/plugins-6.0/libdoppler.so
%{_libdir}/%{name}/plugins-6.0/libfareygen.so
%{_libdir}/%{name}/plugins-6.0/libfractalnoise.so
%{_libdir}/%{name}/plugins-6.0/libimage.so
%{_libdir}/%{name}/plugins-6.0/libipmidi.so
%{_libdir}/%{name}/plugins-6.0/libjacko.so
%{_libdir}/%{name}/plugins-6.0/libjoystick.so
%{_libdir}/%{name}/plugins-6.0/liblinear_algebra.so
%{_libdir}/%{name}/plugins-6.0/libmixer.so
%{_libdir}/%{name}/plugins-6.0/libplaterev.so
%{_libdir}/%{name}/plugins-6.0/librtalsa.so
%{_libdir}/%{name}/plugins-6.0/librtpulse.so
%{_libdir}/%{name}/plugins-6.0/libscansyn.so
%{_libdir}/%{name}/plugins-6.0/libserial.so
%{_libdir}/%{name}/plugins-6.0/libsignalflowgraph.so
%{_libdir}/%{name}/plugins-6.0/libstdutil.so
%{_libdir}/%{name}/plugins-6.0/libsystem_call.so
%{_libdir}/%{name}/plugins-6.0/liburandom.so

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}64.so
%{_libdir}/libcsnd6.so

%files python
%{_libdir}/libcsnd6.so.6.0
%{_libdir}/%{name}/plugins-6.0/libpy.so
%{python_sitearch}/_csnd*
%{python_sitearch}/csnd*

%files python-devel
%{_libdir}/libCsoundAC.so

%files java
%{_libdir}/lib_jcsound6.so
%{_libdir}/%{name}/java/
%{_javadir}/csnd.jar

%files javadoc
%doc COPYING
%{_javadocdir}/%{name}-java

%files lua
%{_libdir}/%{name}/plugins-6.0/libLuaCsound.so
%{_libdir}/lua/%{luaver}/*

%files csoundac
%{python_sitearch}/CsoundAC.*
%{python_sitearch}/_CsoundAC.*
%{_libdir}/libCsoundAC.so.*

%files fltk
%{_libdir}/%{name}/plugins-6.0/libwidgets.so

%files jack
%{_libdir}/%{name}/plugins-6.0/librtjack.so
%{_libdir}/%{name}/plugins-6.0/libjackTransport.so

%files fluidsynth
%{_libdir}/%{name}/plugins-6.0/libfluidOpcodes.so

%files dssi
%{_libdir}/%{name}/plugins-6.0/libdssi4cs.so

%files osc
%{_libdir}/%{name}/plugins-6.0/libosc.so

%files portaudio
%{_libdir}/%{name}/plugins-6.0/librtpa.so

%files stk
%{_libdir}/%{name}/plugins-6.0/libstk.so

%files virtual-keyboard
%{_libdir}/%{name}/plugins-6.0/libvirtual.so

%files manual
%doc examples manual6/copying.txt manual6/html

%changelog
* Fri Aug 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 6.03.1-1
- Update to 6.03.1
- Spec file fixups

* Mon Jul 28 2014 Jerry James <loganjerry@gmail.com> - 6.03.0-1
- Update to 6.03.0 (bz 1094866; fixes bzs 1057580, 1067182, and 1106095)
- Change project URL to github page
- Update BRs and reorganize for readability
- Bring back the manual sources; the manual subpackage has the GFDL license
- Obsolete the -gui and -tk subpackages (no longer supported upstream)
- Add -csoundac, -lua, -portaudio, and -stk subpackages

* Tue Jul  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 5.19.01-7
- Minor cleanups

* Tue Jul 01 2014 Mat Booth <mat.booth@redhat.com> - 5.19.01-6
- Drop support for GCJ AOT compilation (GCJ was retired)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.19.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 5.19.01-4
- Rebuild for boost 1.55.0

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 5.19.01-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 5.19.01-2
- Use xdg-open as help browser again.
- Drop no longer applicable docdir adjustment from specfile (#993711).

* Wed Aug  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 5.19.01-1
- Update to 5.19.01 (fix FTBFS)
- Initial rebase of patches
- Cleanup and modernise spec
- Drop manual (no longer produced upstream) but still ship HTML manual

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.13.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 5.13.0-12
- Rebuild for boost 1.54.0

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.13.0-11
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.13.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.13.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.13.0-8
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.13.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 5.13.0-6
- Rebuild for new libpng

* Tue Jun 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 5.13.0-5
- Build the old Parser as the new Parser isn't stable even though it default!

* Wed Jun 01 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 5.13.0-4
- Reflect fltk include paths having changed.

* Fri May 27 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 5.13.0-3
- Bump build for new fltk

* Fri Apr 29 2011 Dan Horák <dan[at]danny.cz> - 5.13.0-2
- mark s390x as 64-bit arch

* Wed Apr  6 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 5.13.0-1
- Update to 5.13.0.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 26 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 5.12.1-1
- Update to 5.12.1.

* Sat Jul 31 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 5.10.1-21
- Fix python location

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 5.10.1-20
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 20 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 5.10.1-19
- bump build

* Mon Jul 12 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 5.10.1-18
- Add license file to -javadocs

* Sat Jan  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 5.10.1-17
- Some further cleanups

* Sat Jan  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 5.10.1-16
- Some further cleanups

* Sat Jan  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 5.10.1-15
- Updated to the new python sysarch spec file reqs

* Thu Dec  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 5.10.1-14
- Updated python patch thanks to dsd.

* Tue Oct 20 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 5.10.1-13
- Fix use of multiple midi devices, fix segfault (RHBZ 529293)

* Sat Sep  5 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 5.10.1-12
- Build fixes, set PulseAudio as default

* Tue Aug 18 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 5.10.1-11
- Further python build fixes
