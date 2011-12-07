Summary: A console-based network monitoring utility
Name: iptraf
Version: 3.0.1
Release: 13%{?dist}
Source0: http://www.penguin.cz/~fojtik/iptraf/%{name}-%{version}.tar.gz
Source1: iptraf 
URL: http://www.penguin.cz/~fojtik/iptraf/
Patch0: iptraf-2.4.0-Makefile.patch
Patch1: iptraf-2.7.0-install.patch
Patch2: iptraf-2.7.0-doc.patch
Patch4: iptraf-2.7.0-nostrip.patch
Patch5: iptraf-3.0.0-setlocale.patch
Patch6: iptraf-3.0.0-longdev.patch
Patch7: iptraf-3.0.1-compile.fix.patch
Patch8: iptraf-3.0.0-in_trafic.patch
Patch9: iptraf-3.0.1-incltypes.patch
Patch10: iptraf-3.0.0-ifname.patch
Patch11: iptraf-3.0.0-interface.patch
Patch12: iptraf-3.0.1-ipv6.patch
Patch13: iptraf-3.0.1-ipv6-fix.patch
Patch14: iptraf-3.0.1-servmon-fix.patch
Patch15: 0001-fix-strcpy-overlap-memory.patch
Patch16: iptraf-3.0.1-strict-aliasing.patch
License: GPLv2+
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ncurses-devel

%description
IPTraf is a console-based network monitoring utility.  IPTraf gathers
data like TCP connection packet and byte counts, interface statistics
and activity indicators, TCP/UDP traffic breakdowns, and LAN station
packet and byte counts.  IPTraf features include an IP traffic monitor
which shows TCP flag information, packet and byte counts, ICMP
details, OSPF packet types, and oversized IP packet warnings;
interface statistics showing IP, TCP, UDP, ICMP, non-IP and other IP
packet counts, IP checksum errors, interface activity and packet size
counts; a TCP and UDP service monitor showing counts of incoming and
outgoing packets for common TCP and UDP application ports, a LAN
statistics module that discovers active hosts and displays statistics
about their activity; TCP, UDP and other protocol display filters so
you can view just the traffic you want; logging; support for Ethernet,
FDDI, ISDN, SLIP, PPP, and loopback interfaces; and utilization of the
built-in raw socket interface of the Linux kernel, so it can be used
on a wide variety of supported network cards.

%prep
%setup -q 
%patch7 -p1 -b .compile
%patch12 -p1 -b .ipv6
%patch13 -p1 -b .ipv6-fix
%patch14 -p1 -b .servmon-fix
%patch15 -p1 -b .fix-strcpy-overlap-memory
%patch16 -p1 -b .strict-aliasing
%patch0 -p1 -b .Makefile
%patch1 -p1 -b .install
%patch2 -p1 -b .doc
%patch4 -p1 -b .nostrip
%patch5 -p1 -b .setlocale
%patch6 -p1 -b .longdev
%patch8 -p1 -b .in_trafic
%patch9 -p1 -b .incltypes
%patch10 -p0 -b .ifname
%patch11 -p1 -b .interface

%build
make -C src CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
	TARGET=%{_prefix}/bin \
	LOCKDIR=/var/lock/iptraf \
	LOGDIR=/var/log/iptraf \
	WORKDIR=/var/lib/iptraf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}/bin
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install -m644 Documentation/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

make -C src TARGET=$RPM_BUILD_ROOT%{_prefix}/bin \
	LOCKDIR=$RPM_BUILD_ROOT/var/lock/iptraf \
	LOGDIR=$RPM_BUILD_ROOT/var/log/iptraf \
	WORKDIR=$RPM_BUILD_ROOT/var/lib/iptraf \
	install

# remove everything besides the html and pictures in Documentation
find Documentation -type f | grep -v '\.html$\|\.png$\|/stylesheet' | \
	xargs rm -f
rm -rf Documentation/.xvpics
rm -f Documentation/stylesheet-images/.eps
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d/
cp %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/iptraf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES FAQ LICENSE INSTALL README* RELEASE-NOTES
%doc Documentation
%attr(755,root,root) %{_prefix}/bin/*
%{_mandir}/*/*
%dir %attr(755,root,root) /var/lock/iptraf
%dir %attr(755,root,root) /var/log/iptraf
%dir %attr(755,root,root) /var/lib/iptraf
%dir %attr(644,root,root) %config(noreplace) /etc/logrotate.d/iptraf

%changelog
* Thu May 27 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.0.1-13
- add patch iptraf-3.0.1-strict-aliasing.patch
- Resolves: #596173 - RPMdiff run failed for package iptraf-3.0.1-11.el6

* Tue May 25 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.0.1-12
- add patch 0001-fix-strcpy-overlap-memory.patch
- Resolves: 595454  - Doesn't detect any ethernet interface

* Thu Feb 25 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.0.1-11
- remove empty hidden file(Documentation/stylesheet-images/.eps)

* Wed Jan 5 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.0.1-10
- fix url. Changed form original upstream because its dead.

* Mon Jan 4 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.0.1-9
- fix #549745 - "iptraf -s lo" makes iptraf crash

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 3.0.1-8.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 02 2008 Zdenek Prikryl <zprikryl@redhat.com> - 3.0.1-6
- Minor fixes in patches ipv6, incltypes and ifname

