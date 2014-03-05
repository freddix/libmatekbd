Summary:	MATE keyboard library
Name:		libmatekbd
Version:	1.8.0
Release:	2
License:	LGPL
Group:		Libraries
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	e2d7c8ee6d5375ed923c2399eb63aeab
URL:		http://wiki.mate-desktop.org/libmatekbd
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libxklavier-devel >= 5.0
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE keyboard shared library.

%package devel
Summary:	Include files for the libbonobo document model
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package provides the necessary include files to allow you to
develop programs using the libmatekbd.

%package runtime
Summary:	MATE keyboard library - runtime
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires(post,postun):	glib-gio-gsettings

%description runtime
The thing that should not be here.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_CXX_WARNINGS.*/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,cmn,en@shaw}

%find_lang %{name} --with-mate --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%post runtime
%update_gsettings_cache

%postun runtime
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files runtime
%defattr(644,root,root,755)
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml

