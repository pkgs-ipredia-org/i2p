Name:		i2p
Version:	0.8.12
Release:	3%{?dist}
Summary:	I2P is an anonymous network

Group:		Applications/Internet
License:	Public domain and BSD and GPL + exeption and Artistic MIT and Apache License 2.0 and Eclipse Public License 1.0 and check the source
URL:		http://www.i2p2.de
Source0:	http://mirror.i2p2.de/i2psource_%{version}.tar.bz2
Source1:	http://dist.codehaus.org/jetty/jetty-5.1.x/jetty-5.1.15.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	ant
Requires:	java-1.7.0-openjdk

%description
I2P is an anonymous network, exposing a simple layer that applications can use to anonymously and securely send messages to each other. The network itself is strictly message based (a la IP), but there is a library available to allow reliable streaming communication on top of it (a la TCP). All communication is end to end encrypted (in total there are four layers of encryption used when sending a message), and even the end points ("destinations") are cryptographic identifiers (essentially a pair of public keys).

%prep
%setup -q


%build
# Add Jetty source before build script ask about it
cp %{SOURCE1} apps/jetty/
ant pkg

%install
rm -rf $RPM_BUILD_ROOT
echo "------!!! Install in !!!------"
echo "Folder: $RPM_BUILD_ROOT%{_bindir}/%{name}"
java -jar i2pinstall* -console

# Remove problematic and unnecessary files
rm $RPM_BUILD_ROOT%{_bindir}/%{name}/.installationinformation
rm -rf $RPM_BUILD_ROOT%{_bindir}/%{name}/Uninstaller

# Strip buildroot from files
sed -i "s:$RPM_BUILD_ROOT::g" $RPM_BUILD_ROOT%{_bindir}/%{name}/eepget
sed -i "s:$RPM_BUILD_ROOT::g" $RPM_BUILD_ROOT%{_bindir}/%{name}/runplain.sh
sed -i "s:$RPM_BUILD_ROOT::g" $RPM_BUILD_ROOT%{_bindir}/%{name}/wrapper.config
sed -i "s:$RPM_BUILD_ROOT::g" $RPM_BUILD_ROOT%{_bindir}/%{name}/i2prouter

# Install i2p service (eq 'i2prouter install')
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m755 $RPM_BUILD_ROOT%{_bindir}/%{name}/i2prouter $RPM_BUILD_ROOT%{_initrddir}/i2p

# Remove redundant functionality from i2p service
sed -i "s:^.*gettext.*install.*Install to start automatically.*::" $RPM_BUILD_ROOT%{_initrddir}/i2p
sed -i "s:^.*gettext.*remove.*Uninstall.*::" $RPM_BUILD_ROOT%{_initrddir}/i2p
sed -i "s: | install | remove::" $RPM_BUILD_ROOT%{_initrddir}/i2p

%post
# Register the i2p service
/sbin/chkconfig --add i2p

%preun
# Unregister the i2p service
if [ $1 = 0 ]; then
	/sbin/service i2p stop > /dev/null 2>&1
	/sbin/chkconfig --del i2p
fi

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{_bindir}/%{name}/*
%{_initrddir}/i2p

%changelog
* Sun Feb 19 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-2
- Add i2p init.d service

* Sun Feb 19 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-1
- Initial package

* Sat Feb 18 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-1
- Initial spec template