* Thu Jun 05 2008 Zdenek Prikryl <zprikryl@redhat.com> - 3.0.1-5
- Added support for ipv6 (#200503)
- Fixed vlan support (#219772)
- Added support for bond interfaces

* Tue Apr 15 2008 Zdenek Prikryl <zprikryl@redhat.com> - 3.0.1-4
- Length of iface name is increased
- Resolves #439201

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.1-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Marcela Maslanova <mmaslano@redhat.com> - 3.0.1-2
- logratate now rotate only *.log files, not all of them #428683

* Fri Nov  2 2007 Marcela Maslanova <mmaslano@redhat.com> - 3.0.1-1
- upgrade iptraf-3.0.1

* Fri Aug 24 2007 Marcela Maslanova <mmaslano@redhat.com> - 3.0.0-7
- rebuilt for mass rebuilt
- check license

* Wed Apr  4 2007 Marcela Maslanova <mmaslano@redhat.com> - 3.0.0-6
- merge review, add logrotate file
- rhbz#225907

* Mon Dec 11 2006 Marcela Maslanova <mmaslano@redhat.com> - 3.0.0-5
- input traffic

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.0.0-4.1
- rebuild

* Thu Jun 06 2006 Marcela Maslanova <mmaslano@redhat.com> 3.0.0-4
- fix compile (#192510)

* Wed Apr 05 2006 Miroslav Lichvar <mlichvar@redhat.com> 3.0.0-2
- fix crash when parsing long network interface name (#187937)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.0.0-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.0.0-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Miroslav Lichvar <mlichvar@redhat.com> 3.0.0-1
- update to release 3.0.0
- spec cleanup
- drop cfgpath patch
- fix bad display of frames on linux console (#140698)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue May 17 2005 Karsten Hopp <karsten@redhat.de> 2.7.0-15
- move config file to %%{_sysconfdir}/iptraf.cfg to prevent deletion at bootup (#157794)

* Tue May 10 2005 Karsten Hopp <karsten@redhat.de> 2.7.0-14
- enable debuginfo

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 2.7.0-13
- - build with gcc-4

* Tue Dec 21 2004 Karsten Hopp <karsten@redhat.de> 2.7.0-12
- add some ethernet interface names (#143477)

* Mon Aug 09 2004 Karsten Hopp <karsten@redhat.de> 2.7.0-11 
- add patch from Robert Scheck to fix filenames/paths in manpages
  (#128476)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Karsten Hopp <karsten@redhat.de> 2.7.0-8
- #97513, iptraf executable is 0700

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Dec 21 2002 Karsten Hopp <karsten@redhat.de>
- new URL
 
* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Mon Jul 15 2002 Karsten Hopp <karsten@redhat.de> 2.7.0-3
- add missingok for /var/run/iptraf/ files (#68780)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Karsten Hopp <karsten@redhat.de> 2.7.0-1
- update to fix stale locks when IPTraf did not start due to an
  improper terminal size.
- this update adds support for wireless LAN interfaces (wlan*, wvlan*).

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb 22 2002 Karsten Hopp <karsten@redhat.de>
- build with gcc-3x

* Fri Feb 22 2002 Karsten Hopp <karsten@redhat.de>
- added missing define
- rebuild in new environment

* Wed Jan 23 2002 Karsten Hopp <karsten@redhat.de> (2.5.0-2)
- fix #55243 (unable to tag this process)

* Tue Jan 22 2002 Karsten Hopp <karsten@redhat.de>
- Update to 2.5.0

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jul 24 2001 Karsten Hopp <karsten@redhat.de>
- fix #49503 (BuildRequires)

* Sat Jul 07 2001 Karsten Hopp <karsten@redhat.de>
- Copyright -> License

* Mon May 28 2001 Karsten Hopp <karsten@redhat.de>
- really fix #42514

* Mon May 28 2001 Karsten Hopp <karsten@redhat.de>
- fix #42514 (executables had wrong permissions)

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- updated to 2.4.0
- built for distro

* Mon Jan 22 2001 Karsten Hopp <karsten@redhat.de>
- update to 2.3.1 which fixes these bugs:
- segfault in IP Traffic Monitor
- segfault in promiscuous mode management
- failure of filters when source or dest is 255.255.255.255
- statistics logging bug
- small buffer overrun in TCP timeout log
- unrecognized IP display and filter code
- segfault bug when sorting an empty TCP window

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Thu Jul 13 2000 Karsten Hopp <karsten@redhat.de>
- rebuilt

* Wed Jun 28 2000 Karsten Hopp <karsten@redhat.de>
- fixed mandir
- changed install routine to allow building as non-root

* Mon May 15 2000 Tim Powers <timp@redhat.com>
- updated to 2.2.0

* Fri Nov 12 1999 Tim Powers <timp@redhat.com>
- updated to 2.1.0
- gzip man pages

* Wed Jul 28 1999 Tim Powers <timp@redhat.com>
- updated to version 2.0.2
- new patch added to that the spec file isn't out of control
  in the install section
- general spec cleanups
- built for 6.1

* Sat Apr 18 1999 Michael Maher <mike@redhat.com>
- built package for 6.0

* Sat Jan 16 1999 Anders Semb Hermansen <ahermans@vf.telia.no>
- Updated to version 1.4.2
- Used name and version variables in source field

* Wed Jan 6 1999 Anders Semb Hermansen <ahermans@vf.telia.no>
- Maintainer for RHCN: Anders Semb Hermansen
