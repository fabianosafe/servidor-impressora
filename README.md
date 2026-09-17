# Servidor de Impressão — FAGUS

Aplicação desktop Windows que recebe comandos de impressão via HTTP e envia RAW para impressoras térmicas locais — etiquetas ZPL (Zebra e compatíveis) e cupons ESC/POS. Usado pelo ERP FAGUS para imprimir na rede local do cliente.

## Download

Versão mais recente (Windows, .zip):

**[Baixar servidor-impressora.zip](https://github.com/fabianosafe/servidor-impressora/releases/latest/download/servidor-impressora.zip)**

Sem instalação. Extrair o .zip e executar o `servidor-impressora.exe` de dentro da pasta extraída (não mover o `.exe` sozinho — ele depende dos arquivos da pasta `_internal` ao lado).

Distribuído como pasta (onedir), não `.exe` único: builds onefile se autoextraem pra uma pasta temporária a cada execução, um padrão que heurística de antivírus costuma marcar como comportamento de dropper de malware — onedir evita isso.

## Como funciona

- Servidor Flask local escutando em `0.0.0.0:5000` por padrão.
- Interface Tkinter para selecionar impressora, ativar/desativar servidor, ver log.
- **Duas impressoras por papel**: "Impressora Etiquetas" (etiqueta ZPL) e "Impressora de Cupom" (recibo/ticket ESC/POS). O servidor é um **relay RAW agnóstico ao conteúdo** — a largura/layout vêm prontos do envio (Fagus); ele só roteia por papel.
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
- pywin32 (`win32print`) — envio raw pra spooler do Windows
- pyperclip (clipboard)

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

Local:

```bash
pip install -r requirements.txt pyinstaller
pyinstaller servidor-impressora.spec
# saída: dist/servidor-impressora/servidor-impressora.exe (+ dist/servidor-impressora/_internal/)
```

Automático: workflow `.github/workflows/release.yml` roda em `windows-latest`, zipa `dist/servidor-impressora/` e publica `servidor-impressora.zip` como GitHub Release.

## Publicar nova versão

```bash
git tag v1.2.3
git push origin v1.2.3
```

Action builda e cria a Release. URL `latest/download/servidor-impressora.zip` sempre aponta pra última.

## Integração com FAGUS

Fagus envia ZPL pra `/receive` (etiquetas) e ESC/POS em base64 pra `/imprimir-cupom` (cupom do PDV), sempre em `http://<ip-local>:5000`. Endereço configurável no modal de impressão de etiqueta e no badge de impressora do PDV. Botões de download apontam direto pra Release `latest` (`servidor-impressora.zip`).
