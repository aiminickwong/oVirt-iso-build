%global product_family oVirt Node
%global product_release %{version} (0)
%global mgmt_scripts_dir %{_sysconfdir}/node.d
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%define is_f16 %(test "0%{?fedora}" == "016" && echo 1 || echo 0)
%define is_f20 %(test "0%{?fedora}" == "020" && echo 1 || echo 0)
%define is_min_f19 %(test "0%{?fedora}" -ge "019" && echo 1 || echo 0)
%define is_fedora_systemd %(test 0%{?fedora} -ne 0 && test %{?fedora} -ge 16 && echo 1 || echo 0)
%define is_rhel_systemd %(test 0%{?rhel} -ne 0 && test %{?rhel} -ge 7 && echo 1 || echo 0)
%define is_centos_systemd %(test 0%{?centos} -ne 0 && test %{?centos} -ge 7 && echo 1 || echo 0)
%define is_systemd %( test %{is_rhel_systemd} -eq 1 || test %{is_centos_systemd} = 1 || test %{is_fedora_systemd} = 1 && echo 1 || echo 0)
%define dracutdir %(test -e /usr/share/dracut && echo "/usr/share/dracut/modules.d" || echo "/usr/lib/dracut/modules.d")
%define is_el6 %(test 0%{?centos} -eq 06 || test 0%{?rhel} -eq 06 && echo 1 || echo 0)

# Igor can only be shipped on Fedora (because of python-uinput)
%define with_igor 0%{?is_min_f19}

# The minimizer is only bundled on el6, because it is available on Fedora
%define with_minimizer 0%{?is_el6}

# RHN Plugin is only build on RHEL
%define with_rhn 0%{?rhel}

%define dist_ocselected .ocselected.4.1

%global         package_version 3.1.0_master
%global         package_name ovirt-node-image

Summary:        The %{product_family} daemons/scripts
Name:           ovirt-node
Version:        3.1.0
Release:        3%{?dist_ocselected}
Source0:        http://plain.resources.ovirt.org/pub/ovirt-master-snapshot/src/%{name}/%{name}-%{package_version}.tar.gz
License:        GPLv2+
Group:          Applications/System

URL:            http://www.ovirt.org/
BuildRequires:  python-setuptools python-devel dracut
BuildRequires:  automake autoconf
%if %{is_systemd}
BuildRequires:  systemd-units
%endif
BuildRequires:  python-lockfile

Requires(post):  /sbin/chkconfig
Requires(preun): /sbin/chkconfig
%if %{is_systemd}
Requires:       systemd-units
Requires(post):     systemd-units
Requires(preun):    systemd-units
Requires:       python-IPy
%endif
%if ! 0%{?is_el6}
Requires:       python-augeas
%endif
Requires:       glusterfs-client >= 2.0.1
Requires:       system-release
Requires:       augeas >= 0.3.5
Requires:       bridge-utils
Requires:       udev >= 147-2.34
Requires:       wget
Requires:       cyrus-sasl-gssapi cyrus-sasl >= 2.1.22
Requires:       iscsi-initiator-utils
Requires:       ntp
Requires:       nfs-utils
Requires:       bash
Requires:       chkconfig
Requires:       bind-utils
Requires:       qemu-img
Requires:       nc
Requires:       /usr/sbin/crond
Requires:       newt-python
Requires:       libuser-python >= 0.56.9
Requires:       dbus-python
Requires:       python-gudev
Requires:       python-urwid
Requires:       python-lockfile
Requires:       python-lxml
Requires:       PyPAM
Requires:       ethtool
Requires:       cracklib-python
Requires:       dracut
Requires:       openssh-server
%if %{is_el6}
Requires:       /bin/hostname
%else
Requires:       hostname
%endif
Requires:       tuned
%if %{is_min_f19}
Requires:       NetworkManager
%endif
%if 0%{?is_systemd}
Requires:       grub2
%else
Requires:       grub
# for applying patches in %post
Requires(post):       patch
%endif
Requires:       system-release

