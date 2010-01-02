%define modname hidef
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A58_%{modname}.ini

Summary:	A PHP module providing constants for real
Name:		php-%{modname}
Version:	0.1.2
Release:	%mkrel 3
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/hidef/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Allow definition of user defined constants in simple ini files, which are then
processed like internal constants, without any of the usual performance
penalties.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

mv modules/*.so .

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d/%{modname}

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS INSTALL package*.xml
%dir %{_sysconfdir}/php.d/%{modname}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
