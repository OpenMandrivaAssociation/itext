%{?_javapackages_macros:%_javapackages_macros}
%if ! 0%{?rhel}
%global with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}
%else
%global with_gcj 0
%endif
%global alternate_name iText

Summary:          A Free Java-PDF library
Name:             itext
Version:          2.1.7
Release:          21.0%{?dist}
#src/toolbox/com/lowagie/toolbox/Versions.java is MPLv1.1 or MIT
#src/toolbox/com/lowagie/toolbox/plugins/XML2Bookmarks.java is MPLv1.1 or LGPLv2+
#src/rups/com/lowagie/rups/Rups.java is LGPLv2+
#src/rups/com/lowagie/rups/view/icons/ are under CC-BY
#src/core/com/lowagie/text/xml/XmlDomWriter.java is under ASL 2.0
#src/core/com/lowagie/text/pdf/LZWDecoder.java is under BSD
#src/core/com/lowagie/text/pdf/fonts/cmaps/CodespaceRange.java is under BSD
#src/core/com/lowagie/text/pdf/fonts are under APAFML
#src/core/com/lowagie/text/pdf/codec/TIFFConstants.java is under libtiff
License:          (LGPLv2+ or MPLv1.1) and ASL 2.0 and BSD and LGPLv2+ and (MPLv1.1 or MIT) and CC-BY and APAFML and libtiff
URL:              http://www.lowagie.com/iText/

Source0:          http://downloads.sourceforge.net/itext/iText-src-%{version}.tar.gz
Source2:          http://repo2.maven.org/maven2/com/lowagie/itext/%{version}/itext-%{version}.pom
Source3:          itext-rups.sh
Source4:          itext-rups.desktop
Source5:          itext-toolbox.sh
Source6:          itext-toolbox.desktop
# cvs -d :pserver:anonymous@dev.eclipse.org:/cvsroot/tools checkout -r v2_1_7 org.eclipse.orbit/com.lowagie.text/META-INF/MANIFEST.MF
# tar cf export-manifest.tar org.eclipse.orbit/com.lowagie.text/META-INF/MANIFEST.MF
Source7:          export-manifest.tar
Source8:          http://repo2.maven.org/maven2/com/lowagie/itext-rtf/%{version}/itext-rtf-%{version}.pom
Source9:          http://repo2.maven.org/maven2/com/lowagie/itext-rups/%{version}/itext-rups-%{version}.pom
Patch1:           itext-2.1.5-pdftk.patch

# The iText POM specifies that it requires bouncycastle's "jdk14" JARs
# but we have "jdk16".
Patch2:           itext-2.1.7-fixpomforbc.patch
# Maven's Doxia plugin explicitly requires these XML output interfaces
# of iText.  They were removed in iText 1.4.4 [1].  iText versions prior
# to 1.5.x had questionable licensing [2] so rather than try to create
# an itext1 package, I have forward-ported these classes.  The doxia
# developers have told me on IRC on 2009-08-27 that the iText dependency
# will likely be deprecated meaning we won't have to keep these forever.
#
# I've opened a bug with iText:
#
# https://sourceforge.net/tracker/?func=detail&aid=2846427&group_id=15255&atid=365255
#
# and commented on the Doxia but related to this:
#
# http://jira.codehaus.org/browse/DOXIA-53
#
# -- Andrew Overholt, 2009-08-28
#
# [1]
# http://www.1t3xt.com/about/history.php?branch=history.10&node=14
# [2]
# https://bugzilla.redhat.com/show_bug.cgi?id=236309
Patch3:           itext-xmloutput.patch
# Use orbit manifest so the manifest exports packages properly.
Patch4:           itext-manifest.patch
Patch5:           itext-remove-unmappable.patch

BuildRequires:    ant
BuildRequires:    bouncycastle-tsp >= 1.46-4
BuildRequires:    desktop-file-utils
BuildRequires:    dom4j
%if 0%{?fedora}
BuildRequires:    ImageMagick
%else
BuildRequires:    imagemagick
%endif
BuildRequires:    pdf-renderer
BuildRequires:    java-devel >= 1.7
BuildRequires:    jpackage-utils
%if %{with_gcj}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
Requires:         java-1.5.0-gcj
%else
BuildArch:        noarch
%endif
Provides:         %{alternate_name} == %{version}-%{release}
Requires:         %{name}-core = %{version}-%{release}

%description
iText is a library that allows you to generate PDF files on the fly. The iText
classes are very useful for people who need to generate read-only, platform
independent documents containing text, lists, tables and images. The library is
especially useful in combination with Java(TM) technology-based Servlets: The
look and feel of HTML is browser dependent; with iText and PDF you can control
exactly how your servlet's output will look.

