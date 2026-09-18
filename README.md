# Servidor de Impressão — FAGUS

Aplicação desktop Windows que recebe comandos de impressão via HTTP e envia RAW para impressoras térmicas locais — etiquetas ZPL (Zebra e compatíveis) e cupons ESC/POS. Usado pelo ERP FAGUS para imprimir na rede local do cliente.

## Download

Versão mais recente (instalador Windows):

**[Baixar ServidorImpressoraSetup.exe](https://github.com/fabianosafe/servidor-impressora/releases/latest/download/ServidorImpressoraSetup.exe)**

Executar e seguir o assistente (Avançar → Avançar → Concluir). Instala em `C:\Servidor de Impressão` por padrão, cria atalho no Menu Iniciar e desinstalador. Pede elevação (UAC) — normal, é só pra escrever fora da pasta do usuário.

**Atualizar** é rodar o instalador de uma versão nova por cima — o `AppId` é fixo (`installer.iss`), então o Windows reconhece como atualização (mesma pasta, mesmo atalho, sem duplicar nada), não instalação nova. Se o app estiver rodando (comum, já que ele fica minimizado na bandeja com "Iniciar com o Windows"), o próprio instalador encerra o processo antes de sobrescrever os arquivos (`[Code]` em `installer.iss` — decisão deliberada de matar o processo direto em vez de depender do Restart Manager do Windows pedir educadamente: testado e descartado, o Restart Manager só espera ~37ms antes de desistir, tempo curto demais pro loop de eventos do Tcl/Tk responder a tempo).

Instalador em vez de `.exe`/`.zip` solto: builds "onefile" se autoextraem pra uma pasta temporária a cada execução (padrão que antivírus costuma marcar como dropper de malware) — o build já é onedir (pasta com `.exe` + `_internal` ao lado, sem autoextração) e o instalador cria a pasta fixa sozinho, evitando também o antivírus barrar arquivos ao extrair manualmente numa pasta "de passagem" tipo Downloads.

## Como funciona

- Servidor Flask local escutando em `localhost:5000` por padrão (host configurável na interface).
- Interface Tkinter para selecionar impressora, ativar/desativar servidor, ver log.
- **Duas impressoras por papel**: "Impressora Etiquetas" (etiqueta ZPL) e "Impressora de Cupom" (recibo/ticket ESC/POS). O servidor é um **relay RAW agnóstico ao conteúdo** — a largura/layout vêm prontos do envio (Fagus); ele só roteia por papel. Combobox tem opção "(Nenhuma)" pra deixar em branco de propósito (padrão numa instalação nova, sem forçar escolha).
- **Ícone na bandeja do sistema** (pystray): fechar a janela (X) minimiza em vez de encerrar; menu da bandeja tem Abrir/Sair.
- **"Iniciar com o Windows"** (switch único): registra `HKCU\...\Run` apontando pro caminho onde o `.exe` está rodando, inicia minimizado na bandeja, liga o servidor — tudo junto.
- **Checagem de atualização** ao abrir (thread própria, não bloqueia): compara `APP_VERSION` com a Release mais recente no GitHub; se houver mais nova, mostra botão destacado na janela + notificação nativa do Windows (essencial já que o app normalmente abre minimizado).
- Endpoints:
  - `GET /` — health check
  - `GET /test` — teste conexão
  - `POST /receive` — recebe JSON com comando ZPL (`tipo: 'etiqueta_impressao'`) e envia pra impressora de etiqueta
  - `POST /imprimir-cupom` — recebe `{ tipo: 'cupom', dados_base64 }` (bytes ESC/POS em base64) e envia RAW pra impressora de cupom
- CORS liberado pra ser chamado pelo Fagus rodando em qualquer domínio.

## Stack

- Python 3.11
- Flask + flask-cors (HTTP)
- Tkinter (UI)
- pywin32 (`win32print`, `win32gui`) — envio raw pra spooler do Windows, hook de encerramento e registro no autorun
- pystray + Pillow — ícone na bandeja do sistema
- pyperclip (clipboard)
- Inno Setup 6 (`installer.iss`) — instalador Windows, não é dependência Python (baixar separadamente pra build local)

## Build local (desenvolvimento)

Pré-requisitos: Python 3.11 + Windows.

```bash
pip install -r requirements.txt
python servidor-impressora.py
```

### Linux (só desenvolvimento)

Produção é Windows (`pywin32`). No Linux, use o shim em `dev-linux/win32shim/` — simula impressoras virtuais sem alterar o código principal.

```bash
# venv sem pywin32 (Flask + flask-cors + pyperclip; Tkinter do sistema)
python3 -m venv .venv
./.venv/bin/pip install Flask flask-cors pyperclip

PYTHONPATH=dev-linux/win32shim ./.venv/bin/python servidor-impressora.py
```

Impressoras virtuais no combo:
- **Emulador ESC/POS (localhost:9100)** — envia RAW via TCP (ex.: [escpos-netprinter](https://github.com/gilbertfl/escpos-netprinter) em `:8080`)
- **Arquivo (/tmp/impressora-raw)** — grava cada job em `.bin`

O shim **não** entra no PyInstaller / release Windows.

## Build do executável

Local (precisa do [Inno Setup 6](https://jrsoftware.org/isinfo.php) instalado, `winget install JRSoftware.InnoSetup`):

```bash
pip install -r requirements.txt pyinstaller
pyinstaller servidor-impressora.spec
# saída: dist/servidor-impressora/servidor-impressora.exe (+ dist/servidor-impressora/_internal/)

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /DMyAppVersion=1.4.0 installer.iss
# saída: installer_output/ServidorImpressoraSetup.exe
```

`MyAppVersion` também vira o número mostrado em "Programas e Recursos" do Windows — manter em sincronia com a constante `APP_VERSION` no topo de `servidor-impressora.py` (usada na checagem de atualização) e com a tag do git.

Automático: workflow `.github/workflows/release.yml` roda em `windows-latest`, compila o `.exe` + o instalador (`/DMyAppVersion=<versão da tag>`) e publica `ServidorImpressoraSetup.exe` como GitHub Release.

## Publicar nova versão

1. Atualizar `APP_VERSION` em `servidor-impressora.py` pra bater com a tag.
2. `git tag v1.4.1 && git push origin v1.4.1`

Action builda e cria a Release. URL `latest/download/ServidorImpressoraSetup.exe` sempre aponta pra última.

## Integração com FAGUS

Fagus envia ZPL pra `/receive` (etiquetas) e ESC/POS em base64 pra `/imprimir-cupom` (cupom do PDV), sempre em `http://<ip-local>:5000`. Endereço configurável no modal de impressão de etiqueta e no badge de impressora do PDV. Botões de download apontam direto pra Release `latest` (`ServidorImpressoraSetup.exe`).
