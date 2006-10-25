# Csound is really dumb about 64-bit
%ifarch x86_64 ia64 ppc64
%define build64bit 1
%define install64bit --word64
%else
%define build64bit 0
%define install64bit %{nil}
%endif


Summary:       Csound - sound synthesis language and library
Name:          csound
Version:       5.03.0
Release:       5%{?dist}
URL:           http://csound.sourceforge.net/
License:       LGPL
Group:         Applications/Multimedia

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: swig scons libsndfile-devel libpng-devel libjpeg-devel
BuildRequires: python python-devel
BuildRequires: alsa-lib-devel fluidsynth-devel
BuildRequires: jack-audio-connection-kit-devel liblo-devel dssi-devel 
BuildRequires: fltk-devel fltk-fluid
BuildRequires: java-devel >= 1.4.0
BuildRequires: jpackage-utils >= 1.5
BuildRequires: java-gcj-compat-devel
BuildRequires: tk-devel tcl-devel
BuildRequires: tetex tetex-latex libxslt

Source0:     http://superb-east.dl.sourceforge.net/sourceforge/csound/Csound5.03_src-cvs20061023.tar.bz2

# NOTE:
# Manual sources aren't distributed, but may be extracted from CVS via...
# cvs -d :pserver:anonymous@csound.cvs.sourceforge.net:/cvsroot/csound login
# cvs -z9 -d :pserver:anonymous@csound.cvs.sourceforge.net:/cvsroot/csound checkout -P -r csound-5_03_0 manual
Source1: Csound5.03_manual.tgz

Patch0: csound-5.03.0-enable-fluidsynth.patch
Patch1: csound-5.03.0-gstabs-disable-option.patch
Patch2: csound-5.03.0-no-usr-local.patch
Patch3: csound-5.03.0-disable-atsa.patch
Patch4: csound-5.03.0-remote-fixes.patch


%description
Csound is a sound and music synthesis system, providing facilities for
composition and performance over a wide range of platforms. It is not
restricted to any style of music, having been used for many years in
at least classical, pop, techno, ambient...


%package devel
Summary: Csound development files and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Contains headers and libraries for developing applications that use Csound.

%package python
Summary: Python Csound development files and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: python

%description python
Contains Python language bindings for developing Python applications that
use Csound.

%package java
Summary: Java Csound support
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires:         jpackage-utils >= 1.5
Requires:         java-1.4.2-gcj-compat >= 1.4.2.0-40jpp_88rh
Requires(post):   jpackage-utils >= 1.5
Requires(postun): jpackage-utils >= 1.5
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description java
Contains Java language bindings for developing and running Java
applications that use Csound.

%package javadoc
Summary: API documentation for Java Csound support
Group: Documentation

%description javadoc
API documentation for the %{name}-java package.

%package tk
Summary: Tcl/Tk related Csound utilities
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Requires: tcl tk

%description tk
Contains Tcl/Tk related Csound utilities

%package gui
Summary: A FLTK-based GUI for Csound
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Requires: fltk xdg-utils

%description gui
Contains a FLTK-based GUI for Csound

%package jack
Summary: Jack Audio plugins for Csound
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Requires: jack-audio-connection-kit

%description jack
Contains Jack Audio plugins for Csound

%package fluidsynth
Summary: Fluidsyth soundfont plugin for Csound
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Requires: fluidsynth-libs

%description fluidsynth
Contains Fluidsynth soundfont plugin for Csound.

%package dssi
Summary: Disposable Soft Synth Interface (DSSI) plugin for Csound
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Requires: dssi

%description dssi
Disposable Soft Synth Interface (DSSI) plugin for Csound

%package osc
Summary: Open Sound Control (OSC) plugin for Csound
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description osc
Open Sound Control (OSC) plugin for Csound

%package manual
Summary: Csound manual
Group: Documentation

%description manual
Canonical Reference Manual for Csound.

%package tutorial
Summary: Csound tutorial
Group: Documentation

%description tutorial
Tutorial documentation and sample files for Csound.


%prep
%setup -q -n Csound5.03.0
%patch0 -p1 -b .enable-fluidsynth
%patch1 -p1 -b .gstabs-disable-option
%patch2 -p1 -b .no-usr-local
%patch3 -p1 -b .disable-atsa
%patch4 -p1 -b .remote-fixes

tar xf %{SOURCE1}

