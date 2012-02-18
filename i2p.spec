Name:		
Version:	
Release:	1%{?dist}
Summary:	

Group:		
License:	
URL:		
Source0:	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	
Requires:	

%description


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc



%changelog
* 2012-02-18 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.12.18-1
- Initial spec template
