Name:       jetxceldesk
Version:    1.4.5
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://jetxceldesk.com
Vendor:     jetxceldesk <info@jetxceldesk.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/jetxceldesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/jetxceldesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/jetxceldesk.service -t "%{buildroot}/usr/share/jetxceldesk/files"
install -Dm 644 $HBB/res/jetxceldesk.desktop -t "%{buildroot}/usr/share/jetxceldesk/files"
install -Dm 644 $HBB/res/jetxceldesk-link.desktop -t "%{buildroot}/usr/share/jetxceldesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/jetxceldesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/jetxceldesk.svg"

%files
/usr/share/jetxceldesk/*
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
ln -sf /usr/share/jetxceldesk/jetxceldesk /usr/bin/jetxceldesk
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
    rm /usr/bin/jetxceldesk || true
    rmdir /usr/lib/jetxceldesk || true
    rmdir /usr/local/jetxceldesk || true
    rmdir /usr/share/jetxceldesk || true
    rm /usr/share/applications/jetxceldesk.desktop || true
    rm /usr/share/applications/jetxceldesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/jetxceldesk || true
    rmdir /usr/local/jetxceldesk || true
  ;;
esac
