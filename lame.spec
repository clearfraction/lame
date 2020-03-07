# spec file for package lame
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2012 Pascal Bleser &lt;&gt;
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An &quot;Open Source License&quot; is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.



%define sover 0
Name:           lame
Version:        3.100
Release:        2
Summary:        The LAME MP3 encoder
License:        LGPL-2.0+
Group:          Productivity/Multimedia/Sound/Editors and Convertors
Url:            http://lame.sourceforge.net/
Source:         http://prdownloads.sourceforge.net/lame/lame-%{version}.tar.gz     
#Source99:       lame-rpmlintrc
#Source1000:     baselibs.conf
Patch1:         lame-field-width-fix.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  ncurses-dev
BuildRequires:  pkg-config
BuildRequires:  nasm
BuildRequires:  pkgconfig(gtk+-2.0)
Requires:       libmp3lame%{sover} >= %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build


%description
LAME is an educational tool to be used for learning about MP3 encoding.
The goal of the LAME project is to use the open source model to improve the
psycho acoustics, noise shaping and speed of MP3.
Another goal of the LAME project is to use these improvements for the basis of
a patent free audio compression codec for the GNU project.

%package doc
Summary:        Documentation for the LAME MP3 encoder
Group:          Productivity/Multimedia/Sound/Editors and Convertors
Requires:       %{name} = %{version}

%description doc
LAME is an encoder that converts audio to the MP3 file format. It has
an improved psychoacoustic model and performs well in codec listening
tests.

%package -n libmp3lame%{sover}
Summary:        The LAME MP3 encoder library
Group:          System/Libraries

%description -n libmp3lame%{sover}
LAME is an encoder that converts audio to the MP3 file format. It has
an improved psychoacoustic model and performs well in codec listening
tests.

%package -n libmp3lame-dev
Summary:        Development files for the LAME MP3 encoder
Group:          Development/Libraries/C and C++
Requires:       libmp3lame%{sover} = %{version}

%description -n libmp3lame-dev
Contains the header files for use with LAME's encoding library.

%package -n lame-mp3rtp
Summary:        MP3 Encoder for RTP Streaming
Group:          Productivity/Multimedia/Sound/Editors and Convertors
Requires:       libmp3lame%{sover} >= %{version}

%description -n lame-mp3rtp
LAME is an encoder that converts audio to the MP3 file format. It has
an improved psychoacoustic model and performs well in codec listening
tests.

This package includes "mp3rtp", an MP3 encoder with RTP streaming of the output.


%prep
%setup -q
%patch1 -p1

%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export FCFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export FFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export CXXFLAGS="$CXXFLAGS -O3 -ffat-lto-objects -flto=4 "
LIBS="-lm" \
CFLAGS="%{optflags}" \
%configure \
    --enable-nasm \
    --enable-decoder \
    --disable-debug \
    --enable-mp3rtp \
    --with-fileio=lame \
    --enable-dynamic-frontends \
    --disable-rpath \
    --disable-static

make %{?_smp_mflags} pkgdocdir=%{_defaultdocdir}/%{name}/

%check
make test

%install
make install pkgdocdir=%{_defaultdocdir}/%{name}/ DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/libmp3lame.la

for f in ChangeLog README TODO USAGE; do
    install -m0644 "$f" "%{buildroot}%{_defaultdocdir}/%{name}/"
done

%post   -n libmp3lame%{sover} -p /usr/bin/ldconfig

%postun -n libmp3lame%{sover} -p /usr/bin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/lame
%{_mandir}/man1/lame.1*

%files doc
%defattr(-,root,root)
%{_defaultdocdir}/%{name}

%files -n libmp3lame%{sover}
%defattr(0644,root,root,0755)
%doc COPYING LICENSE
%{_libdir}/libmp3lame.so.%{sover}
%{_libdir}/libmp3lame.so.%{sover}.*

%files -n libmp3lame-dev
%defattr(-,root,root)
%doc API HACKING STYLEGUIDE
%{_includedir}/lame/
%{_libdir}/libmp3lame.so

%files -n lame-mp3rtp
%defattr(-,root,root)
%{_bindir}/mp3rtp

%changelog
