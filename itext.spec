%define section free
%define gcj_support 0

Name:           itext
Version:        2.1.5
Release:        2
Epoch:          0
License:        LGPL
Summary:        Free Java-PDF library
URL:            http://www.lowagie.com/iText/
Group:          Development/Java
Source0:        http://downloads.sourceforge.net/itext/iText-src-%{version}.tar.gz
Source1:        itext-www-20070221.tar.bz2
Source2:        itext-1.4-manifest.mf
Requires:       bouncycastle
Requires:       bouncycastle-extras
Provides:       itext2 = %{epoch}:%{version}-%{release}
Obsoletes:      itext2 < %{epoch}:%{version}-%{release}
BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  ant-trax
BuildRequires:  bouncycastle
BuildRequires:  bouncycastle-extras
BuildRequires:  xalan-j2
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
iText is a library that allows you to generate PDF files on the fly. The
iText classes are very useful for people who need to generate read-only,
platform independent documents containing text, lists, tables and
images. The library is especially useful in combination with Java(TM)
technology-based Servlets: The look and feel of HTML is browser
dependent; with iText and PDF you can control exactly how your servlet's
output will look.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Provides:       itext2-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:      itext2-javadoc < %{epoch}:%{version}-%{release}

%description javadoc
API documentation for the %{name} package.

%package manual
Summary:        Documents for %{name}
Group:          Development/Java
Provides:       itext2-manual = %{epoch}:%{version}-%{release}
Obsoletes:      itext2-manual < %{epoch}:%{version}-%{release}

%description manual
A programming manual for the %{name} package.

%prep
%setup -q -c
%setup -q -D -T -a 1

%{__mkdir_p} src/META-INF
cp %{SOURCE2} src/META-INF/MANIFEST.MF

%{__mkdir_p} lib

%{__perl} -pi -e 's/<link.*$//' src/ant/site.xml
%{__perl} -pi -e 's/<attribute name="Class-Path".*$//' src/ant/compile.xml
%{__perl} -pi -e 's/\r$//g' www/examples/com/lowagie/examples/forms/fill/register.xfdf

%build
pushd src
export CLASSPATH=$(build-classpath bcprov bcmail)
export OPT_JAR_LIST="`%{__cat} %{_sysconfdir}/ant.d/trax`"
%{ant} jar javadoc tutorial lowagie.com
popd

%install
# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a lib/iText.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do %{__ln_s} ${jar} `echo ${jar} | %{__sed} "s|-%{version}||g"`; done)

%{gcj_compile}