%build

# Adjust location of the documentation for the GUI bits
sed -ie 's#\"firefox /usr/local/share/doc/csound/manual/#\"xdg-open file://%{_docdir}/%{name}-manual-%{version}/#' \
      frontends/fltk_gui/CsoundGlobalSettings.cpp

scons dynamicCsoundLibrary=1 \
      buildRelease=0 \
      noDebug=0 \
      disableGStabs=1 \
      buildInterfaces=1 \
      useALSA=1 \
      usePortAudio=0 \
      usePortMIDI=0 \
      useOSC=1 \
      useJack=1 \
      useFLTK=1 \
      useFluidsynth=1 \
      generatePdf=0 \
      buildCsound5GUI=1 \
      buildPythonOpcodes=1 \
      buildTclcsound=1 \
      buildJavaWrapper=1 \
      buildDSSI=1 \
      buildUtilities=1 \
      prefix=%{_prefix} \
      customCCFLAGS="%{optflags}" \
      customCXXFLAGS="%{optflags}" \
      Word64=%{build64bit}

# Build the manual
(cd manual; make)

# Generate javadoc
(cd interfaces; javadoc *.java)

# Build the tutorial documentation
(cd tutorial; \
 pdflatex tutorial; bibtex tutorial; pdflatex tutorial; pdflatex tutorial)


%install
%{__rm} -rf %{buildroot}
%{__python} install.py --prefix=%{_prefix} --instdir=%{buildroot} %{install64bit}
%{__rm} -f %{buildroot}%{_docdir}/%{name}/COPYING
%{__rm} -f %{buildroot}%{_docdir}/%{name}/ChangeLog
%{__rm} -f %{buildroot}%{_docdir}/%{name}/INSTALL
%{__rm} -f %{buildroot}%{_docdir}/%{name}/readme-csound5.txt
%{__rm} -f %{buildroot}%{_bindir}/uninstall-csound5
%{__rm} -f %{buildroot}%{_prefix}/csound5-*.md5sums

# This file is zero-lenth for some reason
%{__rm} -f manual/examples/ifthen.csd

%{__mv} %{buildroot}%{_libdir}/lib_csnd.so %{buildroot}%{_libdir}/python2.4/site-packages/_csnd.so

install -dm 755 %{buildroot}%{_javadir}
(cd %{buildroot}%{_javadir}; ln -s %{_libdir}/%{name}/java/csnd.jar .)

