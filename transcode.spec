# TODO (sometime, maybe):
# - avifile (ick): http://avifile.sourceforge.net/
# - LoRS/IBP: http://loci.cs.utk.edu/

# I bet this _will_ change in the future.
%define pvmdir  %{_datadir}/pvm3

Name:           transcode
Version:        1.0.5
Release:        5%{?dist}
Summary:        Video stream processing tool

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.transcoding.org/
Source0:        http://fromani.exit1.org/%{name}-%{version}.tar.bz2
Patch0:         %{name}-pvmbin.patch
Patch2:         %{name}-1.0.2-lzo2.patch
Patch3:		transcode-1.0.4.external_dv.patch
Patch6:		transcode-1.0.5-nuv.patch
Patch7:		transcode-1.0.5-ffmpeg.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libdvdread-devel
BuildRequires:  a52dec-devel
BuildRequires:  libxml2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  lzo-devel >= 2
BuildRequires:  mjpegtools-devel
BuildRequires:  libdv-devel
BuildRequires:  xvidcore-devel
BuildRequires:  libquicktime-devel >= 0.9.8
BuildRequires:  lame-devel >= 3.89
BuildRequires:  SDL-devel >= 1.1.6
BuildRequires:  ffmpeg-devel >= 0.4.9
BuildRequires:  mpeg2dec-devel >= 0.4.0-0.lvn.3.b
BuildRequires:  pvm
BuildRequires:  libtheora-devel
BuildRequires:  libXv-devel
BuildRequires:  libXaw-devel
BuildRequires:  libXpm-devel
BuildRequires:  freetype-devel
%ifarch %{ix86}
BuildRequires:  nasm
%endif
BuildRequires:  ImageMagick-devel >= 5.4.3
BuildRequires:	libmpeg3-devel

# libtool + autotools for patch2, autoreconf
BuildRequires:  libtool

Requires:       xvidcore


%description
transcode is a text console video-stream processing tool. It supports
elementary video and audio frame transformations. Some example modules
are included to enable import of MPEG-1/2, Digital Video, and other
formats. It also includes export modules for writing to AVI files with
DivX, OpenDivX, XviD, Digital Video or other codecs. Direct DVD
transcoding is also supported. A set of tools is available to extract
and decode the sources into raw video/audio streams for import and to
enable post-processing of AVI files.


%prep
%setup -q
%patch0 -p1 -b .pvmbin
%patch2 -p1 -b .lzo
%patch3 -p1 -b .external_dv
rm filter/preview/dv_types.h
%patch6 -p1 -b .types
%patch7 -p1 -b .ffmpeg