%package core
Summary:          The core iText Java-PDF library

BuildArch:        noarch
Requires:         bouncycastle-tsp >= 1.46-4
Requires:         java >= 1.5
Requires:         jpackage-utils
Obsoletes:        itext < 2.1.7-12

%description core
The core package contains the main iText library and the related maven POM
files.

%package rtf
Summary:        Library to output Rich Text Files

BuildArch:      noarch
License:        MPLv1.1 or LGPLv2+
Requires:       %{name}-core = %{version}-%{release}

%description rtf
The RTF package is an extension of the iText library and allows iText to output
Rich Text Files in addition to PDF files. These files can then be viewed and
edited with RTF viewers such as OpenOffice.org Writer.

%package rups
Summary:        Reading/Updating PDF Syntax

BuildArch:      noarch
License:        LGPLv2+ and CC-BY
Requires:       %{name}-core = %{version}-%{release}
Requires:       dom4j
Requires:       pdf-renderer

%description rups
iText RUPS is a tool that combines SUN's PDF Renderer (to view PDF documents),
iText's PdfReader (to inspect the internal structure of a PDF file), and
iText's PdfStamper to manipulate a PDF file.

%package toolbox
Summary:        Some %{alternate_name} tools

BuildArch:      noarch
License:        MPLv1.1 or MIT
Requires:       %{name} = %{version}-%{release}
Requires:       java >= 1.5

%description toolbox
iText is a free open source Java-PDF library released on SF under the MPL/LGPL;
iText comes with a simple GUI: the iText toolbox. The original developers of
iText want to publish this toolbox as a separate project under the more
permissive MIT license. This is a utility that allows you to use a number of
iText tools.

%package javadoc
Summary:        Javadoc for %{alternate_name}

BuildArch:      noarch
Requires:       %{name}-core = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
API documentation for the %{alternate_name} package.


%prep
%setup -q -c -T -a 0
%patch1 -p1 -b .pdftk
cp -pr %{SOURCE2} JPP-itext.pom
%patch2 -p0 -b .fixpomforbc
%patch3 -p0 -b .xmloutput
%patch4 -p0
%patch5 -p0

cp -pr %{SOURCE8} JPP-%{name}-rtf.pom
cp -pr %{SOURCE9} JPP-%{name}-rups.pom

for p in JPP-%{name}-rtf.pom JPP-%{name}-rups.pom ; do
%pom_remove_dep bouncycastle:bcmail-jdk14 ${p}
%pom_add_dep org.bouncycastle:bcmail-jdk16 ${p}
%pom_remove_dep bouncycastle:bcprov-jdk14 ${p}
%pom_add_dep org.bouncycastle:bcprov-jdk16 ${p}
%pom_remove_dep bouncycastle:bctsp-jdk14 ${p}
%pom_add_dep org.bouncycastle:bctsp-jdk16 ${p}
done

# move manifest to build area
tar -xf %{SOURCE7}
mv org.eclipse.orbit/com.lowagie.text/META-INF/MANIFEST.MF src/ant

# Remove preshipped binaries
find . -name "*.jar" -exec rm {} \;

# Fix encoding issues
sed 's/\r//' src/rups/com/lowagie/rups/view/icons/copyright_notice.txt > tmpfile
touch -r src/rups/com/lowagie/rups/view/icons/copyright_notice.txt tmpfile
mv -f tmpfile src/rups/com/lowagie/rups/view/icons/copyright_notice.txt

mkdir lib
build-jar-repository -s -p lib bcprov bcmail bctsp pdf-renderer dom4j

# Remove jdk & version numbers from classpath entries
for file in src/ant/{*,.ant*}; do
 for jarname in bcmail bcprov bctsp dom4j; do
  sed -i "s|$jarname-.*\.jar|$jarname.jar|" $file
 done
done

# Setting debug="on" on javac part of the build script.
sed -i 's|destdir|debug="on" destdir|g' src/ant/compile.xml
sed -i 's|debug="true"||g' src/ant/compile.xml

# Specify encoding, otherwise javadoc blows
sed -i 's|author|Encoding="ISO-8859-1" author|' src/ant/site.xml
# and set max memory higher or we run out
sed -i 's|maxmemory="128m"|maxmemory="512m"|' src/ant/site.xml

%build
export CLASSPATH=$(build-classpath bcprov bcmail bctsp pdf-renderer dom4j)
pushd src
 ant -Ditext.jdk.core=1.5 \
     -Ditext.jdk.rups=1.5 \
     -Ditext.jdk.toolbox=1.5 \
     jar jar.rups jar.rtf jar.toolbox javadoc
