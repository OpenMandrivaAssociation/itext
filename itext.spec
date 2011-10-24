%define _mavenpomdir %{_datadir}/maven2/poms
%define alternate_name iText

Name:           itext
Version:        2.1.7
Release:        4
License:        (LGPLv2+ or MPLv1.1) and ASL 2.0 and BSD and LGPLv2+
Summary:        A Free Java-PDF library
Url:            http://www.lowagie.com/iText/
Group:          Development/Java 
Source0:        http://downloads.sourceforge.net/itext/iText-src-%{version}.tar.bz2
Source2:        http://repo2.maven.org/maven2/com/lowagie/itext/%{version}/itext-%{version}.pom
Source3:        itext-rups.sh
Source4:        itext-rups.desktop
Source5:        itext-toolbox.sh
Source6:        itext-toolbox.desktop
Patch1:         itext-2.1.5-pdftk.patch

# The iText POM specifies that it requires bouncycastle's "jdk14" JARs
# but we have "jdk16".
Patch2:         itext-2.1.7-fixpomforbc.patch
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
Patch3:         itext-xmloutput.patch.bz2

BuildRequires:  ant
BuildRequires:  bouncycastle-tsp
BuildRequires:  desktop-file-utils
BuildRequires:  dom4j
BuildRequires:  ImageMagick
BuildRequires:  mozilla-nss
BuildRequires:  pdf-renderer
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jpackage-utils
Requires:       bouncycastle-tsp
Requires:       java >= 0:1.6.0
Requires:       jpackage-utils >= 1.5
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Requires(post):   jpackage-utils >= 1.7
Requires(postun): jpackage-utils >= 1.7
Provides:         %{alternate_name} == %{version}-%{release}

%description
iText is a library that allows you to generate PDF files on the fly. The iText
classes are very useful for people who need to generate read-only, platform
independent documents containing text, lists, tables and images. The library is
especially useful in combination with Java(TM) technology-based Servlets: The
look and feel of HTML is browser dependent; with iText and PDF you can control
exactly how your servlet's output will look.

%package rtf
License:        MPLv1.1 or LGPLv2+
Summary:        Library to output Rich Text Files
Group:          Development/Java 
Requires:       %{name} = %{version}-%{release}

%description rtf
The RTF package is an extension of the iText library and allows iText to output
Rich Text Files in additon to PDF files. These files can then be viewed and
edited with RTF viewers such as OpenOffice.org Writer.

%package rups
License:        LGPLv2+ and CC-BY
Summary:        Reading/Updating PDF Syntax
Group:          Development/Java 
Requires:       %{name} = %{version}-%{release}
Requires:       dom4j
Requires:       pdf-renderer

%description rups
iText RUPS is a tool that combines SUN's PDF Renderer (to view PDF documents),
iText's PdfReader (to inspect the internal structure of a PDF file), and
iText's PdfStamper to manipulate a PDF file.

%package toolbox
License:        MPLv1.1 or MIT
Summary:        Some %{alternate_name} tools
Group:          Development/Java 
Requires:       %{name} = %{version}-%{release}
Requires:       java >= 0:1.6.0

%description toolbox
iText is a free open source Java-PDF library released on SF under the MPL/LGPL;
iText comes with a simple GUI: the iText toolbox. The original developers of
iText want to publish this toolbox as a separate project under the more
permissive MIT license. This is a utility that allows you to use a number of
iText tools.

%package javadoc
Summary:        Javadoc for %{alternate_name}
Group:          Development/Java 
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
API documentation for the %{alternate_name} package.

%prep
%setup -q -c -T -a 0
%patch1 -p1 -b .pdftk
cp -pr %{SOURCE2} JPP-itext.pom
%patch2 -p0 -b .fixpomforbc
%patch3 -p0 -b .xmloutput

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

# Remove classpath elements from manifest
sed -i '\|Class-Path|d' src/ant/compile.xml

# Setting debug="on" on javac part of the build script.
sed -i 's|destdir|debug="on" destdir|g' src/ant/compile.xml
sed -i 's|debug="true"||g' src/ant/compile.xml

%build
export CLASSPATH=$(build-classpath bcprov bcmail bctsp pdf-renderer dom4j)
pushd src
ant jar jar.rups jar.rtf jar.toolbox javadoc
popd

%install
export NO_BRP_CHECK_BYTECODE_VERSION=true
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p lib/iText.jar \
      %{buildroot}%{_javadir}/%{name}-%{version}.jar
cp -p lib/iText-rtf.jar \
      %{buildroot}%{_javadir}/%{name}-rtf-%{version}.jar
cp -p lib/iText-rups.jar \
      %{buildroot}%{_javadir}/%{name}-rups-%{version}.jar
cp -p lib/iText-toolbox.jar \
      %{buildroot}%{_javadir}/%{name}-toolbox-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do \
      ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# rups stuff
install -D -pm 755 %{SOURCE3} %{buildroot}%{_bindir}/%{name}-rups
install -D -m 0755 %{SOURCE4} %{buildroot}%{_datadir}/applications/itext-rups.desktop

# toolbox stuff
install -D -pm 755 %{SOURCE5} %{buildroot}%{_bindir}/%{name}-toolbox
install -D -m 0755 %{SOURCE6} %{buildroot}%{_datadir}/applications/itext-toolbox.desktop

# icon for rups and toolbox
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
convert -resize 128x128 src/toolbox/com/lowagie/toolbox/1t3xt.gif %{name}.png
cp -a %{name}.png \
      %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}-rups.png
cp -a %{name}.png \
      %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}-toolbox.png

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/docs/* %{buildroot}%{_javadocdir}/%{name}

# Install the pom
install -dm 755 %{buildroot}%{_datadir}/maven2/poms
cp -pr JPP-itext.pom %{buildroot}%{_mavenpomdir}
%add_to_maven_depmap itext itext %{version} JPP itext
%add_to_maven_depmap com.lowagie itext %{version} JPP itext

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%doc build/bin/com/lowagie/text/{apache_license,lgpl,misc_licenses,MPL-1.1}.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_mavenpomdir}/JPP-itext.pom
%config %{_mavendepmapfragdir}/%{name}

%files rtf
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-rtf.jar
%{_javadir}/%{name}-rtf-%{version}.jar

%files rups
%defattr(0644,root,root,0755)
%doc src/rups/com/lowagie/rups/view/icons/copyright_notice.txt
%dir %{_datadir}/icons/hicolor
%{_javadir}/%{name}-rups.jar
%{_javadir}/%{name}-rups-%{version}.jar
%attr(0755,root,root) %{_bindir}/%{name}-rups
%{_datadir}/applications/%{name}-rups.desktop
%{_datadir}/icons/hicolor/*

%files toolbox
%defattr(0644,root,root,0755)
%doc src/toolbox/com/lowagie/toolbox/tools.txt
%dir %{_datadir}/icons/hicolor
%{_javadir}/%{name}-toolbox.jar
%{_javadir}/%{name}-toolbox-%{version}.jar
%attr(0755,root,root) %{_bindir}/%{name}-toolbox
%{_datadir}/applications/%{name}-toolbox.desktop
%{_datadir}/icons/hicolor/*
#%{_datadir}/icons/hicolor/128x128/apps/%{name}-toolbox.png

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

