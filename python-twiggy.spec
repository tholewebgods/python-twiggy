%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%global srcname Twiggy

Name:           python-twiggy
Version:        0.4.5
Release:        1%{?dist}
Summary:        Twiggy is a Pythonic logger.

Group:          Development/Libraries
License:        BSD
URL:            http://twiggy.wearpants.org/
Source0:	https://pypi.python.org/packages/source/T/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

%description
Twiggy
========

Twiggy is a Pythonic logger. 



%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation and examples for %{name}.


%if 0%{?with_python3}
%package -n python3-twiggy
Summary:        The Swiss Army knife of Python web development
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx

%description -n python3-twiggy
Twiggy
========

Twiggy is a Pythonic logger. 


%package -n python3-twiggy-doc
Summary:        Documentation for python3-twiggy
Group:          Documentation
Requires:       python3-twiggy = %{version}-%{release}

%description -n python3-twiggy-doc
Documentation and examples for python3-twiggy.
%endif


%prep
%setup -q -n %{srcname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif


%build
%{__python} setup.py build
pushd doc
make html
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
pushd doc
make html
popd
popd
%endif


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf doc/_build/html/.buildinfo

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf doc/_build/html/.buildinfo
popd
%endif


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README.rst
%dir %{python_sitelib}/twiggy
%{python_sitelib}/*

%files doc
%defattr(-,root,root,-)
%doc doc/_build/html

%if 0%{?with_python3}
%files -n python3-twiggy
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README.rst
%{python3_sitelib}/*

%files -n python3-twiggy-doc
%defattr(-,root,root,-)
%doc doc/_build/html
%endif


%changelog
* Mon Feb 09 2015 Thomas Lehmann <t.lehmann@strato-rz.de> - 0.4.5-1
- Initial package
