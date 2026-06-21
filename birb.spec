#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Library of GLib utilities
Summary(pl.UTF-8):	Biblioteka narzędzi GLib
Name:		birb
Version:	0.7.1
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/pidgin/%{name}-%{version}.tar.xz
# Source0-md5:	24c9e819ab4bedd3ac45d20553c40eeb
URL:		https://keep.imfreedom.org/birb/birb/
# C17
BuildRequires:	gcc >= 6:7
%{?with_apidocs:BuildRequires:	gi-docgen >= 2025.3}
BuildRequires:	glib2-devel >= 1:2.76.0
BuildRequires:	meson >= 1.1.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel >= 1:1.54.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.76.0
Requires:	pango >= 1:1.54.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library of utilities for GLib based applications.

%description -l pl.UTF-8
Biblioteka narzędzia dla aplikacji opartych na bibliotece GLib.

%package devel
Summary:	Header files for birb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki birb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.76.0
Requires:	pango-devel >= 1:1.54.0

%description devel
Header files for birb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki birb.

%package static
Summary:	Static birb library
Summary(pl.UTF-8):	Statyczna biblioteka birb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static birb library.

%description static -l pl.UTF-8
Statyczna biblioteka birb.

%package apidocs
Summary:	API documentation for birb library
Summary(pl.UTF-8):	Dokumentacja API biblioteki birb
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for birb library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki birb.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' scripts/birb-check-license-headers

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_apidocs:-Ddocs=false}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/birb $RPM_BUILD_ROOT%{_gidocdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%{_libdir}/libbirb.so.*.*.*
%ghost %{_libdir}/libbirb.so.0
%{_libdir}/girepository-1.0/Birb-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/birb-check-license-headers
%{_libdir}/libbirb.so
%{_includedir}/birb-1.0
%{_datadir}/gir-1.0/Birb-1.0.gir
%{_pkgconfigdir}/birb.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbirb.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/birb
%endif