Requires:       %{name}-selinux = %{version}-%{release}
Requires:       %{name}-branding-ovirt = %{version}-%{release}

#libvirt dependencies
Requires: libvirt-python
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
Requires: libvirt-daemon >= 1.0.2-1
Requires: libvirt-daemon-config-nwfilter
Requires: libvirt-daemon-driver-network
Requires: libvirt-daemon-driver-nwfilter
Requires: libvirt-daemon-driver-qemu
%else
%if 0%{?rhel}
Requires: libvirt >= 0.10.2-18.el6_4.4
%else
Requires: libvirt >= 1.0.2-1
%endif
%endif


BuildArch:      noarch

%define app_root %{_datadir}/%{name}

%description
Provides a series of daemons and support utilities for hypervisor distribution.


%package recipe
Summary:        Recipes for building and running %{product_family} images
Group:          Applications/System
Requires:       pykickstart  >= 1.54
%if 0%{?centos}
Requires:       livecd-tools >= 13.4.4
%else
Requires:       livecd-tools >= 1:16.0
%endif
Obsoletes:      ovirt-node-tools <= 2.3.0-999

%define recipe_root %{_datadir}/ovirt-node-recipe

%description recipe
This package provides recipe (Kickstart files), client tools,
documentation for building and running an %{product_family} image.
This package is not to be installed on the %{product_family},
however on a development machine to help to build the image.


%package tools
Summary:        Tools for working with plugins on %{product_family} images
Group:          Applications/System
%if 0%{?centos}
Requires:       livecd-tools >= 13.4.4
%else
Requires:       livecd-tools >= 1:16.0
%endif
Requires:       ovirt-node-minimizer
Requires:       libselinux-python

%define tools_root %{_datadir}/ovirt-node-tools

%description tools
This package provides plugin tools for modifying and working with the
%{product_family} image.
This package is not to be installed on the %{product_family},
however on a development machine to work with the image.

%package plugin-ipmi
Summary:        Ipmi plugin for %{product_family} image
Group:          Applications/System
Requires:       ipmitool
Requires:       OpenIPMI

%description plugin-ipmi
This package provides a ipmi plugin for use with %{product_family} image.

%package plugin-puppet
Summary:        Puppet plugin for %{product_family} image
Group:          Applications/System
Requires:       puppet

%description plugin-puppet
This package provides a puppet plugin for use with %{product_family} image.

%post plugin-puppet
%if %{is_el6}
patch -d /usr/lib/ruby/site_ruby/1.8/facter -p0 < \
%else
patch -d /usr/share/ruby/vendor_ruby/facter -p0 < \
%endif
   %{app_root}/puppet-plugin/puppet-operatingsystem.rb.patch
cd /etc/puppet
patch -p0 << EOF
--- puppet.conf 2013-03-21 14:55:43.969130799 -0700
+++ puppet.conf.new 2013-03-21 14:56:02.690178578 -0700
@@ -1,4 +1,6 @@
 [main]
+#    server = ""
+#    certname = ""
     # The Puppet log directory.
     # The default value is '$vardir/log'.
     logdir = /var/log/puppet
EOF

%if %{is_el6}
echo 'files /var/lib/puppet' >> /etc/rwtab
%endif


%package plugin-snmp
Summary:        SNMP plugin for %{product_family} image
Group:          Applications/System
Requires:       net-snmp
Requires:       net-snmp-utils
Requires:       perl-libs

%define snmp_root %{_datadir}/%{name}

%description plugin-snmp
This package provides an snmp plugin tools for use with%{product_family} image.

%post plugin-snmp
%if %{is_systemd}
systemctl enable snmpd.service
%else
chkconfig snmpd on
%endif

cat > /etc/snmp/snmpd.conf << \EOF_snmpd
master agentx
dontLogTCPWrappersConnects yes
rwuser root auth .1
EOF_snmpd


%package plugin-cim
Summary:        CIM plugin for %{product_family} image
Group:          Applications/System
Requires:       libvirt-cim
Requires:       sblim-sfcb

