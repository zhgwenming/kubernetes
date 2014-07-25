%global debug_package %{nil}

Name:		kubernetes
Version:	beta1
Release:	2%{?dist}
Summary:	kubernetes orchestration tool

License:	ASL 2.0
URL:		https://github.com/GoogleCloudPlatform/%{name}/
Source0:	https://github.com/GoogleCloudPlatform/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz
Source1:	kubernetes.service
#Source2:	kubernetes.socket

BuildRequires:	golang
BuildRequires:	systemd

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
kubernetes orchestration tool

%prep
%setup -q

%build
sed -i '/version-gen.sh/s/^/#/' hack/build-go.sh
hack/build-go.sh

%install

install -D -p  output/go/bin/kubelet %{buildroot}%{_bindir}/kubelet
install -D -p  output/go/bin/proxy %{buildroot}%{_bindir}/proxy
install -D -p  output/go/bin/apiserver %{buildroot}%{_bindir}/apiserver
install -D -p  output/go/bin/controller-manager %{buildroot}%{_bindir}/controller-manager
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
#install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.socket

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%{_bindir}/kubelet
%{_bindir}/apiserver
%{_bindir}/proxy
%{_bindir}/controller-manager
%{_unitdir}/%{name}.service
#%{_unitdir}/%{name}.socket
%doc LICENSE README.md

%changelog
* Fri Jul 25 2014 Albert Zhang <zhgwenming@gmail.com> - beta1-1
- initial version