popd

%install
# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p lib/iText.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p lib/iText-rtf.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-rtf-%{version}.jar
cp -p lib/iText-rups.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-rups-%{version}.jar
cp -p lib/iText-toolbox.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-toolbox-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do \
      ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
# rups stuff
install -pm 755 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/%{name}-rups
desktop-file-install \
      --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
      %{SOURCE4}

# toolbox stuff
install -pm 755 %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/%{name}-toolbox
desktop-file-install \
      --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
      %{SOURCE6}

# icon for rups and toolbox
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
convert -resize 128x128 src/toolbox/com/lowagie/toolbox/1t3xt.gif %{name}.png
cp -a %{name}.png \
      $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/%{name}-rups.png
cp -a %{name}.png \
      $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/%{name}-toolbox.png

%if %{with_gcj}
 RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-indirect-classes" %{_bindir}/aot-compile-rpm
%endif
      
# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Install the pom
install -dm 755 $RPM_BUILD_ROOT%{_mavenpomdir}
cp -pr JPP-itext.pom $RPM_BUILD_ROOT%{_mavenpomdir}
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "itext:itext"

cp -pr JPP-%{name}-rtf.pom $RPM_BUILD_ROOT%{_mavenpomdir}
%add_maven_depmap JPP-%{name}-rtf.pom %{name}-rtf.jar -f rtf
cp -pr JPP-%{name}-rups.pom $RPM_BUILD_ROOT%{_mavenpomdir}
%add_maven_depmap JPP-%{name}-rups.pom %{name}-rups.jar  -f rups

%post
%if %{with_gcj}
 if [ -x %{_bindir}/rebuild-gcj-db ]
 then
  %{_bindir}/rebuild-gcj-db
 fi
%endif

%postun
%if %{with_gcj}
 if [ -x %{_bindir}/rebuild-gcj-db ]
 then
  %{_bindir}/rebuild-gcj-db
 fi
%endif

%post rups
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun rups
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans rups
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post toolbox
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun toolbox
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans toolbox
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%if %{with_gcj}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/%{name}-%{version}.*
# We only need the aot bits for the core jar
%exclude %{_libdir}/gcj/%{name}/%{name}-rtf-%{version}.*
%exclude %{_libdir}/gcj/%{name}/%{name}-rups-%{version}.*
%exclude %{_libdir}/gcj/%{name}/%{name}-toolbox-%{version}.*
%endif

%files core
%doc build/bin/com/lowagie/text/{apache_license,lgpl,misc_licenses,MPL-1.1}.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_mavenpomdir}/JPP-itext.pom
%{_mavendepmapfragdir}/%{name}

%files rtf
%{_javadir}/%{name}-rtf.jar
%{_javadir}/%{name}-rtf-%{version}.jar
%{_mavenpomdir}/JPP-%{name}-rtf.pom
%{_mavendepmapfragdir}/%{name}-rtf

%files rups
%doc src/rups/com/lowagie/rups/view/icons/copyright_notice.txt
%{_javadir}/%{name}-rups.jar
%{_javadir}/%{name}-rups-%{version}.jar
%{_mavenpomdir}/JPP-%{name}-rups.pom
%{_mavendepmapfragdir}/%{name}-rups
%{_bindir}/%{name}-rups
%{_datadir}/applications/%{name}-rups.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}-rups.png

%files toolbox
%doc src/toolbox/com/lowagie/toolbox/tools.txt
%{_javadir}/%{name}-toolbox.jar
%{_javadir}/%{name}-toolbox-%{version}.jar
%{_bindir}/%{name}-toolbox
%{_datadir}/applications/%{name}-toolbox.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}-toolbox.png

%files javadoc
%{_javadocdir}/%{name}
%doc build/bin/com/lowagie/text/{apache_license,lgpl,misc_licenses,MPL-1.1}.txt

# -----------------------------------------------------------------------------

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 08 2013 Caolán McNamara <caolanm@redhat.com> 2.1.7-20
- Resolves: rhbz#927722 no gcj on RHEL-7

* Fri Mar 01 2013 gil cattaneo <puntogil@libero.it> 2.1.7-19
- re-added rups parts as noarch

* Fri Mar 01 2013 gil cattaneo <puntogil@libero.it> 2.1.7-18
- re-added gcj bits

