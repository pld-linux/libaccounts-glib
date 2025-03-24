#
# Conditional build:
%bcond_without	python2		# Python 2.x binding (deprecated, not supported upstream)
%bcond_without	static_libs	# static library
%bcond_without	tests		# testsuite build [switch broken in configure]

Summary:	Accounts management library for GLib applications
Summary(pl.UTF-8):	Biblioteka do zarządzania kontami dla aplikacji opartych na bibliotece GLib
Name:		libaccounts-glib
Version:	1.24
Release:	10
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://gitlab.com/accounts-sso/libaccounts-glib/tags
Source0:	https://gitlab.com/accounts-sso/libaccounts-glib/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	bdd91a93ec089547d2d186e9840575c5
URL:		https://gitlab.com/accounts-sso/libaccounts-glib
%{?with_tests:BuildRequires:	check-devel >= 0.9.4}
BuildRequires:	docbook-dtd43-xml
BuildRequires:	docbook-style-xsl-nons
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-progs
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-pygobject3-devel >= 3.0}
BuildRequires:	python3-pygobject3-devel >= 3.0
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.7.0
Requires:	glib2 >= 1:2.36
Requires:	sqlite3 >= 3.7.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project is a library for managing accounts which can be used from
GLib applications. It is part of the accounts-sso project.

%description -l pl.UTF-8
Ten projekt to biblioteka do zarządzania kontami, z której można
korzystać w aplikacjach opartych na bibliotece GLib. Jest to część
projektu accounts-sso.

%package devel
Summary:	Development files for libaccounts-glib library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libaccounts-glib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36
Requires:	libxml2-devel >= 2.0
Requires:	sqlite3-devel >= 3.7.0

%description devel
Development files for libaccounts-glib library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki libaccounts-glib.

%package static
Summary:	Static libaccounts-glib library
Summary(pl.UTF-8):	Statyczna biblioteka libaccounts-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libaccounts-glib library.

%description static -l pl.UTF-8
Statyczna biblioteka libaccounts-glib.

%package apidocs
Summary:	API documentation for libaccounts-glib library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libaccounts-glib
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libaccounts-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libaccounts-glib.

%package -n python-libaccounts-glib
Summary:	Python 2 bindings for libaccounts-glib
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki libaccounts-glib
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygobject3 >= 3

%description -n python-libaccounts-glib
Python 2 bindings for libaccounts-glib.

%description -n python-libaccounts-glib -l pl.UTF-8
Wiązania Pythona 2 do biblioteki libaccounts-glib.

%package -n python3-libaccounts-glib
Summary:	Python 3 bindings for libaccounts-glib
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libaccounts-glib
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-pygobject3 >= 3

%description -n python3-libaccounts-glib
Python 3 bindings for libaccounts-glib.

%description -n python3-libaccounts-glib -l pl.UTF-8
Wiązania Pythona 3 do biblioteki libaccounts-glib.

%package -n vala-libaccounts-glib
Summary:	Vala API for libaccounts-glib
Summary(pl.UTF-8):	API języka Vala do biblioteki libaccounts-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-libaccounts-glib
Vala API for libaccounts-glib.

%description -n vala-libaccounts-glib -l pl.UTF-8
API języka Vala do biblioteki libaccounts-glib.

%package -n gettext-its-accounts
Summary:	Accounts ITS data for gettext tools
Summary(pl.UTF-8):	Dane ITS Accounts dla narzędzi gettext
Group:		Development/Tools
Requires:	gettext-tools >= 0.19

%description -n gettext-its-accounts
Accounts ITS data for gettext tools.

%description -n gettext-its-accounts -l pl.UTF-8
Dane ITS Accounts dla narzędzi gettext.

%prep
%setup -q

%if %{with static_libs}
%{__sed} -i -e '/^ag_library =/ s/shared_library/library/' libaccounts-glib/meson.build
%endif

%build
%meson

%meson_build

# not built from meson
xsltproc --nonet -o build/ --path docs/reference:build/docs/reference \
	http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl docs/reference/ag-backup.xml
xsltproc --nonet -o build/ --path docs/reference:build/docs/reference \
	http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl docs/reference/ag-tool.xml

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}/gi/overrides
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}/gi/overrides

%if %{with python2}
install -d $RPM_BUILD_ROOT%{py_sitedir}/gi/overrides
cp -p libaccounts-glib/pygobject/Accounts.py $RPM_BUILD_ROOT%{py_sitedir}/gi/overrides
%py_comp $RPM_BUILD_ROOT%{py_sitedir}/gi/overrides
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/gi/overrides
%py_postclean
%endif

install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p build/{ag-backup.1,ag-tool.1} $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/ag-backup
%attr(755,root,root) %{_bindir}/ag-tool
%attr(755,root,root) %{_libdir}/libaccounts-glib.so.1
%{_libdir}/girepository-1.0/Accounts-1.0.typelib
# devel only or runtime too?
%{_datadir}/dbus-1/interfaces/com.google.code.AccountsSSO.Accounts.Manager.xml
%dir %{_datadir}/xml/accounts
%dir %{_datadir}/xml/accounts/schema
%dir %{_datadir}/xml/accounts/schema/dtd
%{_datadir}/xml/accounts/schema/dtd/accounts-*.dtd
%{_mandir}/man1/ag-backup.1*
%{_mandir}/man1/ag-tool.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccounts-glib.so
%{_datadir}/gir-1.0/Accounts-1.0.gir
%{_includedir}/libaccounts-glib
%{_pkgconfigdir}/libaccounts-glib.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libaccounts-glib.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libaccounts-glib

%if %{with python2}
%files -n python-libaccounts-glib
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Accounts.py[co]
%endif

%files -n python3-libaccounts-glib
%defattr(644,root,root,755)
%{py3_sitedir}/gi/overrides/Accounts.py
%{py3_sitedir}/gi/overrides/__pycache__/Accounts.cpython-*.py[co]

%files -n vala-libaccounts-glib
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libaccounts-glib.deps
%{_datadir}/vala/vapi/libaccounts-glib.vapi

%files -n gettext-its-accounts
%defattr(644,root,root,755)
%{_datadir}/gettext/its/accounts-application.its
%{_datadir}/gettext/its/accounts-application.loc
%{_datadir}/gettext/its/accounts-provider.its
%{_datadir}/gettext/its/accounts-provider.loc
%{_datadir}/gettext/its/accounts-service-type.its
%{_datadir}/gettext/its/accounts-service-type.loc
%{_datadir}/gettext/its/accounts-service.its
%{_datadir}/gettext/its/accounts-service.loc
