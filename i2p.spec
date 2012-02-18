Name:		i2p
Version:	0.8.12
Release:	1%{?dist}
Summary:	I2P is an anonymous network

Group:		Applications/Internet
License:	Public domain and BSD and GPL + exeption and Artistic MIT and check the source
URL:		http://www.i2p2.de
Source0:	http://mirror.i2p2.de/i2psource_0.8.12.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	ant
Requires:	java-1.7.0-openjdk

%description
I2P is an anonymous network, exposing a simple layer that applications can use to anonymously and securely send messages to each other. The network itself is strictly message based (a la IP), but there is a library available to allow reliable streaming communication on top of it (a la TCP). All communication is end to end encrypted (in total there are four layers of encryption used when sending a message), and even the end points ("destinations") are cryptographic identifiers (essentially a pair of public keys).

%prep
%setup -q


%build
ant pkg

%install
rm -rf $RPM_BUILD_ROOT
java -jar i2pinstall* -console

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc



%changelog
* Sat Feb 18 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.8.12-1
- Initial spec template
