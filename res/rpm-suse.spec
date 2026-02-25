Name:       jetxceldesk
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/jetxceldesk/
mkdir -p %{buildroot}/usr/share/jetxceldesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/jetxceldesk %{buildroot}/usr/bin/jetxceldesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/jetxceldesk/libsciter-gtk.so
install $HBB/res/jetxceldesk.service %{buildroot}/usr/share/jetxceldesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/jetxceldesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/jetxceldesk.svg
install $HBB/res/jetxceldesk.desktop %{buildroot}/usr/share/jetxceldesk/files/
install $HBB/res/jetxceldesk-link.desktop %{buildroot}/usr/share/jetxceldesk/files/

%files
/usr/bin/jetxceldesk
/usr/share/jetxceldesk/libsciter-gtk.so
/usr/share/jetxceldesk/files/jetxceldesk.service
/usr/share/icons/hicolor/256x256/apps/jetxceldesk.png
/usr/share/icons/hicolor/scalable/apps/jetxceldesk.svg
/usr/share/jetxceldesk/files/jetxceldesk.desktop
/usr/share/jetxceldesk/files/jetxceldesk-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop jetxceldesk || true
  ;;
esac

%post
cp /usr/share/jetxceldesk/files/jetxceldesk.service /etc/systemd/system/jetxceldesk.service
cp /usr/share/jetxceldesk/files/jetxceldesk.desktop /usr/share/applications/
cp /usr/share/jetxceldesk/files/jetxceldesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable jetxceldesk
systemctl start jetxceldesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop jetxceldesk || true
    systemctl disable jetxceldesk || true
    rm /etc/systemd/system/jetxceldesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/jetxceldesk.desktop || true
    rm /usr/share/applications/jetxceldesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
