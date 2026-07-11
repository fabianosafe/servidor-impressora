# Servidor de Impressão — FAGUS

Aplicação desktop Windows que recebe comandos de impressão via HTTP e envia RAW para impressoras térmicas locais — etiquetas ZPL (Zebra e compatíveis) e cupons ESC/POS. Usado pelo ERP FAGUS para imprimir na rede local do cliente.

## Download

Versão mais recente (executável Windows):

**[Baixar servidor-impressora.exe](https://github.com/fabianosafe/servidor-impressora/releases/latest/download/servidor-impressora.exe)**

Sem instalação. Executar direto.

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

## Build do executável

Local:

```bash
pip install -r requirements.txt pyinstaller
pyinstaller servidor-impressora.spec
# saída: dist/servidor-impressora.exe
```

Automático: workflow `.github/workflows/release.yml` roda em `windows-latest` e publica o `.exe` como GitHub Release.

## Publicar nova versão

```bash
git tag v1.2.3
git push origin v1.2.3
```

Action builda e cria a Release. URL `latest/download/servidor-impressora.exe` sempre aponta pra última.

## Integração com FAGUS

Fagus envia ZPL pra `/receive` (etiquetas) e ESC/POS em base64 pra `/imprimir-cupom` (cupom do PDV), sempre em `http://<ip-local>:5000`. Endereço configurável no modal de impressão de etiqueta e no badge de impressora do PDV. Botões de download apontam direto pra Release `latest` (`servidor-impressora.exe`).