* Fri Mar 01 2013 gil cattaneo <puntogil@libero.it> 2.1.7-17
- minor changes to current guideline
- removed gcj bits
- added rtf and rups maven poms files (rhbz#879010)
- fix rhbz#905993
- fix rhbz#914094

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov  7 2012 Caolán McNamara <caolanm@redhat.com> - 2.1.7-15
- clarify licences

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May  4 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.7-13
- Change maximum memory for javadoc generation to fix some builds

* Sun Feb 19 2012 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.7-12
- Separate the gcj bits from the other parts, and make the other parts noarch

* Sat Feb 18 2012 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.7-11
- Rebuilt via -target 1.5 due to an openjdk update
- Specify encoding when buliding javadoc

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Andrew Robinson <arobinso@redhat.com> 2.1.7-9
- Fix build issue with un-ASCII-mappable characters.
- Fix build issue inconsistent use of mavenpomdir.

* Fri Nov 25 2011 Andrew Robinson <arobinso@redhat.com> 2.1.7-8
- Add orbit manifest so manifest lists package exports correctly.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 03 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.7-6
- Bump release

* Thu Oct 01 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.7-5
- Separate rtf, rups and toolbox packages
- Reduce dependencies of the main package (RHBZ#524066)

* Thu Aug 27 2009 Andrew Overholt <overholt@redhat.com> 2.1.7-4
- Patch POM file due to explicit "jdk14" requirement on bouncycastle
- Patch in XML output classes from earlier version (their license is
  clean) for maven-doxia

* Thu Aug 27 2009 Andrew Overholt <overholt@redhat.com> 2.1.7-3
- Add maven POM file for use by other maven packages

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 09 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.7-1
- New upstream release

* Tue Jun 16 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.6-1
- New upstream release
- Some SPEC file cleanup

* Tue Apr 21 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.1.5-2
- Patch to allow reading of pdf files from stdin for pdftk (BZ #495574)

* Tue Mar 10 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.1.5-1
- New upstream release

* Tue Mar 03 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.4-5
- Remove the odd Provides introduced in the 2.1.4-3 build.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.4-3
- Add extra Provides for a nice interaction with pdftk.

* Thu Feb 12 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.4-2
- Pass the additional flag "-fno-indirect-classes" to aot-compile-rpm

* Sun Nov 30 2008 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.4-1
- Updated to 2.1.4.
- Set debug="on" on javac part of the build script to compile the aot-bits
  correctly. (bug#472292)

* Sat Oct 11 2008 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.3-4
- Fix more encoding issues.

* Fri Oct 10 2008 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.3-3
- Included the copyright notice (CC-BY) for the icons among the doc files.

* Thu Oct 09 2008 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.3-2
- Enabled compilation of rups library
- Resorted dependencies (added: pdf-renderer, dom4j; removed bouncycastle)
- Fixed java dependencies
- License is (LGPLv2+ or MPLv1.1) and ASL 2.0 and BSD and MIT and LGPLv2+ and CC-BY
- Minor improvements in the SPEC file

* Thu Oct 02 2008 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.1.3-1
- Repacked with version 2.1.3

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.3-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Anthony Green <green@redhat.com> - 1.3-2
- Fix release tag.

* Mon Sep 18 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_9.2
- Rebuild.

* Wed Aug 30 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_9.1
- Rebuild with aot-compile-rpm.

* Tue Jul 25 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_9
- Rebuild with new compiler.

* Tue Feb 28 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_8
- Rebuild with new compiler.

* Mon Jan 17 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_6
- Remove epoch from changelog versions.

* Mon Jan 16 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_5
- Remove empty /usr/share/java/itext.
- Move manual and javadoc packages to Documentation group.
- Add itext-no-javadoc-web-links.patch.

* Mon Jan 16 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_4
- Fixed Group.
- Cleaned up changelog versions.
- Use dos2unix on doc files.
- Don't create unversioned javadoc link.

* Thu Jan 13 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_3
- Remove javadoc %%postun, as that should get handled by the fact
  that the file is ghosted.
- Improve javadoc and manual subpackage descriptions.

* Wed Jan  4 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_2
- Add ant-trax and jaxp_transform_impl dependencies.
- Set OPT_JAR_LIST.

* Wed Jan  4 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_1
- Build native code.
- Add patch to remove proprietary jpeg encoding library usage.
- Fix BuildRequires.
- Tweak BuildRoot.

* Thu Aug 26 2005 Ralph Apel <r.apel at r-apel.de> - 1.3-1jpp
- Upgrade to 1.3
- Now one jar only

* Wed Aug 25 2004 Ralph Apel <r.apel at r-apel.de> - 1.02b-2jpp
- Build with ant-1.6.2
- Relax some versioned dependencies

* Fri Feb 27 2004 Ralph Apel <r.apel at r-apel.de> - 1.02b-1jpp
- First JPackage release
