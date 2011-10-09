#
# TODO: ruby bindings
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
%include	/usr/lib/rpm/macros.perl
Summary:	Windows Registry "hive" extraction library
Name:		hivex
Version:	1.3.1
Release:	2
License:	LGPL v2.1
Group:		Libraries
Source0:	http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz
# Source0-md5:	fa38e8ea348c750046b4f34c573e0c32
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	perl-tools-pod
BuildRequires:	readline-devel
BuildRequires:	libxml2-devel
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib-devel
BuildRequires:	perl
BuildRequires:	perl(Test::More)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(IO::Stringy)
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hivex is a library for extracting the contents of Windows Registry
"hive" files. It is designed to be secure against buggy or malicious
registry files.

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

%package -n perl-hivex
Summary:	Perl bindings for hivex library
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-hivex
Perl bindings for hivex library.

%package -n python-hivex
Summary:	Python bindings for hivex library
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-hivex
Python bindings for hivex library.

%package -n ocaml-hivex
Summary:	OCaml bindings for hivex library
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n ocaml-hivex
OCaml bindings for hivex library.

%package -n ocaml-hivex-devel
Summary:	Header files for ocamlhivex library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ocaml-hivex
Group:		Development/Libraries
Requires:	ocaml-hivex = %{version}-%{release}

%description -n ocaml-hivex-devel
Header files for ocaml-hivex library.

%description -n ocaml-hivex-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ocaml-hivex.

%prep
%setup -q

%build
%configure \
	ac_cv_lib_ruby_ruby_init=no \
	ac_cv_prog_RAKE=no \
	%{__enable_disable static_libs static} \
	--disable-silent-rules

%{__make} \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALLDIRS=vendor \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{py_sitedir}/*.la

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
%{_libdir}/libhivex.so
%{_includedir}/hivex.h
%{_pkgconfigdir}/hivex.pc
%{_mandir}/man3/hivex.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libhivex.a
%endif

%files -n perl-hivex
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hivexregedit
%dir %{perl_vendorarch}/Win
%dir %{perl_vendorarch}/Win/Hivex
%{perl_vendorarch}/Win/Hivex.pm
%{perl_vendorarch}/Win/Hivex/Regedit.pm
%{perl_vendorarch}/auto/Win/Hivex/Hivex.bs
%dir %{perl_vendorarch}/auto/Win
%dir %{perl_vendorarch}/auto/Win/Hivex
%attr(755,root,root) %{perl_vendorarch}/auto/Win/Hivex/Hivex.so
%{_mandir}/man1/hivexregedit.1*
%{_mandir}/man3/Win::Hivex.3pm.gz
%{_mandir}/man3/Win::Hivex::Regedit.3pm.gz

%files -n python-hivex
%defattr(644,root,root,755)
%{py_sitedir}/hivex.py
%attr(755,root,root) %{py_sitedir}/libhivexmod.so

%files -n ocaml-hivex
%defattr(644,root,root,755)
%{_libdir}/ocaml/stublibs/dllmlhivex.so
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