%description plugin-cim
This package provides a cim plugin for use with%{product_family} image.

%post plugin-cim
# Hack for rhbz#1018063
# The only time this is a problem is if we're upgrading from a pre-
# plugin version to a newer node. Manually specify the GID so we don't
# end up with a different one on the new image
if [[ ! `egrep '^cim' /etc/group` ]]; then
    # Create a group
    if [[ ! `egrep '^.*?:.*?:501:' /etc/group` ]]; then
        # gid 501 isn't taken
        groupadd -g 501 cim
    else
        # Take whatever GID we get -- probably no conflicts
        groupadd cim
    fi
fi
useradd -g cim -G sfcb -s /sbin/nologin cim
%if ! %{is_systemd}
/sbin/chkconfig --add ovirt-cim
/sbin/chkconfig ovirt-cim on
%else
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    /bin/systemctl enable ovirt-cim >/dev/null 2>&1 || :
fi
%endif
#CIM related changes
# set read-only
echo "readonly = true;" > /etc/libvirt-cim.conf

#cleanup tmp directory from cim setup
rm -rf /tmp/cim_schema*


%if 0%{?with_rhn}
%package plugin-rhn
Summary:        RHN plugin for %{product_family} image
Group:          Applications/System
Requires:       subscription-manager
Requires:       rhn-virtualization-host
Requires:       rhn-setup
Requires:       virt-who

%description plugin-rhn
This package provides the necessary rhn plugin tools for use with%{product_family} image.
%endif


#
# SELinux subpackage
#
%global selinux_modulename ovirt
%global selinux_variants targeted
%if %{is_el6}
%global selinux_policyver %(%{__sed} -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp || echo 0.0.0)
%else
%global selinux_policyver %_selinux_policy_version
%endif

%package selinux
Summary:          SELinux policy module supporting %{product_family}
Group:            System Environment/Base
BuildRequires:    policycoreutils, checkpolicy
BuildRequires:    selinux-policy-devel >= %{selinux_policyver}
BuildRequires:    /usr/share/selinux/devel/policyhelp, hardlink
%if "%{selinux_policyver}" != ""
Requires:         selinux-policy >= %{selinux_policyver}
%endif
Requires:         %{name} = %{version}-%{release}
Requires:         selinux-policy-base
Requires(post):   policycoreutils
Requires(postun): policycoreutils

%description selinux
SELinux policy module supporting %{product_family}

%post selinux
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{selinux_modulename}.pp
done
# Is this to greedy?
/sbin/restorecon -R / || :

# set SELinux booleans
# rhbz#502779 restrict certain memory protection operations
#     keep allow_execmem on for grub
# rhbz#642209 allow virt images on NFS
/usr/sbin/setsebool -P allow_execstack=0 \
                       virt_use_nfs=1 \
                       virt_use_sanlock=1 \
                       sanlock_use_nfs=1


%postun selinux
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
     /usr/sbin/semodule -s ${selinuxvariant} -r %{selinux_modulename} &> /dev/null || :
  done
  # Is this to greedy?
  /sbin/restorecon -R / &> /dev/null || :
fi

# FIXME what about semanage?


#
# Igor service subpackage
#
%if 0%{?with_igor}
%package plugin-igor-slave
Summary:        Igor slave plugin for %{product_family}
Group:          Applications/System

Requires:       igor-common
%if 0%{?is_systemd}
BuildRequires:  systemd-units
Requires:       systemd
%else
BuildRequires:  initscripts
Requires(post): chkconfig
%endif

# We need python-uinput for TUI tests
Requires:       python-uinput


%description plugin-igor-slave
This package provides an igor service for %{product_family}. This service
is responsible for running testcase offered by an igor server.


%post plugin-igor-slave
%if 0%{?is_systemd}
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    /bin/systemctl enable ovirt-node-igor-slave.service >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --add ovirt-node-igor-slave >/dev/null 2>&1 || :
%endif


