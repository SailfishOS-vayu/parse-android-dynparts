Name:		parse-android-dynparts	
Version:	0.1	
Release:	1%{?dist}
Summary:	Allows mounting Android Dynamic Partitions (a.k.a. super.img) files on Linux using "dmsetup create"

Group:		tchebb
License:	Apache-2.0
URL:		https://github.com/tchebb/parse-android-dynparts
Source0:	https://github.com/tchebb/parse-android-dynparts/archive/refs/heads/master.zip

BuildRequires:	cmake
BuildRequires:	openssl-devel
BuildRequires:  ninja
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Most devices running Android 10 and higher use Android's Dynamic Partitions feature to allow the different read-only system partitions (e.g. system, vendor, product) to share the same pool of storage space. This allows vendors to safely resize those partitions in OTA updates, as long as the sum of their sizes doesn't exceed that of the physical partition they all reside in.

The physical partition image that holds multiple Android dynamic partitions is conventionally named super.img and holds similar information as an LVM physical volume on Linux: a list of logical partitions, each associated with a (possibly non-contiguous) set of blocks in the file that comprise it. Like LVM, Android makes use of Device Mapper's dm-linear target to inform the kernel of the logical partitions so it can map them to block devices in /dev/mapper.

In true Google fashion, however, Android dynamic partitions use a totally custom header format that is not compatible with LVM or other similar software. As such, the only official tools that exist to mount them are part of Android and depend heavily on Android's frameworks, volume manager, and init system. (There are official tools that run on Linux to pack and unpack super.img files, but they cannot mount them in-place.)

This tool makes it possible to mount super.img files with a standard Linux userspace. It uses a modified version of Google's AOSP code to parse the partition layout, then outputs that layout as a textual "concise device specification" which, when passed to dmsetup, instructs the kernel to create a Device Mapper block device for each logical partition in the image.

%prep
%autosetup -n %{name}-%{version}/%{name}


%build
mkdir -p build
pushd build
%cmake ..\
    -G Ninja
%ninja_build
popd

%install
rm -rf %{buildroot}
pushd build
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/%{_libdir}
install -m 755 parse-android-dynparts %{buildroot}/usr/bin/parse-android-dynparts
install -m 644 liblp/liblp.so %{buildroot}/%{_libdir}/liblp.so
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/liblp.so

%changelog

