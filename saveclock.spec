%global     commit 40031c0f437b70ad5e46f93fce2622b28dbe14e2
%global     commit_short %(c=%{commit}; echo ${c:0:7})

Name:       saveclock
Summary:    Restore/save system clock from/to a file
Version:    0.1
Release:    1.%{commit_short}%{?dist}
URL:        https://github.com/monnerat/saveclock
Source:     %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}-%{commit_short}.tar.gz
License:    MIT
Group:      System Environment/Daemons
BuildRequires:      systemd-units
BuildRequires:      autoconf
BuildRequires:      automake
Requires(post):     systemd-units
Requires(post):     systemd-sysv
Requires(preun):    systemd-units
Requires(postun):   systemd-units


%description
This daemon restores the system clock from a file at start-up, then
periodically saves it back to the same file. This is particularly useful on
systems without a working hardware RTC clock, avoiding problems that may be
caused by a system believing it is still in 1970.
The save period as well as the clock file can be specified on the
command line.


%prep
%setup -n %{name}-%{commit}


%build
./buildconf
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_unitdir}/
install -p -m 0644 %{name}.service %{buildroot}%{_unitdir}/

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
install -p -m 644 %{name}.sysconfig \
%{buildroot}/%{_sysconfdir}/sysconfig/%{name}


%clean
rm -rf %{buildroot}



%post
if [ "${1}" = 1 ]
then	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%preun
if [ "${1}" = 0 ]
then	/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ "${1}" != 0 ]
then	/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi


%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING
%doc %{_mandir}/*/*
%{_sbindir}/*
%dir %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/*


%changelog
* Sat Dec 02 2017 Vaughan <devel at agrez dot net> 0.1-1.40031c0
- Initial package: git commit 40031c0f437b70ad5e46f93fce2622b28dbe14e2
