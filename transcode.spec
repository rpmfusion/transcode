# TODO (sometime, maybe):
# - avifile (ick): http://avifile.sourceforge.net/
# - LoRS/IBP: http://loci.cs.utk.edu/

Name:           transcode
Version:        1.1.7
Release:        19%{?dist}
Summary:        Video stream processing tool

Group:          Applications/Multimedia
License:        GPLv2+
URL:            https://bitbucket.org/france/transcode-tcforge/overview
Source0:        https://bitbucket.org/france/transcode-tcforge/downloads/transcode-%{version}.tar.bz2
Patch0:         %{name}-pvmbin.patch
Patch1:         transcode-freetype.patch
Patch3:         transcode-1.0.4.external_dv.patch
Patch4:         transcode-1.1.6.header.patch
Patch5:         transcode-debian-697558.patch
#Debian patch series
#Patch22:         04_ffmpeg_options.patch
Patch23:         ac3-audio-track-number.patch
#Patch26:         07_libav9-preset.patch
#Patch27:         08_libav9-opt.patch
Patch31:         12_underlinkage.patch
# Gentoo / Archlinux patch series
Patch50:         transcode-1.1.7-ffmpeg.patch
Patch51:         transcode-1.1.7-ffmpeg-0.10.patch
Patch52:         transcode-1.1.7-ffmpeg-0.11.patch
Patch53:         transcode-1.1.7-preset-free.patch
Patch54:         transcode-1.1.7-libav-9.patch
Patch55:         transcode-1.1.7-preset-force.patch
Patch56:         transcode-1.1.7-ffmpeg2.patch
Patch57:         transcode-1.1.7-ffmpeg-2.4.patch
Patch58:         transcode-1.1.7-ffmpeg29.patch
Patch59:         transcode-ffmpeg3.patch


BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libdvdread-devel >= 4.1.3
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
BuildRequires:  ffmpeg-devel
BuildRequires:  mpeg2dec-devel >= 0.4.0
BuildRequires:  libtheora-devel
BuildRequires:  libXext-devel
BuildRequires:  libXv-devel
BuildRequires:  libXaw-devel
BuildRequires:  libXpm-devel
BuildRequires:  freetype-devel
%{?_with_faac:BuildRequires: faac-devel}
BuildRequires:  x264-devel
%ifarch %{ix86}
BuildRequires:  nasm
%endif
BuildRequires:  ImageMagick-devel
BuildRequires:  libmpeg3-devel
BuildRequires:  kernel-headers
BuildRequires:  libv4l-devel

# libtool + autotools for patch2, autoreconf
BuildRequires:  libtool


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
%patch1 -p1 -b .freetype
%patch3 -p1 -b .external_dv
%patch4 -p1 -b .header
%patch5 -p1 -b .strdup

rm filter/preview/dv_types.h
rm import/v4l/videodev.h
rm import/v4l/videodev2.h

%patch50 -p0
%patch51 -p0
%patch52 -p1
%patch53 -p1
%patch54 -p0
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1

#patch22 -p1 to see
%patch23 -p1
#patch26 -p1 to see
#patch27 -p1 to see
%patch31 -p1

mv configure.in configure.ac