%preun plugin-igor-slave
%if ! %{is_systemd}
if [ $1 = 0 ] ; then
    /sbin/service ovirt-node-igor-slave stop >/dev/null 2>&1
    /sbin/chkconfig --del ovirt-node-igor-slave
fi
%else
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable ovirt-node-igor-slave.service > /dev/null 2>&1 || :
    /bin/systemctl stop ovirt-node-igor-slave.service > /dev/null
fi
%endif

# </Igor service subpackage>
%endif


#
# minimizer subpackage
#
%if 0%{?with_minimizer}
%package minimizer
Summary:        The image-minimizer tool
Group:          Applications/System
Obsoletes:      appliance-tools-minimizer


%description minimizer
This package ships the image-minimizer tool.
This tool is used to remove unneeded rpms and files from a filesystem tree.

# </minimizer subpackage>
%endif


#
# oVirt Brand subpackage
#
%package branding-ovirt
Summary:  oVirt branding for oVirt Node
Group:    Applications/System

%description branding-ovirt
This package contains the files to let Node appear in the oVirt look.



%prep
%setup -q -n "%{name}-%{package_version}"


%build
aclocal && autoheader && automake --add-missing && autoconf


%configure --with-image-minimizer 
make

# Build SELinux policy module
cd semodule
for selinuxvariant in %{selinux_variants}
do
    %{__make} NAME=${selinuxvariant} \
        -f %{?policy_devel_root}%{_datadir}/selinux/devel/Makefile
    mv -v %{selinux_modulename}.pp %{selinux_modulename}.pp.${selinuxvariant}
done
cd -


%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot}
%{__install} -d -m0755 %{buildroot}%{_libexecdir}/ovirt-node/hooks
%{__install} -d -m0755 %{buildroot}%{_libexecdir}/ovirt-node/hooks/pre-upgrade
%{__install} -d -m0755 %{buildroot}%{_libexecdir}/ovirt-node/hooks/post-upgrade
%{__install} -d -m0755 %{buildroot}%{_libexecdir}/ovirt-node/hooks/rollback
%{__install} -d -m0755 %{buildroot}%{_libexecdir}/ovirt-node/hooks/on-boot
%{__install} -d -m0755 %{buildroot}%{_libexecdir}/ovirt-node/hooks/on-changed-boot-image

%if %{is_f16}
# install libvirtd systemd service
%{__install} -p -m0644 libvirtd.service %{buildroot}%{_unitdir}
%endif
%if ! %{is_systemd}
# install libvirtd upstart job
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/init
%{__install} -p -m0644 libvirtd.upstart %{buildroot}%{_sysconfdir}/init/libvirtd.conf
%endif

# dracut patches for rhel6
%if ! %{is_systemd}
%{__install} -p -m0644 dracut/dracut-7ed4ff0636c74a2f819ad6e4f2ab4862.patch %{buildroot}%{app_root}

%endif

# python-augeas is not in RHEL-6
%if 0%{?is_el6}
# specific version of python-augeas is not available in Fedora yet
%{__install} -p -m0644 scripts/augeas.py %{buildroot}%{python_sitelib}
%endif

# Install SELinux policy module
cd semodule
%{__install} -d %{buildroot}%{_datadir}/selinux
for selinuxvariant in %{selinux_variants}
do
    %{__install} -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
    %{__install} -p -m 644 %{selinux_modulename}.pp.${selinuxvariant} \
               %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{selinux_modulename}.pp
done
cd -

/usr/sbin/hardlink -cv %{buildroot}%{_datadir}/selinux

# Keep old name for backwards compatibilitiy reasons
ln -vfs %{_bindir}/ovirt-node-config-password %{buildroot}%{_libexecdir}/ovirt-config-password

# Remove igor stuff if not needed
%if ! 0%{?with_igor}
%{__rm} -vf %{buildroot}/%{_libexecdir}/ovirt-node-igor-slave \
            %{buildroot}/%{_unitdir}/ovirt-node-igor-slave.service \
            %{buildroot}/%{_initrddir}/ovirt-node-igor-slave
%endif