install -dm 766 %{buildroot}%{_javadocdir}/%{name}-java
(cd interfaces; tar cf - *.html csnd/*.html) | (cd %{buildroot}%{_javadocdir}/%{name}-java; tar xvf -)

%{_bindir}/aot-compile-rpm

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post java
if [ -x %{_bindir}/rebuild-gcj-db ]; then
  %{_bindir}/rebuild-gcj-db
fi

%postun java
if [ -x %{_bindir}/rebuild-gcj-db ]; then
  %{_bindir}/rebuild-gcj-db
fi

%files
%defattr(-,root,root,0755)
%doc COPYING ChangeLog readme-csound5.txt
%{_bindir}/cs
%{_bindir}/csb64enc
%{_bindir}/csound
%{_bindir}/cvanal
%{_bindir}/dnoise
%{_bindir}/envext
%{_bindir}/extract
%{_bindir}/extractor
%{_bindir}/het_export
%{_bindir}/het_import
%{_bindir}/hetro
%{_bindir}/lpanal
%{_bindir}/lpc_export
%{_bindir}/lpc_import
%{_bindir}/makecsd
%{_bindir}/mixer
%{_bindir}/pvanal
%{_bindir}/pvlook
%{_bindir}/scale
%{_bindir}/scot
%{_bindir}/scsort
%{_bindir}/sndinfo
%{_bindir}/srconv
%{_bindir}/pv_export
%{_bindir}/pv_import
%{_libdir}/lib%{name}.so.5.1
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/xmg/*.xmg
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/libbabo.so
%{_libdir}/%{name}/plugins/libbarmodel.so
%{_libdir}/%{name}/plugins/libcompress.so
%{_libdir}/%{name}/plugins/libcontrol.so
%{_libdir}/%{name}/plugins/libftest.so
%{_libdir}/%{name}/plugins/libgrain4.so
%{_libdir}/%{name}/plugins/libhrtferX.so
%{_libdir}/%{name}/plugins/libloscilx.so
%{_libdir}/%{name}/plugins/libminmax.so
%{_libdir}/%{name}/plugins/libmixer.so
%{_libdir}/%{name}/plugins/libmodal4.so
%{_libdir}/%{name}/plugins/libphisem.so
%{_libdir}/%{name}/plugins/libphysmod.so
%{_libdir}/%{name}/plugins/libpitch.so
%{_libdir}/%{name}/plugins/libpvoc.so
%{_libdir}/%{name}/plugins/libpvs_ops.so
%{_libdir}/%{name}/plugins/libpy.so
%{_libdir}/%{name}/plugins/librtalsa.so
%{_libdir}/%{name}/plugins/libscansyn.so
%{_libdir}/%{name}/plugins/libsfont.so
%{_libdir}/%{name}/plugins/libstackops.so
%{_libdir}/%{name}/plugins/libstdopcod.so
%{_libdir}/%{name}/plugins/libstdutil.so
%{_libdir}/%{name}/plugins/libudprecv.so
%{_libdir}/%{name}/plugins/libudpsend.so
%{_libdir}/%{name}/plugins/libvbap.so
%{_libdir}/%{name}/plugins/libharmon.so
%{_libdir}/%{name}/plugins/libugakbari.so
%{_libdir}/%{name}/plugins/libvaops.so
%{_libdir}/%{name}/plugins/opcodes.dir

%files devel
%defattr(-,root,root,0755)
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so

%files python
%defattr(-,root,root,0755)
%{_libdir}/python2.4/site-packages/*

%files java
%{_libdir}/lib_jcsound.so
%{_libdir}/%{name}/java/
%{_javadir}/csnd.jar
%attr(-,root,root) %{_libdir}/gcj/%{name}

%files javadoc
%defattr(-,root,root,0755)
%doc %{_javadocdir}/%{name}-java

%files tk
%defattr(-,root,root,0755)
%{_libdir}/%{name}/tcl/
%{_bindir}/matrix.tk
%{_bindir}/brkpt
%{_bindir}/linseg
%{_bindir}/tabdes
%{_bindir}/cstclsh
%{_bindir}/cswish

%files gui
%defattr(-,root,root,0755)
%{_bindir}/csound5gui
%{_libdir}/%{name}/plugins/libwidgets.so

%files jack
%defattr(-,root,root,0755)
%{_libdir}/%{name}/plugins/librtjack.so

%files fluidsynth
%defattr(-,root,root,0755)
%{_libdir}/%{name}/plugins/libfluidOpcodes.so

%files dssi
%defattr(-,root,root,0755)
%{_libdir}/%{name}/plugins/libdssi4cs.so

%files osc
%defattr(-,root,root,0755)
%{_libdir}/%{name}/plugins/libosc.so

%files manual
%defattr(-,root,root,0755)
%doc manual/copying.txt manual/credits.txt manual/bugs.txt manual/readme.txt manual/news.txt
%doc manual/html/*
%doc manual/examples

%files tutorial
%defattr(-,root,root,0755)
%doc tutorial/tutorial.pdf
%doc tutorial/*.csd
%doc tutorial/*.cpr
%doc tutorial/*.py

%changelog
* Wed Oct 25 2006 Dan Williams <dcbw@redhat.com> 5.03.0-5
- Fix the remote plugin's local IP address read code, add more error checking

* Mon Oct 23 2006 Dan Williams <dcbw@redhat.com> 5.03.0-4
- Drop csound-5.03.0-uninitialized.patch, upstream
- Drop csound-5.03.0-printf-redef.patch, upstream
- CVS snapshot to grab some updated opcodes and fixes
- Make disabling -gstabs an option for better upstream palatability
- Disable atsa; it breaks the build for some unknown reason

* Fri Sep  8 2006 Dan Williams <dcbw@redhat.com> 5.03.0-3
- csound-5.03.0-no-gstabs.patch added; produce dwarf2 like everyone else

* Fri Aug 24 2006 Dan Williams <dcbw@redhat.com> 5.03.0-2
- Kill printf redefinition
- Remove zero-length ifthen.csd
- Remove explicit liblo dep in csound-osc
- Add fluidsynth plugin

* Fri Aug 24 2006 Dan Williams <dcbw@redhat.com> 5.03.0-1
- Package for Fedora Extras
