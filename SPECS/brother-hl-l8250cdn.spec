# Based on the archlinux PKGBUILD,
#   https://aur.archlinux.org/packages/brother-hl-l8250cdn/

Name:           brother-hl-l8250cdn
Version:        1.0
Release:        1%{?dist}
Summary:        LPR and CUPS driver for the Brother HL-L8250CDN

License:        Brother Commercial License
URL:            http://solutions.brother.com/linux/en_us/
Source0:        http://www.brother.com/pub/bsc/linux/packages/hll8250cdncupswrapper-1.1.3-1.i386.rpm
Source1:        http://www.brother.com/pub/bsc/linux/packages/hll8250cdnlpr-1.1.2-1.i386.rpm
Source2:        cupswrapper-license.txt
Source3:        lpr-license.txt

BuildRequires:  cpio
Requires:       cups-filesystem
Requires(post): policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils

# TODO: is this defined somewhere in CUPS RPM macros ?
%global _cups_serverbin     /usr/lib/cups
%global _wrapper_generator  ./opt/brother/Printers/hll8250cdn/cupswrapper/cupswrapperhll8250cdn

%description
Includes the driver for the Brother HL-L8250CDN networked laser printer,
as distributed by Brother.


%prep
rm -rf %{_builddir}/opt %{_builddir}/usr
rpm2cpio %{SOURCE0} | cpio -idmv
rpm2cpio %{SOURCE1} | cpio -idmv

# Create directories needed for wrapper script creation
install -d %{_builddir}/usr/share/cups/model
install -d %{_builddir}/usr/lib/cups/filter

# Patch wrapper script generator
sed -i '/^\/etc\/init.d\/cups/d' %{_wrapper_generator}
sed -i '/^sleep/d' %{_wrapper_generator}
sed -i '/^lpadmin/d' %{_wrapper_generator}
sed -i 's|/usr|$builddir/usr|g' %{_wrapper_generator}
sed -i 's|/opt|$builddir/opt|g' %{_wrapper_generator}
sed -i 's|/model/Brother|/model|g' %{_wrapper_generator}
sed -i 's|lpinfo|echo|g' %{_wrapper_generator}

# Remove print cap management component, done by CUPS
rm opt/brother/Printers/hll8250cdn/inf/setupPrintcapij

# Copy licenses
cp %{SOURCE2} %{_builddir}
cp %{SOURCE3} %{_builddir}


%build
# Run wrapper script generator
export builddir=%{_builddir}
./%{_wrapper_generator}

# Fix paths in generated wrapper
sed -i 's|$builddir||' usr/lib/cups/filter/*lpdwrapper*
sed -i "s|%{_builddir}||" usr/lib/cups/filter/*lpdwrapper*

# Remove wrapper generator
rm %{_wrapper_generator}


%install
cp -Rp %{_builddir}/usr $RPM_BUILD_ROOT
cp -Rp %{_builddir}/opt $RPM_BUILD_ROOT


%post
# TODO:
# See https://fedoraproject.org/wiki/PackagingDrafts/SELinux#File_contexts
# where it is suggested to update main SELinux policy instead which makes
# sense. We can then also drop the dependency on policycoreutils-python-utils.

setsebool -P cups_execmem 1
semanage fcontext -a -t cupsd_rw_etc_t '/opt/brother/Printers/hll8250cdn/inf(/.*)?'
semanage fcontext -a -t bin_t          '/opt/brother/Printers/hll8250cdn/lpd(/.*)?'
semanage fcontext -a -t bin_t          '/opt/brother/Printers/hll8250cdn/cupswrapper(/.*)?'
restorecon -R /opt/brother/Printers/hll8250cdn


%postun
# TODO: restore bool value for cups_execmem
semanage fcontext -d -t cupsd_rw_etc_t '/opt/brother/Printers/hll8250cdn/inf(/.*)?'
semanage fcontext -d -t bin_t          '/opt/brother/Printers/hll8250cdn/lpd(/.*)?'
semanage fcontext -d -t bin_t          '/opt/brother/Printers/hll8250cdn/cupswrapper(/.*)?'


%files
%license cupswrapper-license.txt lpr-license.txt
%{_bindir}/brprintconf_hll8250cdn
%{_datarootdir}/cups/model/brother_hll8250cdn_printer_en.ppd
%{_cups_serverbin}/filter/brother_lpdwrapper_hll8250cdn
/opt/brother/Printers/hll8250cdn


%changelog
* Mon Nov 19 2018 Stijn Hoop <stijn@sandcat.nl> 1.0-1
- Initial RPM version