# Remove minimizer if unneeded
%if ! 0%{?with_minimizer}
%{__rm} -vf %{buildroot}/%{_sbindir}/image-minimizer
%endif

# Remove rhn stuff if not needed
%if ! 0%{?with_rhn}
%{__rm} -vf %{buildroot}/%{python_sitelib}/ovirt/node/setup/rhn/* \
            %{buildroot}/%{_sysconfdir}/ovirt-commandline.d/rhn_autoinstall_args \
            %{buildroot}/%{_sysconfdir}/ovirt-config-boot.d/rhn_autoinstall.py*
rmdir %{buildroot}/%{python_sitelib}/ovirt/node/setup/rhn/
%endif

# Remove augeas.py if not needed
%if ! 0%{?is_el6}
%{__rm} -vf %{buildroot}/%{python_sitelib}/augeas*
%endif


%clean
%{__rm} -rf %{buildroot}


%post
/sbin/chkconfig --level 35 netconsole off
%if ! %{is_systemd}
/sbin/chkconfig --add ovirt-awake
/sbin/chkconfig --add ovirt-early
/sbin/chkconfig --add ovirt-firstboot
/sbin/chkconfig --add ovirt
/sbin/chkconfig --add ovirt-post
/sbin/chkconfig --add ovirt-kdump
%else
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    /bin/systemctl --no-reload enable ovirt-firstboot.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload enable ovirt.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload enable ovirt-post.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload enable ovirt-early.service > /dev/null 2>&1 || :
fi
%endif
# workaround for imgcreate/live.py __copy_efi_files
if [ ! -e /boot/grub/splash.xpm.gz ]; then
  cp %{app_root}/grub-splash.xpm.gz /boot/grub/splash.xpm.gz
fi
%if ! %{is_systemd}
# apply dracut fixes not in rhel6
# rhbz#683330
# dracut.git commits rediffed for dracut-004-336.el6
patch -d /usr/share/dracut/ -p0 < %{app_root}/dracut-7ed4ff0636c74a2f819ad6e4f2ab4862.patch

%endif

#Disable X11Forwarding for sshd
sed -i -e 's/X11Forwarding yes/X11Forwarding no/' /etc/ssh/sshd_config

#release info for dracut to pick it up into initramfs
# remove symlink to keep original redhat-release
rm -f /etc/system-release
echo "%{product_family} release %{product_release}" > /etc/system-release


%pre
#
# ovirt-node must not be upgraded.
# It is intended to only be installed.
# Upgrades happen on an image basis
#
if [[ $1 -eq 2 ]] ; then
    echo "Upgrade ovirt-node as a package is not supported."
    exit 42
fi


%preun
#
# ovirt-node must not be uninstalled.
# It is intended to only be installed.
# Upgrades happen on an image basis
#
echo "Upgrade/Uninstalling ovirt-node as a package is not supported."
exit 42

# Keeping the rest if it is possible one day
/sbin/chkconfig --level 35 netconsole off
%if ! %{is_systemd}
if [ $1 = 0 ] ; then
    /sbin/service ovirt-early stop >/dev/null 2>&1
    /sbin/service ovirt-firstboot stop >/dev/null 2>&1
    /sbin/service ovirt stop >/dev/null 2>&1
    /sbin/service ovirt-post stop >/dev/null 2>&1
    /sbin/chkconfig --del ovirt-awake
    /sbin/chkconfig --del ovirt-early
    /sbin/chkconfig --del ovirt-firstboot
    /sbin/chkconfig --del ovirt
    /sbin/chkconfig --del ovirt-post
fi
%else
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable ovirt-firstboot.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable ovirt.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable ovirt-post.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable ovirt-early.service > /dev/null 2>&1 || :

    /bin/systemctl stop ovirt.service > /dev/null
    /bin/systemctl stop ovirt-post.service > /dev/null
    /bin/systemctl stop ovirt-early.service > /dev/null
fi
%endif


%preun plugin-cim
%if ! %{is_systemd}
if [ $1 = 0 ] ; then
    /sbin/service ovirt-cim stop >/dev/null 2>&1
    /sbin/chkconfig --del ovirt-cim
fi
%else
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable ovirt-cim.service > /dev/null 2>&1 || :
    /bin/systemctl stop ovirt-cim.service > /dev/null
fi
%endif


#
# FILES
#
%files recipe
%defattr(0644,root,root,0755)
%doc README COPYING
%{recipe_root}/*.ks
%defattr(0755,root,root,0755)
%{_mandir}/man8/node-creator.8.gz
%{_sbindir}/node-creator


%files tools
%{_sbindir}/edit-node
%{_sbindir}/testable-node
%{_mandir}/man8/edit-node.8.gz

%files plugin-ipmi
%{python_sitelib}/ovirt/node/setup/ipmi/__init__.py*
%{python_sitelib}/ovirt/node/setup/ipmi/ipmi_page.py*

%files plugin-puppet
%{python_sitelib}/ovirt/node/setup/puppet/__init__.py*
%{python_sitelib}/ovirt/node/setup/puppet/puppet_page.py*
%{_localstatedir}/lib/puppet/facts/ovirt.rb
%{_sysconfdir}/ovirt-plugins.d/puppet.minimize
%{_sysconfdir}/ovirt-commandline.d/puppet-args
%{app_root}/puppet-plugin/puppet-operatingsystem.rb.patch
%{_sysconfdir}/ovirt-config-boot.d/puppet_autoinstall.py*

%files plugin-snmp
%{python_sitelib}/ovirt_config_setup/snmp.py*
%{python_sitelib}/ovirt/node/setup/snmp/__init__.py*
%{python_sitelib}/ovirt/node/setup/snmp/snmp_model.py*
%{python_sitelib}/ovirt/node/setup/snmp/snmp_page.py*
%{_sysconfdir}/ovirt-plugins.d/snmp.minimize
%{_sysconfdir}/ovirt-config-boot.d/snmp_autoinstall.py*


%files plugin-cim
%{python_sitelib}/ovirt_config_setup/cim.py*
%{python_sitelib}/ovirt/node/setup/cim/__init__.py*
%{python_sitelib}/ovirt/node/setup/cim/cim_model.py*
%{python_sitelib}/ovirt/node/setup/cim/cim_page.py*
%{_sysconfdir}/ovirt-plugins.d/cim.minimize
%{_sysconfdir}/ovirt-commandline.d/cim-args
%{_sysconfdir}/ovirt-config-boot.d/cim_autoinstall.py*
%if %{is_systemd}
%{_unitdir}/ovirt-cim.service
%else
%{_initrddir}/ovirt-cim
%endif

%if 0%{?with_igor}
%files plugin-igor-slave
%{_libexecdir}/ovirt-node-igor-slave
%if %{is_systemd}
%{_unitdir}/ovirt-node-igor-slave.service
%else
%{_initrddir}/ovirt-node-igor-slave
%endif
%endif


%if 0%{?with_rhn}
%files plugin-rhn
%{python_sitelib}/ovirt/node/setup/rhn/__init__.py*
%{python_sitelib}/ovirt/node/setup/rhn/rhn_model.py*
%{python_sitelib}/ovirt/node/setup/rhn/rhn_page.py*
%{_sysconfdir}/ovirt-commandline.d/rhn_autoinstall_args
%{_sysconfdir}/ovirt-config-boot.d/rhn_autoinstall.py*
%endif


%files selinux
%defattr(-,root,root,0755)
%doc semodule/*.fc semodule/*.te
%{_datadir}/selinux/*/%{selinux_modulename}.pp


