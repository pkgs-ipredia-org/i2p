%global _binaries_in_noarch_packages_terminate_build 0

Name:		i2p
Version:	0.9.15
Release:	1%{?dist}
Summary:	I2P Anonymous Network

Group:		Applications/Internet
License:	Public domain and BSD and GPL + exeption and Artistic MIT and Apache License 2.0 and Eclipse Public License 1.0 and check the source
URL:		http://www.i2p2.de
Source0:	https://download.i2p2.de/releases/%{version}/i2psource_%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Patch10: 	i2p-0.9.15-add-ipredia-host-targets.patch

BuildRequires:	ant expect jetty gettext
Requires:	java jetty
Requires(pre):	/usr/sbin/useradd
Requires(post):	chkconfig

BuildArch:	noarch

# Description from Slackware/i2p/slack-desc
%description
I2P is an anonymizing network, offering a simple layer that
identity-sensitive applications can use to securely communicate. All
data is wrapped with several layers of encryption, and the network is
both distributed and dynamic, with no trusted parties.
Many applications are available that interface with I2P, including 
mail, peer-peer file sharing, IRC chat, and others.


%prep
%setup -q

%patch10 -p1 -b .add-ipredia-host-targets.patch


%build
# Change the home path (i2p config dir) before izpack does it
sed -i "s:%USER_HOME:\$HOME:g" installer/resources/i2prouter

# Building EXEs in x64 Linux requires that 32bit libraries are installed
sed -i "s:#noExe=true:noExe=true:g" build.properties


ant pkg


%install
rm -rf $RPM_BUILD_ROOT

echo "------!!! Install in !!!------"
echo "Folder: $RPM_BUILD_ROOT%{_bindir}/%{name}"
# java -jar i2pinstall* -console
expect -c "spawn java -jar i2pinstall.jar -console; expect redisplay; send \"1\r\"; expect path; send \"$RPM_BUILD_ROOT%{_bindir}/%{name}\r\"; expect redisplay; send \"1\n\"; expect done"

# Remove problematic and unnecessary files
rm $RPM_BUILD_ROOT%{_bindir}/%{name}/.installationinformation
rm -rf $RPM_BUILD_ROOT%{_bindir}/%{name}/Uninstaller

# Strip buildroot from files
sed -i "s:$RPM_BUILD_ROOT::g" $RPM_BUILD_ROOT%{_bindir}/%{name}/eepget
sed -i "s:$RPM_BUILD_ROOT::g" $RPM_BUILD_ROOT%{_bindir}/%{name}/runplain.sh
sed -i "s:$RPM_BUILD_ROOT::g" $RPM_BUILD_ROOT%{_bindir}/%{name}/wrapper.config
sed -i "s:$RPM_BUILD_ROOT::g" $RPM_BUILD_ROOT%{_bindir}/%{name}/i2prouter

# Disable updates
echo "router.updateDisabled=true" >> $RPM_BUILD_ROOT%{_bindir}/%{name}/router.config

# Install i2p service (eq 'i2prouter install')
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m755 $RPM_BUILD_ROOT%{_bindir}/%{name}/i2prouter $RPM_BUILD_ROOT%{_initrddir}/i2p

# Remove redundant functionality from i2p service
sed -i "s:^.*gettext.*install.*Install to start automatically.*::g" $RPM_BUILD_ROOT%{_initrddir}/i2p
sed -i "s:^.*gettext.*remove.*Uninstall.*::g" $RPM_BUILD_ROOT%{_initrddir}/i2p
sed -i "s: | install | remove::g" $RPM_BUILD_ROOT%{_initrddir}/i2p

# Use i2p user to run the service
sed -i "s:^#RUN_AS_USER=:RUN_AS_USER=\"i2p\":g" $RPM_BUILD_ROOT%{_initrddir}/i2p

# Fix for upstream bug (runuser and a secure (without a shell) service account)
# Fix: add a shell with -s /bin/sh
sed -i "s:/sbin/runuser -:/sbin/runuser -s /bin/sh -:g" $RPM_BUILD_ROOT%{_initrddir}/i2p

# Append init order to row 2
sed -i '2 a # chkconfig: - 99 10' $RPM_BUILD_ROOT%{_initrddir}/i2p


%posttrans
# Condrestart and return 0
/sbin/service i2p condrestart >/dev/null 2>&1 || :

%post
# Register the i2p service
/sbin/chkconfig --add i2p > /dev/null 2>&1


%pre
# Add the "i2p" user
getent group i2p >/dev/null || groupadd -r i2p
getent passwd i2p >/dev/null || useradd -r -g i2p -s /sbin/nologin -d /usr/local/i2p -c "I2P" i2p
# Create the home diretory for i2p if it not exist (useradd cant do it with selinux enabled)
if [ ! -d "/usr/local/i2p" ]; then
	mkdir /usr/local/i2p
	chown i2p:i2p /usr/local/i2p
fi
exit 0

%preun
# Unregister the i2p service
if [ $1 = 0 ]; then
	/sbin/service i2p stop > /dev/null 2>&1
	/sbin/chkconfig --del i2p > /dev/null 2>&1
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{_bindir}/%{name}
%{_initrddir}/i2p


%changelog
* Tue Sep 30 2014 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9.15-1
- Update to 0.9.15

* Tue Sep 30 2014 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9.7-2
- Change source URL

* Mon Oct 5 2013 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9.7-1
- Update to 0.9.7

* Wed May 29 2013 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9.6-1
- Update to 0.9.6

* Sat Mar 16 2013 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9.5-1
- Update to 0.9.5

* Thu Jan 3 2013 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9.4-1
- Update to 0.9.4

* Sat Sep 22 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9.2-1
- Update to 0.9.2

* Tue Jul 31 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9.1-1
- Update to 0.9.1

* Tue Jul 10 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9-3
- Add init order

* Mon Jun 18 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9-2
- Remove desktop

* Sun May 6 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.9-1
- Update to i2p 0.9

* Tue Apr 10 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.13-2
- Change from openjdk 1.7.0 to java.

* Tue Apr 3 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.13-1
- Update to 0.8.13

* Wed Mar 28 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-8
- Add desktop sub package

* Tue Mar 20 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-7
- Condrestart return 0

* Wed Feb 22 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-6
- Add service i2p start in post installation

* Mon Feb 20 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-5
- Add i2p service account

* Sun Feb 19 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-4
- Use expect for silent install

* Sun Feb 19 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-3
- Include installation folder in %files

* Sun Feb 19 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-2
- Add i2p init.d service

* Sun Feb 19 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-1
- Initial package

* Sat Feb 18 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-1
- Initial spec template
