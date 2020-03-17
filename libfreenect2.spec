# TODO: CUDA (on bcond)
#
# Conditional build:
%bcond_without	openni2		# OpenNI2 driver
#
Summary:	Driver for Kinect for Windows v2 (K4W2) devices
Summary(pl.UTF-8):	Sterownik dla urządzeń Kinect for Windows v2 (K4W2)
Name:		libfreenect2
Version:	0.2.0
Release:	1
License:	Apache v2.0 or GPL v2
Group:		Libraries
#Source0Download: https://github.com/OpenKinect/libfreenect2/releases
Source0:	https://github.com/OpenKinect/libfreenect2/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	54bde616ede3cff23eaeb2a736ca6e45
Patch0:		%{name}-c++.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-libsuffix.patch
URL:		https://openkinect.org/wiki/Main_Page
BuildRequires:	OpenCL-devel >= 1.1
BuildRequires:	OpenGL-devel >= 3.1
%{?with_openni2:BuildRequires:	OpenNI2-devel >= 2.2.0.33}
BuildRequires:	cmake >= 2.8.12.1
BuildRequires:	glfw-devel >= 3
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libusb-devel >= 1.0.20
BuildRequires:	libva-devel
BuildRequires:	libva-drm-devel
BuildRequires:	pkgconfig
Requires:	libusb >= 1.0.20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Driver for Kinect for Windows v2 (K4W2) devices.

%description -l pl.UTF-8
Sterownik dla urządzeń Kinect for Windows v2 (K4W2).

%package devel
Summary:	Header files for libfreenect libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek libfreenect
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libusb-devel >= 1.0.20

%description devel
Header files for libfreenect libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek libfreenect.

%package -n OpenNI2-driver-freenect2
Summary:	OpenNI2 driver for Microsoft Kinect
Summary(pl.UTF-8):	Sterownik do kontrolera Microsoft Kinect dla platformy OpenNI2
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenNI2 >= 2.2.0.33

%description -n OpenNI2-driver-freenect2
OpenNI2 driver for Microsoft Kinect.

%description -n OpenNI2-driver-freenect2 -l pl.UTF-8
Sterownik do kontrolera Microsoft Kinect dla platformy OpenNI2.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%cmake .. \
	-DBUILD_EXAMPLES=OFF \
	%{!?with_openni2:-DBUILD_OPENNI2_DRIVER=OFF} \
	-DENABLE_CUDA=OFF \
	-DENABLE_CXX11=ON \
	-DLIBFREENECT2_THREADING_LIBRARIES=pthread

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CONTRIB README.md
%attr(755,root,root) %{_libdir}/libfreenect2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreenect2.so.0.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreenect2.so
%{_includedir}/libfreenect2
%{_pkgconfigdir}/freenect2.pc
%{_libdir}/cmake/freenect2

%if %{with openni2}
%files -n OpenNI2-driver-freenect2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/OpenNI2/Drivers/libfreenect2-openni2.so*
%endif
