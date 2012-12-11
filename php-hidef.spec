%define modname hidef
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A58_%{modname}.ini

Summary:	A PHP module providing constants for real
Name:		php-%{modname}
Version:	0.1.13
Release:	%mkrel 1
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


%changelog
* Mon Jul 16 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.13-1mdv2012.0
+ Revision: 809919
- 0.1.13

* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.12-1
+ Revision: 806359
- 0.1.12

* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.11-2
+ Revision: 795447
- rebuild for php-5.4.x

* Tue Apr 10 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.11-1
+ Revision: 790151
- 0.1.11

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.10-2
+ Revision: 761254
- rebuild

* Sun Nov 27 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.10-1
+ Revision: 733708
- 0.1.10

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.8-3
+ Revision: 696430
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.8-2
+ Revision: 695405
- rebuilt for php-5.3.7

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.8-1
+ Revision: 678086
- 0.1.8

* Tue May 17 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-1
+ Revision: 675367
- 0.1.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.6-2
+ Revision: 646649
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.6-1mdv2011.0
+ Revision: 630301
- 0.1.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.5-3mdv2011.0
+ Revision: 629811
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.5-2mdv2011.0
+ Revision: 628132
- ensure it's built without automake1.7

* Wed Dec 01 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.5-1mdv2011.0
+ Revision: 604428
- 0.1.5

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-3mdv2011.0
+ Revision: 600496
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-2mdv2011.0
+ Revision: 588834
- rebuild

* Thu Sep 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-1mdv2011.0
+ Revision: 578872
- 0.1.4

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-4mdv2010.1
+ Revision: 514553
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-3mdv2010.1
+ Revision: 485376
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-2mdv2010.1
+ Revision: 468174
- rebuilt against php-5.3.1

* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2010.0
+ Revision: 452813
- 0.1.2 (php-5.3.x fixes)

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-8mdv2010.0
+ Revision: 451278
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.1.1-7mdv2010.0
+ Revision: 397335
- Rebuild

* Tue May 19 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-6mdv2010.0
+ Revision: 377686
- fix build
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-5mdv2009.1
+ Revision: 346501
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-4mdv2009.1
+ Revision: 341762
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-3mdv2009.1
+ Revision: 321793
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-2mdv2009.1
+ Revision: 310274
- rebuilt against php-5.2.7

* Wed Oct 15 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-1mdv2009.1
+ Revision: 293863
- 0.1.1

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-9mdv2009.0
+ Revision: 238401
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-8mdv2009.0
+ Revision: 200207
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-7mdv2008.1
+ Revision: 162227
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-6mdv2008.1
+ Revision: 107663
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-5mdv2008.0
+ Revision: 77547
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4mdv2008.0
+ Revision: 39499
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3mdv2008.0
+ Revision: 33810
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2008.0
+ Revision: 21332
- rebuilt against new upstream version (5.2.2)

