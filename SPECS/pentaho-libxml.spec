%define origname libxml

Name: pentaho-libxml
Version: 1.1.3
Release: 30%{?dist}
Summary: Namespace aware SAX-Parser utility library
License: LGPLv2
#Original source: http://downloads.sourceforge.net/jfreereport/%%{origname}-%%{version}.zip
#unzip, find . -name "*.jar" -exec rm {} \;
#to simplify the licensing
Source: %{origname}-%{version}-jarsdeleted.zip
URL: http://reporting.pentaho.org/
BuildRequires: ant, java-devel, jpackage-utils, libbase, libloader
Requires: java-headless, jpackage-utils, libbase >= 1.1.2, libloader >= 1.1.2
BuildArch: noarch
Patch0: libxml-1.1.2-build.patch
Patch1: libxml-1.1.2-java11.patch
Patch2: libxml-1.1.3-remove-commons-logging.patch
Patch3: libxml-1.1.3-remove-antcontrib-support.patch

%description
Pentaho LibXML is a namespace aware SAX-Parser utility library. It eases the
pain of implementing non-trivial SAX input handlers.

%package javadoc
Summary: Javadoc for %{name}
Requires: %{name} = %{version}-%{release}
Requires: jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
%patch0 -p1 -b .build
%patch1 -p1 -b .java11
%patch2 -p1 -b .no_commons_logging
%patch3 -p1 -b .remove-antcontrib-support
find . -name "*.jar" -exec rm -f {} \;
mkdir -p lib
build-jar-repository -s -p lib libbase libloader
cd lib

%build
ant jar javadoc
for file in README.txt licence-LGPL.txt ChangeLog.txt; do
    tr -d '\r' < $file > $file.new
    mv $file.new $file
done

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p ./dist/%{origname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{origname}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{origname}
cp -rp bin/javadoc/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{origname}

%files
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/%{origname}.jar

%files javadoc
%{_javadocdir}/%{origname}

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.1.3-30
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Mon Jun 28 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.3-29
- Resolves: rhbz#1976942 remove build dependency on ant-contrib

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.1.3-28
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937
- Related: rhbz#1951271 replace apache-commons-logging with java.util.logging

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.1.3-25
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue May 05 2020 Caolán McNamara <caolanm@redhat.com> - 1.1.3-24
- allow rebuild with java 11

* Wed Feb 26 2020 Kalev Lember <klember@redhat.com> - 1.1.3-23
- Require java-headless, rather than java

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 05 2019 Stephan Bergmann <sbergman@redhat.com> - 1.1.3-20
- Use /usr/share/java instead of _javadir macro for build dependencies

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 23 2013 Caolán McNamara <caolanm@redhat.com> - 1.1.3-11
- Resolves: rhbz#1022153 remove versioned jars

* Tue Aug 06 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.1.3-10
- ant-nodeps is dropped from ant-1.9.0-2 build in rawhide
- Drop buildroot, %%clean, %%defattr and removal of buildroot in %%install

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Caolán McNamara <caolanm@redhat.com> - 1.1.3-7
- clarify license

* Fri Nov 02 2012 Caolán McNamara <caolanm@redhat.com> - 1.1.3-6
- repack source to remove bundled multi-license .jars

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Caolán McNamara <caolanm@redhat.com> - 1.1.3-3
- Related: rhbz#749103 drop gcj aot

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 03 2009 Caolan McNamara <caolanm@redhat.com> 1.1.3
- latest version

* Tue Nov 17 2009 Caolan McNamara <caolanm@redhat.com> 1.1.2
- latest version

* Fri Jul 24 2009 Caolan McNamara <caolanm@redhat.com> 1.0.0-2.OOo31
- make javadoc no-arch when building as arch-dependant aot

* Mon Mar 16 2009 Caolan McNamara <caolanm@redhat.com> 1.0.0-1.OOo31
- Post release tuned for OpenOffice.org reportdesigner

* Mon Mar 09 2009 Caolan McNamara <caolanm@redhat.com> 1.0.0-0.1.rc
- latest version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 07 2008 Caolan McNamara <caolanm@redhat.com> 0.9.11-1
- initial fedora import
