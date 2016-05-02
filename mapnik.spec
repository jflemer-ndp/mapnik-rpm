%define major 3
%define libname lib%{name}2_%{major}
%define develname %{name}-devel

Name:      mapnik
Version:   3.0.10
Release:   2.ndp1
Summary:   Free Toolkit for developing mapping applications
Group:     Geography
License:   LGPLv2+
URL:       http://mapnik.org/
Source0:   http://mapnik.s3.amazonaws.com/dist/v%{version}/%{name}-v%{version}.tar.bz2
Source1:   mapnik-data.license
Source2:   no_date_footer.html
Source3:   viewer.desktop
Patch0:    mapnik-v3.0.6-linking.patch
BuildRequires: postgresql-devel 
BuildRequires: postgis
BuildRequires: pkgconfig
BuildRequires: gdal-devel 
BuildRequires: proj-devel 
BuildRequires: agg-devel
BuildRequires: scons 
BuildRequires: doxygen 
BuildRequires: desktop-file-utils
BuildRequires: libltdl-devel 
BuildRequires: qt4-devel > 4.3
BuildRequires: libxml2-devel 
BuildRequires: boost-devel
BuildRequires: libicu-devel
BuildRequires: libtiff-devel 
BuildRequires: libjpeg-devel 
BuildRequires: libpng-devel
BuildRequires: cairomm-devel 
BuildRequires: python-cairo-devel
BuildRequires: freetype2-devel
BuildRequires: python-devel
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(libwebp)
Requires:  fonts-ttf-dejavu
Requires: %{libname} = %{version}-%{release}
ExcludeArch: %{ix86}


%description
Mapnik is a Free Toolkit for developing mapping applications.
It's written in C++ and there are Python bindings to
facilitate fast-paced agile development. It can comfortably
be used for both desktop and web development, which was something
I wanted from the beginning.

Mapnik is about making beautiful maps. It uses the AGG library
and offers world class anti-aliasing rendering with subpixel
accuracy for geographic data. It is written from scratch in
modern C++ and doesn't suffer from design decisions made a decade
ago. When it comes to handling common software tasks such as memory
management, filesystem access, regular expressions, parsing and so
on, Mapnik doesn't re-invent the wheel, but utilises best of breed
industry standard libraries from boost.org 

%package -n %{libname}
Summary: Mapnik is a Free toolkit for developing mapping applications
Group: System/Libraries

%description -n %{libname}
Mapnik is a Free Toolkit for developing mapping applications.
It's written in C++ and there are Python bindings to
facilitate fast-paced agile development. It can comfortably
be used for both desktop and web development, which was something
I wanted from the beginning.

Mapnik is about making beautiful maps. It uses the AGG library
and offers world class anti-aliasing rendering with subpixel
accuracy for geographic data. It is written from scratch in
modern C++ and doesn't suffer from design decisions made a decade
ago. When it comes to handling common software tasks such as memory
management, filesystem access, regular expressions, parsing and so
on, Mapnik doesn't re-invent the wheel, but utilises best of breed
industry standard libraries from boost.org


%package -n %{develname}
Summary: Mapnik is a Free toolkit for developing mapping applications
Group: Development/C++
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %{name}-devel

%description -n %{develname}
Mapnik is a Free Toolkit for developing mapping applications.
It's written in C++ and there are Python bindings to
facilitate fast-paced agile development. It can comfortably
be used for both desktop and web development, which was something
I wanted from the beginning.

Mapnik is about making beautiful maps. It uses the AGG library
and offers world class anti-aliasing rendering with subpixel
accuracy for geographic data. It is written from scratch in
modern C++ and doesn't suffer from design decisions made a decade
ago. When it comes to handling common software tasks such as memory
management, filesystem access, regular expressions, parsing and so
on, Mapnik doesn't re-invent the wheel, but utilises best of breed
industry standard libraries from boost.org

%package python
Summary:  Python bindings for the Mapnik spatial visualization library
License:  GPLv2+
Group:    Development/Python
Requires: %{name} = %{version}-%{release}
Requires: python-imaging python-lxml

%description python
Language bindings to enable the Mapnik library to be used from python

%package utils
License:  GPLv2+
Summary:  Utilities distributed with the Mapnik spatial visualization library
Group:    Geography
Requires: %{name} = %{version}-%{release}

%description utils
Miscellaneous utilities distributed with the Mapnik spatial visualization
library

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1


rm -fr demo

%build

# fix build flags
#sed -i -e "s|common_cxx_flags = .-D\%s|common_cxx_flags = \'-D\%s %optflags |g" SConstruct

