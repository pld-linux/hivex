#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	python3		# CPython 3 module
%bcond_without	ocaml		# OCaml bindings
%bcond_without	ocaml_opt	# OCaml native optimized binaries (bytecode is always built)
%bcond_without  ruby		# Ruby bindings

%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif
#
Summary:	Windows Registry "hive" extraction library
Summary(pl.UTF-8):	Biblioteka do wydobywania danych z plików "hive" Rejestru Windows
Name:		hivex
Version:	1.3.19
Release:	3
License:	LGPL v2.1
Group:		Libraries
Source0:	https://download.libguestfs.org/hivex/%{name}-%{version}.tar.gz
# Source0-md5:	bfbce53beb2a2d8ef29cbdfec5157633
URL:		https://libguestfs.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.0
%if %{with ocaml}
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib
%endif
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-IO-stringy
BuildRequires:	perl-Test-Simple
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	python >= 2
BuildRequires:	python-devel >= 2
%if %{with python3}
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-devel >= 1:3.2
%endif
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with ruby}
BuildRequires:	ruby-devel
BuildRequires:	ruby-rake
%endif
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
Summary:	Python 2 bindings for hivex library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki hivex
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-hivex
Python 2 bindings for hivex library.

%description -n python-hivex -l pl.UTF-8
Wiązania Pythona 2 do biblioteki hivex.

%package -n python3-hivex
Summary:	Python 3 bindings for hivex library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki hivex
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-hivex
Python 3 bindings for hivex library.

%description -n python3-hivex -l pl.UTF-8
Wiązania Pythona 3 do biblioteki hivex.

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

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+perl(\s|$),#!%{__perl}\1,' \
      regedit/hivexregedit

%build
%{__aclocal}
%{__automake}
%{__autoconf}

%if %{with python3}
install -d build-py3
cd build-py3
../%configure \
	PYTHON="%{__python3}" \
	--with-python-installdir=%{py3_sitedir} \
	--disable-ocaml \
	--disable-perl \
	--disable-ruby \
	--disable-silent-rules

%{__make}
cd ..
%endif

%configure \
	--disable-silent-rules \
	--with-python-installdir=%{py_sitedir} \
	%{__enable_disable ocaml} \
	%{__enable_disable static_libs static}

%{__make} \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
# lib is needed for relink on install
%{__make} -C build-py3/lib install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -C build-py3/python install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.la
%endif

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

%if %{with ocaml}
%files -n ocaml-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmlhivex.so
%{_libdir}/ocaml/stublibs/dllmlhivex.so.owner

%files -n ocaml-hivex-devel
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/hivex
%{_libdir}/ocaml/hivex/META
%{_libdir}/ocaml/hivex/hivex.cmi
%{_libdir}/ocaml/hivex/hivex.mli
%{_libdir}/ocaml/hivex/libmlhivex.a
%{_libdir}/ocaml/hivex/mlhivex.cma
%if %{with ocaml_opt}
%{_libdir}/ocaml/hivex/hivex.cmx
%{_libdir}/ocaml/hivex/mlhivex.a
%{_libdir}/ocaml/hivex/mlhivex.cmxa
%endif
%endif

%files -n perl-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hivexregedit
%dir %{perl_vendorarch}/Win
%dir %{perl_vendorarch}/Win/Hivex
%{perl_vendorarch}/Win/Hivex.pm
%{perl_vendorarch}/Win/Hivex/Regedit.pm
%dir %{perl_vendorarch}/auto/Win
%dir %{perl_vendorarch}/auto/Win/Hivex
%attr(755,root,root) %{perl_vendorarch}/auto/Win/Hivex/Hivex.so
%{_mandir}/man1/hivexregedit.1*
%{_mandir}/man3/Win::Hivex.3pm*
%{_mandir}/man3/Win::Hivex::Regedit.3pm*

%files -n python-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/libhivexmod.so
%dir %{py_sitedir}/hivex
%{py_sitedir}/hivex/*.py[co]

%if %{with python3}
%files -n python3-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/libhivexmod.cpython-*.so
%{py3_sitedir}/hivex
%endif

%if %{with ruby}
%files -n ruby-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/_hivex.so
%{ruby_vendorlibdir}/hivex.rb
%endif
