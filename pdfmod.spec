Name:		pdfmod
License:	GPL v2.0 or later
Group:		Office
Version:        0.9.1
Release:        %mkrel 2
Summary:	PDF Mod is a simple application for modifying PDF documents
Url:		http://live.gnome.org/PdfMod
Source:         http://ftp.gnome.org/pub/GNOME/sources/pdfmod/0.9//%{name}-%{version}.tar.bz2
Source1:	pdfmod-poppler-sharp.dll.config
#patch for mono 2.10
Patch0:		pdfmod-mono-2.10-1.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	hyena >= 0.5
BuildRequires:	docbook-dtd42-sgml
BuildRequires:	gmime-sharp
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-sharp2-devel
BuildRequires:	gnome-sharp2
BuildRequires:	gtk-sharp2
BuildRequires:	mono-basic
#BuildRequires:	mono-data-sqlite
BuildRequires:	mono-devel
BuildRequires:	mono-nunit
BuildRequires:	ndesk-dbus
BuildRequires:	ndesk-dbus-glib-devel
BuildRequires:	scrollkeeper
BuildRequires:	tango-icon-theme
BuildRequires:  desktop-file-utils
BuildRequires:	intltool
Requires:	mono
Requires:	gtk-sharp2
#Requires:	libpoppler-glib

%description
PDF Mod is a simple application for modifying PDF documents.

You can reorder, rotate, and remove pages, export images from a document, 
edit the title, subject, author, and keywords, and combine documents via drag and drop. 

%prep
%setup
%patch0 -p1
# upstream uses 0.4 vs Fedora current 0.6
cp %{SOURCE1} lib/poppler-sharp/poppler-sharp/poppler-sharp.dll.config

%build
%configure 
make

%install
make install DESTDIR=%{buildroot}

%find_lang %{name}

desktop-file-install --dir=%{buildroot}%{_datadir}/applications/   %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README COPYING
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome/help/pdfmod/*/pdfmod.xml
