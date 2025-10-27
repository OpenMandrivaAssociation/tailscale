%global debug_package %{nil}

Name:		tailscale
Version:	1.90.2
Release:	1
Source0:	https://github.com/tailscale/tailscale/archive/v%{version}/%{name}-%{version}.tar.gz
# Dependency is only fetchable from proxy run commands below to vendor
# export GOPROXY=https://proxy.golang.org,direct
# go mod vendor
Source1:	%{name}-%{version}-vendor.tar.gz
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
export GOPROXY=https://proxy.golang.org,direct
export LDFLAGS="-s -w -X tailscale.com/version.longStamp=%{version} -X tailscale.com/version.shortStamp="
go build --buildmode=pie -o bin/%{name}cli ./cmd/%{name}
go build --buildmode=pie -o bin/%{name}d ./cmd/%{name}d

%install
install -Dm0755 bin/%{name}cli %{buildroot}%{_bindir}/%{name}cli
install -Dm0755 bin/%{name}d %{buildroot}%{_sbindir}/%{name}d
install -Dm0755 cmd/%{name}d/%{name}d.service %{buildroot}%{_unitdir}/%{name}d.service

%files
%license LICENSE
%doc README.md LICENSE PATENTS api.md SECURITY.md docs
%{_bindir}/%{name}cli
%{_bindir}/tailscaled
%{_unitdir}/tailscaled.service