%configure    DESTDIR=%{buildroot} \
              PREFIX=/usr \
              LIBDIR_SCHEMA=%{buildroot}/%{_libdir} \
              THREADING=multi \
              XMLPARSER=libxml2 \
              GDAL_INCLUDES=%{_includedir}/gdal \
              CUSTOM_CFLAGS="%optflags" \
              CUSTOM_CXXFLAGS="%optflags" \
              CUSTOM_LDFLAGS="%ldflags" \
              INTERNAL_LIBAGG=False \
              SYSTEM_FONTS=%{_datadir}/fonts \
              DEMO=False

%make

%install

%make_install 

# get rid of fonts use external instead
rm -rf %{buildroot}%{_libdir}/%{name}/fonts

# install more utils
mkdir -p %{buildroot}%{_bindir}
#install -p -m 755 demo/viewer/viewer %{buildroot}%{_bindir}/
#install -p -m 755 utils/stats/mapdef_stats.py %{buildroot}%{_bindir}/
#install -p -m 644 %{SOURCE1} demo/data/

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
includedir=%{_includedir}

Name: %{name}
Description: Free Toolkit for developing mapping applications
Version: %{version}
Libs: -lmapnik
Cflags: -I${includedir}/%{name} -I${includedir}/agg
EOF

mkdir -p %{buildroot}%{_datadir}/pkgconfig/
install -p -m 644 %{name}.pc %{buildroot}%{_datadir}/pkgconfig/

# install desktop file
#desktop-file-install --vendor="mandriva" \
 #       --dir=%{buildroot}%{_datadir}/applications %{SOURCE3}

%check

# export test enviroment
export PYTHONPATH=$PYTHONPATH:%{buildroot}%{python_sitearch}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH%{buildroot}%{_libdir}

pushd test/
./run ||:
popd

%files
%doc AUTHORS.md COPYING CHANGELOG.md
%{_libdir}/%{name}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{develname}
%{_bindir}/mapnik-config
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_datadir}/pkgconfig/%{name}.pc

%files python


%files utils
%{_bindir}/shapeindex
%{_bindir}/mapnik-render
# %%{_bindir}/upgrade_map_xml.py
#%%{_bindir}/nik2img
%{_bindir}/mapnik-index 
%{_libdir}/libmapnik-json.a
%{_libdir}/libmapnik-wkt.a


%changelog
* Sun May 01 2016 James E. Flemer <james.flemer@ndpgroup.com> 3.0.10-2.ndp1
- Replace Mageia macros

* Sun Mar 06 2016 spuhler <spuhler> 3.0.10-1.mga6
+ Revision: 986704
- upgrade to vers 3.0.10

* Tue Dec 15 2015 spuhler <spuhler> 3.0.9-1.mga6
+ Revision: 910589
- added file   /usr/bin/mapnik-render
- removed missing file
- upgrade to vers. 3.0.9

* Wed Oct 21 2015 spuhler <spuhler> 3.0.6-1.mga6
+ Revision: 893216
- added "/" tp %%{_bindir}/mapnik-index  in files section
- fixed ExcludeArch:    %%ix86
- removed CXX=clang++
- build for x86-_64 only as 32 bit doesn't build
- added new file %%{_bindir}mapnik-index
- removed geojson.patch
  * fixed upstream
- upgrade to vers. 3.0.6
- bumped rel because 64bit has built
- use make instead of %%make -j1
- bumped rel because 64bit did build
- reduced %%make to 1 CPU to save memory on 32 bit
- added back files after finding them
-- added prefix to %%configure
   * it's not taking it from the macro
- commented out a couple more non-existent files
- commented out a couple more none-existent files
- commented out the none existing mapdef_stats.py
- use %%make instead of make to spped up the build.
- added %%{buildroot}in before /%%{_libdir} LIBDIR_SCHEMA=%%{buildroot}/%%{_libdir}
  * it's a try
- added DESTDIR=%%{buildroot}  to configure
  * otherwise it wants to install to /
- added option to configure
- changed patch0 from upstream
  * finds icu
- using make and %%make_install instead of scons and scons install
  * seems to use less RAM
