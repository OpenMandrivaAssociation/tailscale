%global debug_package %{nil}

Name:		tailscale
Version:	1.86.2
Release:	1
Source0:	https://github.com/tailscale/tailscale/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:    %{name}-%{version}-vendor.tar.gz
Summary:	The easiest, most secure way to use WireGuard and 2FA
URL:		https://github.com/tailscale/tailscale
License:	BSD-3-Clause
Group:		Network/Remote access

BuildRequires:	go

%description
%summary.

%prep
%autosetup -p1
tar -zxf %{S:1}

%build
go build tailscale.com/cmd/tailscale
go build tailscale.com/cmd/tailscaled

%install
install -Dm755 tailscale tailscaled -t %{buildroot}%{_bindir}
install -Dm644 cmd/tailscaled/tailscaled.defaults %{buildroot}%{_sysconfdir}/default/tailscaled
install -Dm644 cmd/tailscaled/tailscaled.service -t %{buildroot}%{_unitdir}

%post
%systemd_post tailscaled.service

%preun
%systemd_preun tailscaled.service

%postun
%systemd_postun tailscaled.service

%files
%{_sysconfdir}/default/tailscaled
%{_bindir}/%{name}
%{_bindir}/tailscaled
%{_unitdir}/tailscaled.service
%license LICENSE