%if 0%{?with_minimizer}
%files minimizer
%{_sbindir}/image-minimizer
%endif


%files branding-ovirt
%{python_sitelib}/ovirt/node/presets.py*


%files
%defattr(-,root,root)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/default/ovirt

%config(noreplace) %{_sysconfdir}/logrotate.d/ovirt-node
%config(noreplace) %{_sysconfdir}/cron.d/ovirt-logrotate

%{mgmt_scripts_dir}
%dir %{_sysconfdir}/ovirt-config-boot.d
%{_sysconfdir}/ovirt-config-boot.d/local_boot_trigger.sh

%if %{is_f16}
%{_unitdir}/libvirtd.service
%endif
%if ! %{is_systemd}
%{_sysconfdir}/init/libvirtd.conf
%endif
%{_sysconfdir}/ovirt-node/logging.conf
%{_sysconfdir}/ovirt-node/logging.debug.conf
%{_sysconfdir}/sysconfig/modules/vlan.modules
%{_sysconfdir}/modprobe.d/ovirt-qla4xxx.conf
%{_sysconfdir}/modprobe.d/bonding.conf
%{_libexecdir}/ovirt-node/hooks


%doc COPYING
# should be ifarch i386
%{app_root}/grub-splash.xpm.gz
# end i386 bits
%{app_root}/syslinux-vesa-splash.jpg
%if ! %{is_systemd}
%{app_root}/dracut-7ed4ff0636c74a2f819ad6e4f2ab4862.patch

