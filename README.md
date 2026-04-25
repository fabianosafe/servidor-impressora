# Servidor de Impressão de Etiquetas — FAGUS

Aplicação desktop Windows que recebe comandos ZPL via HTTP e imprime em impressoras térmicas locais (Zebra e compatíveis). Usado pelo ERP FAGUS para imprimir etiquetas de produto na impressora da rede local do cliente.

## Download

Versão mais recente (executável Windows):

**[Baixar etiqueta-server.exe](https://github.com/fabianosafe/servidor-impressora/releases/latest/download/etiqueta-server.exe)**

Sem instalação. Executar direto.

## Como funciona

- Servidor Flask local escutando em `0.0.0.0:5000` por padrão.
- Interface Tkinter para selecionar impressora, ativar/desativar servidor, ver log.
- Endpoints:
  - `GET /` — health check
  - `GET /test` — teste conexão
  - `POST /receive` — recebe JSON com comando ZPL e envia pra impressora selecionada
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
python etiqueta-server.py
```

## Build do executável

Local:

```bash
pip install -r requirements.txt pyinstaller
pyinstaller servidor-etiquetas.spec
# saída: dist/etiqueta-server.exe
```

Automático: workflow `.github/workflows/release.yml` roda em `windows-latest` e publica o `.exe` como GitHub Release.

## Publicar nova versão

```bash
git tag v1.2.3
git push origin v1.2.3
```

Action builda e cria a Release. URL `latest/download/etiqueta-server.exe` sempre aponta pra última.

## Integração com FAGUS

Fagus envia ZPL via `fetch` pra `http://<ip-local>:5000/receive`. Endereço configurável no modal de impressão de etiqueta. Botão de download no modal aponta direto pra Release `latest`.
