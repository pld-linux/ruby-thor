%define		pkgname	thor
Summary:	A scripting framework that replaces rake, sake and rubigen
Summary(pl.UTF-8):	Szkielet skryptowy zastępujący rake, sake i rubigen
Name:		ruby-%{pkgname}
Version:	0.19.1
Release:	1
License:	MIT
#Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
Source0:	https://github.com/erikhuda/thor/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a75c399b989c0cb98edb5431ff458419
Group:		Development/Languages
URL:		http://whatisthor.com/
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	sed >= 4.0
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A scripting framework that replaces rake, sake and rubigen.

%description -l pl.UTF-8
Szkielet skryptowy zastępujący rake, sake i rubigen.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu thor
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu thor.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla pakietu thor
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla pakietu thor.

%prep
%setup -q -n %{pkgname}-%{version}
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%build
# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("thor.gemspec"))
	File.open("thor-%{version}.gemspec", "w") do |file|
		file.puts spec.to_ruby_for_cache
	end'

# UTF8 locale needed for doc generation
export LC_ALL=en_US.UTF-8
rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} ri/created.rid
%{__rm} ri/cache.ri
# foreign docs
%{__rm} -r ri/Object

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_ridir},%{ruby_rdocdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{ruby_specdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md LICENSE.md
%attr(755,root,root) %{_bindir}/thor
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Thor
