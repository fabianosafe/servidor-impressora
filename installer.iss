; Instalador Windows (Inno Setup) do Servidor de Impressão FAGUS.
;
; AppId é FIXO e não deve mudar entre versões — é o que permite rodar o
; instalador de uma versão nova por cima de uma instalação existente e o
; Windows tratar como ATUALIZAÇÃO (mesmo atalho, mesma pasta, sem duplicar
; nada), em vez de instalação nova/paralela.
;
; Versão vem de fora via /DMyAppVersion=X.Y.Z (workflow do GitHub Actions
; passa a versão da tag). Sem isso, cai no default "0.0.0-dev" (build local).

#ifndef MyAppVersion
  #define MyAppVersion "0.0.0-dev"
#endif

#define MyAppName "Servidor de Impressão FAGUS"
#define MyAppPublisher "FAGUS"
#define MyAppExeName "servidor-impressora.exe"
#define MyAppId "{6B209E4C-F27D-4F25-9BFA-AF1FBE4466C9}"

[Setup]
AppId={{#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
; Pasta fixa e previsível — fora de Downloads/Desktop (evita heurística de
; antivírus contra pastas "de passagem") e serve de âncora estável pro
; auto-início com o Windows (o app registra o caminho de onde está rodando).
DefaultDirName=C:\Servidor de Impressão
DisableDirPage=no
DirExistsWarning=no
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputDir=installer_output
OutputBaseFilename=ServidorImpressoraSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Files]
Source: "dist\servidor-impressora\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName} agora"; Flags: nowait postinstall skipifsilent

[Code]
// O app normalmente está rodando (minimizado na bandeja, auto-início com o
// Windows) na hora de uma atualização — sem isso, o instalador falharia
// tentando sobrescrever o .exe travado pelo processo em execução.
//
// Testado e descartado: CloseApplications=yes (Restart Manager do Windows)
// pede pro app fechar sozinho via WM_QUERYENDSESSION/WM_ENDSESSION, mas só
// espera ~37ms antes de desistir — tempo curto demais pro loop de eventos do
// Tcl/Tk processar a mensagem a tempo, então falhava toda vez na prática.
//
// Em vez disso: mata o processo direto (taskkill /F) antes de copiar os
// arquivos — determinístico, não depende de o app responder a nada. Seguro
// porque o app grava a config a cada mudança (nunca em lote, nada a perder
// num encerramento abrupto).
procedure MatarProcessoEmExecucao();
var
  ResultCode: Integer;
begin
  Exec('taskkill.exe', '/F /IM "{#MyAppExeName}"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  MatarProcessoEmExecucao();
  Result := '';
end;