%build
autoreconf -i
for file in docs/{man/*.1,export_mp2.txt,export_mpeg.txt,filter_dnr.txt} \
    AUTHORS ChangeLog README docs/README.vcd ; do
    iconv -f iso-8859-1 -t utf-8 $file > $file.utf8 && mv -f $file.utf8 $file
done

%configure \
        --disable-dependency-tracking                           \
        --disable-x86-textrels                                  \
        --with-x                                                \
        --enable-libavcodec                                     \
        --enable-libavformat                                    \
        --enable-libpostproc                                    \
        --enable-alsa                                           \
        --enable-freetype2                                      \
        --enable-xvid                                           \
        --enable-x264                                           \
        --enable-ogg                                            \
        --enable-vorbis                                         \
        --enable-theora                                         \
        --enable-libdv                                          \
        --enable-libquicktime                                   \
        --enable-a52                                            \
        --enable-lzo                                            \
  %{?_with_faac:--enable-faac}                                  \
        --enable-libxml2                                        \
        --enable-mjpegtools                                     \
        --enable-sdl                                            \
        --enable-imagemagick                                    \
%ifarch %{ix86}
        --enable-pv3                                            \
%endif
%ifarch %{ix86} x86_64
        --enable-nuv                                            \
%endif
        --enable-deprecated                 \
    --enable-v4l                        \
    --enable-libv4l2                    \
    --enable-libv4lconvert                  \
    --enable-libmpeg2                   \
    --enable-libmpeg2convert

# arch linux suggestion:
#    --disable-sse --disable-sse2 --disable-altivec --enable-mmx

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%files
%doc AUTHORS README* TODO
%license COPYING
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*.1*
%{_docdir}/transcode/


%changelog
* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.1.7-19
- Rebuild for ffmpeg update

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.1.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Sep 17 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.1.7-17
- Redo patch

* Sat Sep 17 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.1.7-16
- Add patch

* Sat Sep 17 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.1.7-15
- Patch to rename avcodec_encode_audio to avcodec_encode_audio2 rfbz#4262

* Mon Feb 29 2016 Sérgio Basto <sergio@serjux.com> - 1.1.7-14
- Add all archlinux/gentoo patches make it compatible with lastest ffmpeg.
- Build with ffmpeg-devel and not ffmpeg-compat.
- Remove PVM3 because was retired in F23.
- Add license tag.
- Some cleanups.
- Add 2 pacthes from Debian.
- Add transcode-debian-697558.patch (rfbz #1337)

* Sun May 03 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-13
- Disable pvm3 on arm - rhbz#986677

* Fri Jul 25 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1.7-12
- Add patch to fix build with freetype 2.5

* Thu Jul 24 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1.7-11
- Rebuild for new ImageMagick

* Sun Nov 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-10
- Rebuilt for mjpegtools update to 2.1.0

* Tue Apr 16 2013 Orion Poplawski <orion@cora.nwra.com> - 1.1.7-9
- Rebuild for libjpeg soname revert

* Fri Nov 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-8
- Rebuilt for x264

* Sat May 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-7
- Fix for ffmpeg oldabi

* Thu May 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-6
- Switch to ffmpeg-compat

* Tue Apr 10 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-5
- Rebuilt

* Fri Mar 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-4
- Disable FFmpeg libpostproc 

* Mon Feb 27 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-3
- Rebuilt for x264/FFmpeg

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-1
- Update to 1.1.7

* Wed Nov 09 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.6-1
- Update to 1.1.6

* Mon Sep 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.5-9
- Rebuilt for FFmpeg-0.8
- Add patch from Rathann

* Wed Aug 24 2011 David Juran <david@juran.se> - 1.1.5-8
- Rebuild for new mjpegtools (Bz 1906)

* Sun Jun 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.5-7
- Fix support for v4l - rfbz#1824

* Wed Apr 20 2011 David Juran <david@juran.se> - 1.1.5-6
- Disable v4l, Bz 1700

* Thu Sep 30 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.5-5
- rebuilt for ImageMagick

* Fri May 21 2010 David Juran <david@juran.se> - 1.1.5-4
- Rebuild for new ImageMagick (Bz1188)

* Sat Jan 30 2010 David Juran <david@juran.se> - 1.1.5-3
- fix crash when using no video with the ogg exporter (Bz 1060)

* Sat Nov  7 2009 David Juran <david@juran.se> - 1.1.5-2
- explicitly (re-)enabled libmpeg2 support (Bz 922)

* Sun Nov  1 2009 David Juran <david@juran.se> - 1.1.5-1
- upgrade to 1.1.5

* Sat Oct 17 2009 kwizart < kwizart at gmail.com > - 1.1.4-2
- Conditionalize faac (moved to nonfree).

* Thu Aug 27 2009 David Juran <david@juran.se> - 1.1.4-1
- update to 1.1.4

* Sat Jul 25 2009 David Juran <david@juran.se> - 1.1.3-2
- Fix build problem

* Tue Jul 21 2009 David Juran <david@juran.se> - 1.1.3-1
- Update to 1.1.3

* Sun Jul  5 2009 David Juran <david@juran.se> - 1.1.2-1
- Update to 1.1.2
- Fix rpmlint errors

* Sat Jul  4 2009 David Juran <david@juran.se> - 1.1.1-6
- Fix TEXTREL (Bz 658)
- Update URL

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.1.1-5
- rebuild for new F11 features

* Thu Mar 12 2009 kwizart < kwizart at gmail.com > - 1.1.1-4
- Rebuild for ImageMagick
- Remove internal videodev.h videodev2.h (btw v4l1 is deprecated).
- Re-enable faac pvm3 xvidcore x264
- Enable pv3 only for %%{ix86}
- Enable NuppelVideo only for %%{ix86} and x86_64

* Sun Feb 22 2009 David Juran <david@juran.se> - 1.1.1-1
- upgrade to 1.1.1

* Fri Jan 23 2009 David Juran <david@juran.se> - 1.1.0-3
- thick fingers

* Fri Jan 23 2009 David Juran <david@juran.se> - 1.1.0-2
- enable deprecated (broken?) features

* Sun Jan 18 2009 David Juran <david@juran.se> - 1.1.0-1
- upgrade to 1.1.0

* Tue Dec 16 2008 kwizart < kwizart at gmail.com > - 1.0.7-3
- Re-enable the use of the default asm options
  (to be tested on x86)

* Thu Dec 11 2008 kwizart < kwizart at gmail.com > - 1.0.7-2
- Fix autoreconf use
- Fix CFLAGS
- Fix asm options

* Sun Nov 16 2008 David Juran <david@juran.se> - 1.0.7-1
- upgrade to 1.0.7

* Mon Nov 10 2008 David Juran <david@juran.se> - 1.0.6-3
- drop libdvdread patch

* Sat Aug  9 2008 David Juran <david@juran.se> - 1.0.6-2
- bump release for rpmfusion

* Fri Aug 8 2008 <david@juran.se> - 1.0.6-1
- upgraded to 1.0.6
- fix rpmlint warnings

* Thu Jul  3 2008  <david@juran.se> - 1.0.5-3
- updated for new ffmpeg directory layout
- updated for new libdvdread directory layout
- libMagick split in libMagicCore and libMagicWand

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
