; ReadytoWork - Inno Setup script
; English wizard. Build with: ISCC.exe installer.iss
; Requires Inno Setup 6.x. On CI it is installed by the release workflow.

#define AppName "ReadytoWork"
#define AppNameLower "readytowork"
#define AppVersion "1.0.0"
#define AppPublisher "ilkeryigit"
#define AppURL "https://github.com/ilkeryigit/ReadytoWork"
#define AppExeName "ReadytoWork.exe"

[Setup]
AppId={{7B4C9A21-6D3E-4F18-9C55-2A8E1D6B0F34}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}/issues
AppUpdatesURL={#AppURL}/releases
DefaultDirName={localappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE
OutputDir=dist
OutputBaseFilename={#AppName}-Setup-{#AppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
; Per-user by default: the app writes HKCU and %APPDATA%, so no admin rights
; are needed. The dialog still offers a machine-wide install for power users.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#AppExeName}
SetupIconFile=app.ico
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; Both tasks are checked by default, as specified for this project.
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"
Name: "autostart"; Description: "Start {#AppName} when Windows starts"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; DestName: "README.md"; Flags: ignoreversion isreadme

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
  ValueType: string; ValueName: "{#AppName}"; ValueData: """{app}\{#AppExeName}"""; \
  Flags: uninsdeletevalue; Tasks: autostart

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; \
  Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Settings are removed on uninstall, as decided for this project.
Type: filesandordirs; Name: "{userappdata}\{#AppNameLower}"
Type: filesandordirs; Name: "{userappdata}\{#AppName}"

[Code]
function InitializeSetup: Boolean;
begin
  Result := True;
end;