%build
autoreconf # for patch2, and fixes standard rpaths on lib64 archs
for file in docs/{man/*.1,export_mp2.txt,export_mpeg.txt,filter_dnr.txt} \
    AUTHORS ChangeLog README docs/README.vcd ; do
    iconv -f iso-8859-1 -t utf-8 $file > $file.utf8 && mv -f $file.utf8 $file
done

%configure \
        --disable-dependency-tracking                           \
        --with-x                                                \
        --enable-netstream                                      \
        --enable-v4l                                            \
        --enable-oss                                            \
        --enable-libpostproc                                    \
        --enable-freetype2                                      \
        --enable-ogg                                            \
        --enable-vorbis                                         \
        --enable-theora                                         \
        --enable-pvm3                                           \
        --with-pvm3-libs=`ls -1d %{pvmdir}/lib/LINUX*`          \
        --with-pvm3-includes=%{pvmdir}/include                  \
        --enable-libdv                                          \
        --enable-libquicktime                                   \
        --enable-lzo                                            \
        --enable-a52                                            \
	--enable-a52-default-decoder                            \
        --enable-libxml2                                        \
        --enable-mjpegtools                                     \
        --enable-sdl                                            \
        --enable-imagemagick					\
	--enable-libmpeg3

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __documentation
make install DESTDIR=$RPM_BUILD_ROOT 
mv $RPM_BUILD_ROOT%{_docdir}/transcode/ __documentation
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README* TODO __documentation/*
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*.1*


%changelog
* Sun Aug 17 2008 David Juran <david@juran.se> - 1.0.5-5
- Build for rpmfusion

* Thu Jan 10 2008 David Juran <david@juran.se> - 1.0.5-1
- Upgrade to 1.0.5
- exchanve nuv patch to the one from HEAD
- drop dep-cleanup patch as it's no longer needed
- drop shared-libmpeg3 patch as it's no longer needed

* Sun Dec  9 2007 David Juran <david@juran.se> - 1.0.4-7
- Fix build error in nuv import

* Sun Dec  9 2007 David Juran <david@juran.se> - 1.0.4-6
- Rebuild for new libdvdread

* Tue Oct  16 2007 David Juran <david@juran.se> - 1.0.4-5
- use shared libmpeg3
- use a52dec default decoder as recommended
- License is GPLv2+

* Mon Oct  8 2007 David Juran <david@juran.se> - 1.0.4-4
- enable libmpeg3 for rpmfusion

* Sat Sep 29 2007 David Juran <david@juran.se> - 1.0.4-3
- Drop indirect dependencies

* Fri Sep 28 2007 David Juran <david@juran.se> - 1.0.4-2
- Get rid of glib dependency

* Mon Sep 24 2007 David Juran <david@juran.se> - 1.0.4-1
- updated to 1.0.4

* Fri Jun  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.0.3-1
- 1.0.3.
- Convert more docs to UTF-8.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.0.2-12
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.2-11
- Fix build with recent ffmpeg.
- Don't build with libfame.
- Specfile cleanup.

* Wed Jul 26 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.2-10
- Backport upstream changes for lzo2, require it.
- Apply upstream fix for compare filter never returning (#987).
- Avoid standard rpaths on lib64 archs.

* Wed Jul 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.2-4
- Rebuild for new ImageMagick (#1066).
- Fix some cosmetic rpmlint warnings.

* Sat Apr  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.2-3
- Rebuild for new ffmpeg.

* Tue Mar 14 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.2-2
- drop "0.lvn" from release

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Jan  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.2-0.lvn.2
- 1.0.2, libquicktime detection/build fixed upstream.
- Rebuild against new ffmpeg.
- Drop zero Epochs.
- Adapt to modular X.

* Sat Oct  8 2005 Dams <anvil[AT]livna.org> - 0:1.0.0-0.lvn.4
- Really rebuilding against new mjpegtools

* Mon Sep 26 2005 Thorsten Leemhuis <fedoral[AT]leemhuis.info> - 0:1.0.0-0.lvn.3
- Rebuilt against new mjpegtools

* Tue Aug 30 2005 Dams <anvil[AT]livna.org> - 0:1.0.0-0.lvn.2
- Rebuilt against new mjpegtools

* Thu Jul 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.0-0.lvn.1
- 1.0.0, no more SSE/gcc4 special casing needed, pvmlink patch applied upstream

* Tue Jul  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.0-0.lvn.0.4.rc1
- 1.0.0rc1, gcc4 patch no longer needed (but SSE/gcc4 problems persist).
- Add upstream patch to fix PVM linking.
- Clean up obsolete pre-FC2 support.

* Sat Jun 18 2005 Ville Skyttä <ville.skytta at iki.fi> 0:1.0.0-0.lvn.0.3.beta3
- Add "--without sse" rpmbuild option, needed with gcc4.

* Mon Jun 06 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.0.0-0.lvn.0.2.beta3
- Add gcc4.patch from plf-package with a small addition from cvs

* Sun May  1 2005 Ville Skyttä <ville.skytta at iki.fi> 0:1.0.0-0.lvn.0.1.beta3
- 1.0.0beta3.
- Enable PVM support.

* Sun Feb 20 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.14-0.lvn.5
- Requires: xvidcore.

* Thu Jan 13 2005 Dams <anvil[AT]livna.org> - 0:0.6.14-0.lvn.4
- buildroot -> RPM_BUILD_ROOT, for consistency

* Sun Jan 02 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:0.6.14-0.lvn.3
- Use --with-mod-path={_libdir}/transcode on x86_64
- use make install DESTDIR=%%{buildroot} instead makeinstall; adjust doc-install

* Thu Dec 23 2004 Dams <anvil[AT]livna.org> - 0:0.6.14-0.lvn.2
- Workaround for bad Magick-config

* Tue Dec 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.14-0.lvn.1
- Update to 0.6.14.
- Build with whatever the compiler supports; CPU features detected at runtime.
- Build with dependency tracking disabled.

* Thu Jul 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.12-0.lvn.5
- Remove ffmpeg-devel and libpostproc-devel build deps, transcode uses its
  internal ones.

* Tue Jul 27 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.12-0.lvn.4
- Make xvid4 (XviD 1.0.x) the default xvid export module.
- Convert man pages to UTF-8.

* Sun Jul 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.12-0.lvn.3
- Build with theora by default, use "--without theora" to disable.
- BuildRequire libexif-devel to work around yet another missing dependency
  in ImageMagick-devel.
- Replace hardcoded i686 BuildArch with i686+ ExclusiveArchs.
- Enable MMX and CMOV (also) when built on ia64 and x86_64.
- Enable SSE by default (only) on ia64 and x86_64; use "--with sse" to
  enable it on other archs.
- Rebuild with libfame 0.9.1.
- First cut at building with pvm support (incomplete, disabled).

* Sat May  8 2004 Dams <anvil[AT]livna.org> - 0:0.6.12-0.lvn.2
- Added url in Source0

* Fri Jan  9 2004 Dams <anvil[AT]livna.org> 0:0.6.12-0.lvn.1
- Updated to 0.6.12

* Sun Nov  9 2003 Dams <anvil[AT]livna.org> 0:0.6.11-0.lvn.1
- Updated to 0.6.11
- exclude -> rm

* Mon Sep 29 2003 Dams <anvil[AT]livna.org> 0:0.6.10-0.fdr.2
- BuildArch i686

* Tue Sep  9 2003 Dams <anvil[AT]livna.org> 0:0.6.10-0.fdr.1
- Updated to 0.6.10
- Updated doc files
- Dropped Patch1 and Patch2 (applied upstream)

* Thu Aug 14 2003 Dams <anvil[AT]livna.org> 0:0.6.9-0.fdr.1
- Updated to 0.6.9

* Thu Jul 31 2003 Dams <anvil[AT]livna.org> 0:0.6.8-0.fdr.2
- Applied filter_resample-segfault-fix-0.6.8 patch from upstream

* Tue Jul  8 2003 Dams <anvil[AT]livna.org> 0:0.6.8-0.fdr.1
- Updated to 0.6.8
- Removed glib/gtk+ version in BuildReqs

* Mon Jun  2 2003 Warren Togami <warren@togami.com> 0:0.6.7-0.fdr.3
- Remove smp_flags due to build failure

* Sun Jun  1 2003 Dams <anvil[AT]livna.org> 0:0.6.7-0.fdr.2
- Enabled text filter

* Sun Jun  1 2003 Dams <anvil[AT]livna.org> 0:0.6.6-0.fdr.1
- Updated to 0.6.7
- Updated BuildRequires

* Sun Jun  1 2003 Dams <anvil[AT]livna.org> 0:0.6.6-0.fdr.3
- Removed URL in Source0

* Thu May 22 2003 Dams <anvil[AT]livna.org> 0:0.6.6-0.fdr.2
- Changed URL in Source0

* Thu May 22 2003 Dams <anvil[AT]livna.org> 0:0.6.6-0.fdr.1
- Updated to 0.6.6
- Updated doc entry
- Slightly modified ifarch condition for nasm

* Sat May 10 2003 Dams <anvil[AT]livna.org> 0:0.6.4-0.fdr.2
- Re-added ffmpeg-devel BuildRequires
- Added libquicktime-devel libpostproc-devel and nasm BuildRequires

* Sat May 10 2003 Dams <anvil[AT]livna.org> 0:0.6.4-0.fdr.1
- Updated to 0.6.4
- Added missing BuildRequires
- exclude some ".la" files
- buildroot -> RPM_BUILD_ROOT

* Wed Apr 23 2003 Dams <anvil[AT]livna.org> 
- Initial build.
