%define section free
%define gcj_support 0

Name:           itext
Version:        2.1.5
Release:        %mkrel 2
Epoch:          0
License:        LGPL
Summary:        Free Java-PDF library
URL:            http://www.lowagie.com/iText/
Group:          Development/Java
Source0:        http://downloads.sourceforge.net/itext/iText-src-%{version}.tar.gz
Source1:        itext-www-20070221.tar.bz2
Source2:        itext-1.4-manifest.mf
Requires:       bouncycastle
Provides:       itext2 = %{epoch}:%{version}-%{release}
Obsoletes:      itext2 < %{epoch}:%{version}-%{release}
BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  ant-trax
BuildRequires:  bouncycastle
BuildRequires:  xalan-j2
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%{__rm} -rf %{buildroot}

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
%{__cp} -a build/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

# manual
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}-%{version}
%{__cp} -a build/lowagie/* %{buildroot}%{_docdir}/%{name}-%{version}
%{__cp} -a build/examples %{buildroot}%{_docdir}/%{name}-%{version}
%{__cp} -a build/tutorial %{buildroot}%{_docdir}/%{name}-%{version}

%clean
%{__rm} -rf %{buildroot}

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
