Summary:	MATE keyboard library
Name:		libmatekbd
Version:	1.6.2
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	35880a6bc967ed3093e7c46a58958b1f
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
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

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

