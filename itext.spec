%define section free
%define gcj_support 1

Name:           itext
Version:        2.0.7
Release:        %mkrel 0.0.3
Epoch:          0
License:        LGPL
Summary:        A Free Java-PDF library
URL:            http://www.lowagie.com/iText/
Group:          Development/Java
Source0:        http://ovh.dl.sourceforge.net/itext/iText-src-%{version}.tar.gz
Source1:        itext-www-20070221.tar.bz2
Source2:        itext-1.4-manifest.mf
Requires:       bouncycastle
BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  ant-trax
BuildRequires:  bouncycastle
BuildRequires:  xalan-j2
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
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

%description javadoc
API documentation for the %{name} package.

%package manual
Summary:        Documents for %{name}
Group:          Development/Java

%description manual
A programming manual for the %{name} package.

%prep
%setup -q -c -T -n itext
%{__mkdir_p} src/META-INF
(cd src
%{__tar} xf %{SOURCE0})
cp %{SOURCE2} src/META-INF/MANIFEST.MF
%{__tar} xf %{SOURCE1}
%{_bindir}/find . -name "*.jar" | %{_bindir}/xargs -t %{__rm}
%{__perl} -pi -e 's/<link.*$//' src/ant/site.xml
%{__perl} -pi -e 's/<attribute name="Class-Path".*$//' src/ant/compile.xml
%{__perl} -pi -e 's/\r$//g' www/examples/com/lowagie/examples/forms/fill/register.xfdf

%build
%{__mkdir_p} lib
pushd src
export CLASSPATH=$(build-classpath bcprov bcmail)
export OPT_JAR_LIST="ant/ant-trax xalan-j2 xalan-j2-serializer"
%{ant} jar javadoc tutorial lowagie.com
popd

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a lib/iText.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

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
