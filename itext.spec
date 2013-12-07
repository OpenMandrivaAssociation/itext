%define section free
%define gcj_support 0

Summary:	Free Java-PDF library
Name:		itext
Version:	2.1.5
Release:	5
License:	LGPLv2
Group:		Development/Java
Url:		http://www.lowagie.com/iText/
Source0:	http://downloads.sourceforge.net/itext/iText-src-%{version}.tar.gz
Source1:	itext-www-20070221.tar.bz2
Source2:	itext-1.4-manifest.mf
BuildRequires:	java-rpmbuild
BuildRequires:	ant
BuildRequires:	ant-trax
BuildRequires:	bouncycastle
BuildRequires:	bouncycastle-extras
BuildRequires:	xalan-j2
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:	noarch
%endif
Requires:	bouncycastle
Requires:	bouncycastle-extras
Provides:	itext2 = %{version}-%{release}
Obsoletes:	itext2 < %{version}-%{release}

%description
iText is a library that allows you to generate PDF files on the fly. The
iText classes are very useful for people who need to generate read-only,
platform independent documents containing text, lists, tables and
images. The library is especially useful in combination with Java(TM)
technology-based Servlets:	The look and feel of HTML is browser
dependent; with iText and PDF you can control exactly how your servlet's
output will look.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
Provides:	itext2-javadoc = %{version}-%{release}
Obsoletes:	itext2-javadoc < %{version}-%{release}

%description javadoc
API documentation for the %{name} package.

%package manual
Summary:	Documents for %{name}
Group:		Development/Java
Provides:	itext2-manual = %{version}-%{release}
Obsoletes:	itext2-manual < %{version}-%{release}

%description manual
A programming manual for the %{name} package.

%prep
%setup -q -c
%setup -q -D -T -a 1

mkdir -p src/META-INF
cp %{SOURCE2} src/META-INF/MANIFEST.MF

mkdir -p lib

perl -pi -e 's/<link.*$//' src/ant/site.xml
perl -pi -e 's/<attribute name="Class-Path".*$//' src/ant/compile.xml
perl -pi -e 's/\r$//g' www/examples/com/lowagie/examples/forms/fill/register.xfdf

%build
pushd src
export CLASSPATH=$(build-classpath bcprov bcmail)
export OPT_JAR_LIST="`%{__cat} %{_sysconfdir}/ant.d/trax`"
%{ant} jar javadoc tutorial lowagie.com
popd

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -a lib/iText.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -s ${jar} `echo ${jar} | sed "s|-%{version}||g"`; done)

%{gcj_compile}

perl -pi -e 's/\r$//g' build/lowagie/*.{txt,xml}
perl -pi -e 's/\r$//g' build/lowagie/ant/*.xml
perl -pi -e 's/\r$//g' build/lowagie/ant/.ant.properties

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
#cp -a build/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -s %{name}-%{version} %{name})

# manual
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
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
%doc %{_docdir}/%{name}-%{version}/MPL-1.1.txt
%doc %{_docdir}/%{name}-%{version}/lgpl.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%doc %{_docdir}/*
%exclude %{_docdir}/%{name}-%{version}/*.txt

