#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
%include	/usr/lib/rpm/macros.perl
Summary:	Windows Registry "hive" extraction library
Summary(pl.UTF-8):	Biblioteka do wydobywania danych z plików "hive" Rejestru Windows
Name:		hivex
Version:	1.3.10
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz
# Source0-md5:	38f82c568e71a9783b12e1983fdf71f9
URL:		http://libguestfs.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-IO-stringy
BuildRequires:	perl-Test-Simple
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	ruby-devel
BuildRequires:	ruby-rake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hivex is a library for extracting the contents of Windows Registry
"hive" files. It is designed to be secure against buggy or malicious
registry files.

%description -l pl.UTF-8
Hivex to biblioteka do wydobywania zawartości plików "hive" Rejestru
Windows. Została zaprojektowana w celu ochrony przez błędnymi lub
niebezpiecznymi plikami rejestru.

%package devel
Summary:	Header files for hivex library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki hivex
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for hivex library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki hivex.

%package static
Summary:	Static hivex library
Summary(pl.UTF-8):	Statyczna biblioteka hivex
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static hivex library.

%description static -l pl.UTF-8
Statyczna biblioteka hivex.

%package -n ocaml-hivex
Summary:	OCaml bindings for hivex library
Summary(pl.UTF-8):	Wiązania OCamla do biblioteki hivex
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n ocaml-hivex
OCaml bindings for hivex library.

%description -n ocaml-hivex -l pl.UTF-8
Wiązania OCamla do biblioteki hivex.

%package -n ocaml-hivex-devel
Summary:	Development files for hivex OCaml bindings
Summary(pl.UTF-8):	Pliki programistyczne wiązań OCamla do biblioteki hivex
Group:		Development/Libraries
Requires:	ocaml-hivex = %{version}-%{release}

%description -n ocaml-hivex-devel
Development files for hivex OCaml bindings.

%description -n ocaml-hivex-devel -l pl.UTF-8
Pliki programistyczne wiązań OCamla do biblioteki hivex.

%package -n perl-hivex
Summary:	Perl bindings for hivex library
Summary(pl.UTF-8):	Wiązania Perla do biblioteki hivex
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-hivex
Perl bindings for hivex library.

%description -n perl-hivex -l pl.UTF-8
Wiązania Perla do biblioteki hivex.

%package -n python-hivex
Summary:	Python bindings for hivex library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki hivex
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-hivex
Python bindings for hivex library.

%description -n python-hivex -l pl.UTF-8
Wiązania Pythona do biblioteki hivex.

%package -n ruby-hivex
Summary:	Ruby bindings for hivex library
Summary(pl.UTF-8):	Wiązania języka Ruby do biblioteki hivex
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n ruby-hivex
Ruby bindings for hivex library.

%description -n ruby-hivex -l pl.UTF-8
Wiązania języka Ruby do biblioteki hivex.

%prep
%setup -q

%build
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules \
	%{__enable_disable static_libs static}

%{__make} \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALLDIRS=vendor \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{py_sitedir}/*.la

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog README TODO
%attr(755,root,root) %{_bindir}/hivexget
%attr(755,root,root) %{_bindir}/hivexml
%attr(755,root,root) %{_bindir}/hivexsh
%attr(755,root,root) %{_libdir}/libhivex.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhivex.so.0
%{_mandir}/man1/hivexget.1*
%{_mandir}/man1/hivexml.1*
%{_mandir}/man1/hivexsh.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhivex.so
%{_includedir}/hivex.h
%{_pkgconfigdir}/hivex.pc
%{_mandir}/man3/hivex.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libhivex.a
%endif

%files -n ocaml-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmlhivex.so
%{_libdir}/ocaml/stublibs/dllmlhivex.so.owner

%files -n ocaml-hivex-devel
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/hivex
%{_libdir}/ocaml/hivex/META
%{_libdir}/ocaml/hivex/hivex.cmi
%{_libdir}/ocaml/hivex/hivex.cmx
%{_libdir}/ocaml/hivex/hivex.mli
%{_libdir}/ocaml/hivex/libmlhivex.a
%{_libdir}/ocaml/hivex/mlhivex.a
%{_libdir}/ocaml/hivex/mlhivex.cma
%{_libdir}/ocaml/hivex/mlhivex.cmxa

%files -n perl-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hivexregedit
%dir %{perl_vendorarch}/Win
%dir %{perl_vendorarch}/Win/Hivex
%{perl_vendorarch}/Win/Hivex.pm
%{perl_vendorarch}/Win/Hivex/Regedit.pm
%dir %{perl_vendorarch}/auto/Win
%dir %{perl_vendorarch}/auto/Win/Hivex
%{perl_vendorarch}/auto/Win/Hivex/Hivex.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Win/Hivex/Hivex.so
%{_mandir}/man1/hivexregedit.1*
%{_mandir}/man3/Win::Hivex.3pm.*
%{_mandir}/man3/Win::Hivex::Regedit.3pm.*

%files -n python-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/libhivexmod.so
%{py_sitedir}/hivex.py[co]

%files -n ruby-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/_hivex.so
%{ruby_vendorlibdir}/hivex.rb