%endif

%{dracutdir}/91ovirtnode
%{_sysconfdir}/dracut.conf.d/ovirt-dracut.conf
%{_libexecdir}/ovirt-auto-install
%{_libexecdir}/ovirt-config-uninstall
%{_libexecdir}/ovirt-functions
%{_libexecdir}/ovirt-admin-shell
%{_libexecdir}/ovirt-config-password
%{_libexecdir}/ovirt-init-functions.sh
%{_sbindir}/persist
%{_sbindir}/unpersist
%{_sbindir}/ovirt-node-upgrade
%{_sbindir}/ovirt-node-register
%{python_sitelib}/ovirt_config_setup
%exclude %{python_sitelib}/ovirt_config_setup/cim.py*
%exclude %{python_sitelib}/ovirt_config_setup/snmp.py*
%{python_sitelib}/ovirtnode
%if 0%{?is_el6}
%{python_sitelib}/augeas*
%endif
%{_sysconfdir}/ovirt-early.d
%dir %{_sysconfdir}/ovirt-commandline.d
%if %{is_systemd}
%{_unitdir}/ovirt.service
%{_unitdir}/ovirt-awake.service
%{_unitdir}/ovirt-firstboot.service
%{_unitdir}/ovirt-post.service
%{_unitdir}/ovirt-early.service
%{_unitdir}/ovirt-kdump.service
%else
%{_initrddir}/ovirt-awake
%{_initrddir}/ovirt-early
%{_initrddir}/ovirt-firstboot
%{_initrddir}/ovirt
%{_initrddir}/ovirt-post
%{_initrddir}/ovirt-kdump
%endif
# Files related to the new TUI
%{python_sitelib}/ovirt/__init__.py*
%{python_sitelib}/ovirt/node/*.py*
%{python_sitelib}/ovirt/node/ui/*.py*
%{_datadir}/locale/zh_CN/LC_MESSAGES/*.mo
%{_datadir}/locale/en_US/LC_MESSAGES/*.mo
%{_datadir}/locale/pt_BR/LC_MESSAGES/*.mo
%{python_sitelib}/ovirt/node/utils/*.py*
%{python_sitelib}/ovirt/node/utils/fs/*.py*
%{python_sitelib}/ovirt/node/tools/*.py*
%{python_sitelib}/ovirt/node/tools/*.xsl
%{python_sitelib}/ovirt/node/config/*.py*
%exclude %{python_sitelib}/ovirt/node/presets.py*
%{python_sitelib}/ovirt/node/setup/*.py*
%{python_sitelib}/ovirt/node/setup/core/*.py*
%{python_sitelib}/ovirt/node/installer/*.py*
%{python_sitelib}/ovirt/node/installer/core/*.py*
%exclude %{python_sitelib}/ovirt/node/setup/snmp/*.py*
%exclude %{python_sitelib}/ovirt/node/setup/cim/*.py*
%{_bindir}/ovirt-node-setup
%{_bindir}/ovirt-node-installer
%{_bindir}/ovirt-node-doc
%{_bindir}/ovirt-node-features
%{_bindir}/ovirt-node-config
%{_bindir}/ovirt-node-config-password



%changelog
* Sat Dec 23 2014 Zhao Chao <zhaochao1984@gmail.com> 3.1.0-3-ocselected.4.1
- update chinese locale file.

* Sat Dec 20 2014 Zhao Chao <zhaochao1984@gmail.com> 3.1.0-2-ocselected.4.1
- merge upstream to cf277e10bb0191a392e27605659935db1ce32f15.
- fix default iscsi iname substituion.
- add two i18n strings for OCselected-oVirt.
- remove the Plugins page.

* Mon Dec 15 2014 Zhao Chao <zhaochao1984@gmail.com> 3.1.0-1-ocselected.4.1
- setup/core/remote_storage_page: replace Red Hat with OCselected.

* Mon Jun 20 2011 Alan Pevec <apevec@redhat.com> 2.0.0-1
- split kickstarts per distro, currently ovirt15 and rhevh6
- new installation and configuration text UI for standalone mode
- drop gptsync, make it noarch

* Tue Apr 06 2010 Darryl L. Pierce <dpierce@redhat.com> - 1.9.2-1
- Updated autoconf environment.
- Allow persistence of empty configuration files.

* Wed Mar 24 2010 Darryl L. Pierce <dpierce@redhat.com> - 1.9.1-1
- Update ovirt-process-config to fail configs that are missing the field name or value.
- Updated build system will use Fedora 13 as the rawhide repo.
- Fixed ovirt-config-networking to not report success when network start fails.
- Reboot hangs on /etc [FIXED].
- Multipath translation performance improvements.
- Cleanup ROOTDRIVE when partitioning.
- Fix hang when cleaning dirty storage.
- The order of the oVirt SysVInit scripts has been changed.
-   ovirt-early -> ovirt-awake -> ovirt -> ovirt-post
- Fixes to the SysVINit scripts to name lifecycle methods propery.
- Added psmisc package.
- Added default KEYTAB_FILE name to /etc/sysconfig/node-config.
- Fixes to the persist and unpersist commands to handle already persisted files and directories.
- Duplicate NTP/DNS entries are rejected during network setup.

* Wed Oct 07 2009 David Huff <dhuff@redhat.com> - 1.0.3-4
- Added ovirt-node-tools subpackage

* Tue Jun 23 2009 David Huff <dhuff@redhat.com> - 1.0.3
- Clean up spec for inclusion in Fedora
- Removed subpackages, stateful, stateless, logos, and selinux

* Thu Dec 11 2008 Perry Myers <pmyers@redhat.com> - 0.96
- Subpackage stateful/stateless to separate out functionality for
  embedded Node and Node running as part of already installed OS
- ovirt-config-* setup scripts for standalone mode

* Thu Sep 11 2008 Chris Lalancette <clalance@redhat.com> - 0.92 0.7
- Add the ovirt-install- and ovirt-uninstall-node scripts, and refactor
  post to accomodate

* Mon Sep  8 2008 Jim Meyering <meyering@redhat.com> - 0.92 0.6
- Update ovirt-identify-node's build rule.

* Fri Aug 22 2008 Chris Lalancette <clalance@redhat.com> - 0.92 0.5
- Add the ovirt-listen-awake daemon to the RPM

* Fri Aug 22 2008 Chris Lalancette <clalance@redhat.com> - 0.92 0.4
- Re-arrange the directory layout, in preparation for ovirt-listen-awake

* Tue Jul 29 2008 Perry Myers <pmyers@redhat.com> - 0.92 0.2
- Added /etc/ovirt-release and merged ovirt-setup into spec file

* Wed Jul 02 2008 Darryl Pierce <dpierce@redhat.com> - 0.92 0.2
- Added log rotation to limit file system writes.

* Mon Jun 30 2008 Perry Myers <pmyers@redhat.com> - 0.92 0.1
- Add in sections of kickstart post, general cleanup
