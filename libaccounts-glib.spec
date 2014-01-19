#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# testsuite build [switch broken in configure]
#
Summary:	Accounts management library for GLib applications
Summary(pl.UTF-8):	Biblioteka do zarządzania kontami dla aplikacji opartych na bibliotece GLib
Name:		libaccounts-glib
Version:	1.16
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: http://code.google.com/p/accounts-sso/downloads/list
Source0:	http://accounts-sso.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		%{name}-types.patch
# Source0-md5:	9cdb46354885a8973bccd05090360361
URL:		http://code.google.com/p/accounts-sso/
%{?with_tests:BuildRequires:	check-devel >= 0.9.4}
BuildRequires:	docbook-dtd43-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	python-pygobject3-devel >= 3.0
BuildRequires:	sqlite3-devel >= 3.7.0
BuildRequires:	rpmbuild(macros) >= 1.219
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

%description apidocs
API documentation for libaccounts-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libaccounts-glib.

%package -n python-libaccounts-glib
Summary:	Python bindings for libaccounts-glib
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libaccounts-glib
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygobject3 >= 3

%description -n python-libaccounts-glib
Python bindings for libaccounts-glib.

%description -n python-libaccounts-glib -l pl.UTF-8
Wiązania Pythona do biblioteki libaccounts-glib.

%package -n vala-libaccounts-glib
Summary:	Vala API for libaccounts-glib
Summary(pl.UTF-8):	API języka Vala do biblioteki libaccounts-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala

%description -n vala-libaccounts-glib
Vala API for libaccounts-glib.

%description -n vala-libaccounts-glib -l pl.UTF-8
API języka Vala do biblioteki libaccounts-glib.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{!?with_tests:--disable-tests} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/libaccounts-glib.la
%if %{with tests}
# tests suite
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaccounts-glib/*test*
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/libaccounts-glib/testdata
%endif

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/ag-backup
%attr(755,root,root) %{_bindir}/ag-tool
%attr(755,root,root) %{_libdir}/libaccounts-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaccounts-glib.so.0
%{_libdir}/girepository-1.0/Accounts-1.0.typelib
# who owns / uses it?
#%{_datadir}/backup-framework/applications/accounts.conf
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

%files -n python-libaccounts-glib
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Accounts.py[co]

%files -n vala-libaccounts-glib
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libaccounts-glib.deps
%{_datadir}/vala/vapi/libaccounts-glib.vapi