- adding new geojson.patch from upstream
- added icu patch from upstream
- upgrade to vers. 3.0.5
- included our icu version in boost patch
- fixed fontdir in configure
- added boost-1.59.0 patch
- added export CPPFLAGS=-DBOOST_ERROR_CODE_HEADER_ONLY
- added BuildRequires: postgis
- made it multi-cpu build to speed up the build
- adde BuildRequires: pkgconfig (icu...
- added BuildRequires: pkgconfig(harfbuzz)

  + fwang <fwang>
    - link stdc++
    - link stdc++
    - fix linking

  + pterjan <pterjan>
    - Build with clang++ as g++ needs more than 4GB memory which fails on i586

  + barjac <barjac>
    - new major 3
    - change tests dir and script name
    - BR libwebp
    - dont try to install missing bin file

  + daviddavid <daviddavid>
    - rebuild for new boost-1.58.0

* Fri Jul 24 2015 cjw <cjw> 2.2.0-11.mga6
+ Revision: 856804
- rebuild for icu 55

* Tue Nov 25 2014 cjw <cjw> 2.2.0-10.mga5
+ Revision: 798964
- rebuild against postgresql9.4

* Wed Oct 15 2014 umeabot <umeabot> 2.2.0-9.mga5
+ Revision: 748187
- Second Mageia 5 Mass Rebuild

* Sat Sep 27 2014 tv <tv> 2.2.0-8.mga5
+ Revision: 727110
- rebuild for missing pythoneggs deps

* Tue Sep 16 2014 umeabot <umeabot> 2.2.0-7.mga5
+ Revision: 682163
- Mageia 5 Mass Rebuild

* Sat May 31 2014 pterjan <pterjan> 2.2.0-6.mga5
+ Revision: 628321
- Rebuild for new Python

* Sat Apr 05 2014 wally <wally> 2.2.0-5.mga5
+ Revision: 611884
- rebuild for new icu

* Sat Feb 08 2014 barjac <barjac> 2.2.0-4.mga5
+ Revision: 586735
- rebuild against boost-1.55

* Mon Oct 21 2013 umeabot <umeabot> 2.2.0-3.mga4
+ Revision: 537690
- Mageia 4 Mass Rebuild

* Fri Sep 27 2013 fwang <fwang> 2.2.0-2.mga4
+ Revision: 487454
- rebuild for icu 52

* Sat Aug 03 2013 fwang <fwang> 2.2.0-1.mga4
+ Revision: 462909
- update file list
- link with cairo
- add libs
- fix linkage of dl
- do not build demo prog
- drop unused command
- new version 2.2.0

* Mon Jul 08 2013 fwang <fwang> 2.1.0-8.mga4
+ Revision: 451284
- rebuild for new boost

* Sun Jun 02 2013 fwang <fwang> 2.1.0-7.mga4
+ Revision: 435461
- rebuild for new libpng

* Sun May 26 2013 fwang <fwang> 2.1.0-6.mga4
+ Revision: 428043
- rebuild for icu

* Thu Apr 11 2013 barjac <barjac> 2.1.0-5.mga3
+ Revision: 409500
- rebuild for boost-1.53

* Wed Mar 27 2013 barjac <barjac> 2.1.0-4.mga3
+ Revision: 405843
- fix build with boost-1.53

* Sat Jan 12 2013 umeabot <umeabot> 2.1.0-3.mga3
+ Revision: 359408
- Mass Rebuild - https://wiki.mageia.org/en/Feature:Mageia3MassRebuild

* Thu Dec 20 2012 fwang <fwang> 2.1.0-2.mga3
+ Revision: 332955
- rebuild for new boost

* Sat Nov 10 2012 fwang <fwang> 2.1.0-1.mga3
+ Revision: 316802
- correct link flags
- more linkage fix
- fix typo
- more linkage fix
- fix linkage
- update build switch
- update file list
- update file list
- drop old patch
- new version 2.1.0
- rebuild for updated icu

* Tue Nov 06 2012 fwang <fwang> 2.0.1-4.mga3
+ Revision: 314776
- rebuild for new icu

* Wed Oct 03 2012 malo <malo> 2.0.1-3.mga3
+ Revision: 302538
- update RPM group

* Tue Jul 31 2012 fwang <fwang> 2.0.1-2.mga3
+ Revision: 276581
- use default boos-filesyste-version
- rebuild for new boost

* Wed Jun 06 2012 obgr_seneca <obgr_seneca> 2.0.1-1.mga3
+ Revision: 256219
- fixed file names
- fixed path to extracted source
- fixed doc files
- New version 2.0.1

* Wed May 30 2012 fwang <fwang> 2.0.0-3.mga3
+ Revision: 249633
- rebuild for new icu

* Sun Dec 25 2011 fwang <fwang> 2.0.0-2.mga2
+ Revision: 187468
- rebuild for new libtiff

* Sun Dec 11 2011 fwang <fwang> 2.0.0-1.mga2
+ Revision: 180567
- update file list
- update file list
- new version 2.0.0

* Mon Nov 28 2011 fwang <fwang> 0.7.1-10.mga2
+ Revision: 173470
- rebuild for new boost

* Sun Sep 18 2011 fwang <fwang> 0.7.1-9.mga2
+ Revision: 144950
- fix build with latest libpng15
- rebuild for new mapnik
- rebuild for new boost

* Wed Jun 22 2011 fwang <fwang> 0.7.1-7.mga2
+ Revision: 111884
- rebuild for new boost

* Mon Jun 20 2011 fwang <fwang> 0.7.1-6.mga2
+ Revision: 110337
- rebuild for new icu

* Wed May 04 2011 ennael <ennael> 0.7.1-5.mga1
+ Revision: 94769
- fix BR
- /bin/bash: q : commande introuvable
- imported package mapnik

