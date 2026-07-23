%global debug_package %{nil}

Name:		tailscale
Version:	1.98.8
Release:	1
Source0:	https://github.com/tailscale/tailscale/archive/v%{version}/%{name}-%{version}.tar.gz
# Unless patched, one dependency is only fetchable from proxy run commands below to vendor
# export GOPROXY=https://proxy.golang.org,direct
# go mod vendor

#Non export vendoring
#tar xf tailscale-1.98.8.tar.gz
#cd tailscale-1.98.8
#cp go.mod go.mod.omv~
#cp go.sum go.sum.omv~
#go mod edit -replace github.com/tdakkota/asciicheck=github.com/golangci/asciicheck@v0.2.0
#cat >> go.sum <<'EOF'
#github.com/golangci/asciicheck v0.2.0 h1:8XjfVwGLXloGLltr2AwcahnjbqXiYILwDWsQTvmglSE=
#github.com/golangci/asciicheck v0.2.0/go.mod h1:Qb7Y9EgjCLJGup51gDHFzbI08/gbGhL/UVhYIPWG2rg=
#EOF
#go mod vendor
#cd ..
#gendiff tailscale-1.98.8 .omv~ > tailscale-1.96.4-new-asciicheck-url.patch
#tar -cJf tailscale-1.98.8-vendor.tar.xz vendor

Source1:	%{name}-%{version}-vendor.tar.xz
Summary:	The easiest, most secure way to use WireGuard and 2FA
URL:		https://github.com/tailscale/tailscale
License:	BSD-3-Clause
Group:		Network/Remote access

BuildRequires:	go

%patchlist
tailscale-1.96.4-new-asciicheck-url.patch

%description
%summary.

%prep
%autosetup -p1
tar -zxf %{S:1}

%build
GO_LDFLAGS="\
	-linkmode=external \
	-X tailscale.com/version.longStamp=%{version} \
	-X tailscale.com/version.shortStamp=$(cut -d+ -f1 <<< "%{version}")"

go build --buildmode=pie -ldflags "$GO_LDFLAGS" -o bin/%{name} ./cmd/%{name}
go build --buildmode=pie -ldflags "$GO_LDFLAGS" -o bin/%{name}d ./cmd/%{name}d

%install
install -Dm0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm0755 bin/%{name}d %{buildroot}%{_sbindir}/%{name}d
install -Dm0755 cmd/%{name}d/%{name}d.service %{buildroot}%{_unitdir}/%{name}d.service
install -Dm644 cmd/tailscaled/tailscaled.defaults %{buildroot}%{_sysconfdir}/default/tailscaled

%files
%license LICENSE
%doc README.md LICENSE PATENTS api.md SECURITY.md docs
%{_bindir}/%{name}
%{_bindir}/tailscaled
%{_unitdir}/tailscaled.service
%{_sysconfdir}/default/tailscaled