%{__perl} -pi -e 's/\r$//g' build/lowagie/*.{txt,xml}
%{__perl} -pi -e 's/\r$//g' build/lowagie/ant/*.xml
%{__perl} -pi -e 's/\r$//g' build/lowagie/ant/.ant.properties

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
#cp -a build/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

# manual
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}-%{version}
cp -a build/lowagie/* %{buildroot}%{_docdir}/%{name}-%{version}
cp -a build/examples %{buildroot}%{_docdir}/%{name}-%{version}
cp -a build/tutorial %{buildroot}%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/MPL-1.1.txt
%doc %{_docdir}/%{name}-%{version}/lgpl.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/*
%exclude %{_docdir}/%{name}-%{version}/*.txt

%changelog
* Sun Mar 08 2009 Frederik Himpe <fhimpe@mandriva.org> 0:2.1.5-1mdv2009.1
+ Revision: 352880
- update to new version 2.1.5

* Wed Feb 18 2009 Jérôme Soyer <saispo@mandriva.org> 0:2.1.4-0.0.1mdv2009.1
+ Revision: 342309
- New upstream release

* Sun Jul 13 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:2.1.3-0.0.1mdv2009.0
+ Revision: 234258
- new version 2.1.3

* Fri May 23 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:2.1.2-0.0.2mdv2009.0
+ Revision: 210151
- disable gcj compile

  + David Walluck <walluck@mandriva.org>
    - move mkdir to %%prep
    - 2.1.2u

* Mon Apr 14 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:2.1.0-0.0.1mdv2009.0
+ Revision: 193443
- new version

* Fri Jan 25 2008 David Walluck <walluck@mandriva.org> 0:2.0.8-0.0.2mdv2008.1
+ Revision: 158083
- obsolete itext2 subpackage as well

* Fri Jan 25 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:2.0.8-0.0.1mdv2008.1
+ Revision: 157919
- new release

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 31 2007 David Walluck <walluck@mandriva.org> 0:2.0.7-0.0.4mdv2008.1
+ Revision: 139929
- add itext2 Provides/Obsoletes
- set OPT_JAR_LIST better
- more macros

* Thu Dec 20 2007 David Walluck <walluck@mandriva.org> 0:2.0.7-0.0.3mdv2008.1
+ Revision: 135375
- there are no jars to remove
- fix syntax error in spec
- fix bouncycastle (Build)Requires

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Thu Nov 29 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:2.0.7-0.0.1mdv2008.1
+ Revision: 113887
- new version

* Sat Oct 13 2007 David Walluck <walluck@mandriva.org> 0:2.0.6-1mdv2008.1
+ Revision: 97842
- add sources
- 2.0.6

* Mon Sep 17 2007 David Walluck <walluck@mandriva.org> 0:2.0.5-1mdv2008.1
+ Revision: 89365
- 2.0.5

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.0.4-3mdv2008.0
+ Revision: 87394
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:2.0.4-2mdv2008.0
+ Revision: 82854
- rebuild

* Mon Jun 04 2007 David Walluck <walluck@mandriva.org> 0:2.0.4-1mdv2008.0
+ Revision: 35251
- 2.0.4

* Tue Apr 17 2007 David Walluck <walluck@mandriva.org> 0:2.0.2-1mdv2008.0
+ Revision: 14114
- 2.0.2


* Tue Dec 19 2006 David Walluck <walluck@mandriva.org> 1.4.8-1mdv2007.0
+ Revision: 100231
- 1.4.8

* Mon Dec 11 2006 David Walluck <walluck@mandriva.org> 0:1.4.7-1mdv2007.1
+ Revision: 95103
- 1.4.7

* Tue Oct 31 2006 David Walluck <walluck@mandriva.org> 0:1.4.6-1mdv2007.1
+ Revision: 73920
- 1.4.6
- Import itext

* Sat Sep 16 2006 David Walluck <walluck@mandriva.org> 0:1.4.5-1mdv2007.0
- 1.4.5

* Tue Sep 05 2006 David Walluck <walluck@mandriva.org> 0:1.4.4-1mdv2007.0
- 1.4.4

* Tue Aug 29 2006 David Walluck <walluck@mandriva.org> 0:1.4.3-2mdv2007.0
- 1.4.4
- do not require dos2unix for build

* Wed Aug 09 2006 David Walluck <walluck@mandriva.org> 0:1.4.3-1mdv2007.0
- 1.4.3

* Tue Jun 06 2006 David Walluck <walluck@mandriva.org> 0:1.3-1.8.1mdv2007.0
- release

* Tue Feb 28 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_8
- Rebuild with new compiler.

* Tue Jan 17 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_6
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

* Fri Jan 13 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_3
- Remove javadoc %%postun, as that should get handled by the fact
  that the file is ghosted.
- Improve javadoc and manual subpackage descriptions.

* Wed Jan 04 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_2
- Add ant-trax and jaxp_transform_impl dependencies.
- Set OPT_JAR_LIST.

* Wed Jan 04 2006 Anthony Green <green@redhat.com> - 1.3-1jpp_1
- Build native code.
- Add patch to remove proprietary jpeg encoding library usage.
- Fix BuildRequires.
- Tweak BuildRoot.

* Sat Aug 27 2005 Ralph Apel <r.apel at r-apel.de> - 1.3-1jpp
- Upgrade to 1.3
- Now one jar only

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> - 1.02b-2jpp
- Build with ant-1.6.2
- Relax some versioned dependencies

* Fri Feb 27 2004 Ralph Apel <r.apel at r-apel.de> - 1.02b-1jpp
- First JPackage release

