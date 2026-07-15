"""Shim Linux de win32print para simular o servidor-impressora.

Só para desenvolvimento. Não entra no build do .exe Windows.

Expõe duas "impressoras" virtuais:
- "Emulador ESC/POS (localhost:9100)" — envia os bytes RAW via TCP para o
  escpos-netprinter (cupom renderizado em http://localhost:8080)
- "Arquivo (/tmp/impressora-raw)" — grava cada job em um arquivo .bin

Uso:
  PYTHONPATH=dev-linux/win32shim ./.venv/bin/python servidor-impressora.py
"""
import os
import socket
import time

PRINTER_ENUM_LOCAL = 2

PRINTER_TCP = "Emulador ESC/POS (localhost:9100)"
PRINTER_FILE = "Arquivo (/tmp/impressora-raw)"

_EMULADOR_HOST = os.environ.get("ESCPOS_EMULATOR_HOST", "127.0.0.1")
_EMULADOR_PORT = int(os.environ.get("ESCPOS_EMULATOR_PORT", "9100"))
_FILE_DIR = "/tmp/impressora-raw"


def EnumPrinters(flags, name=None, level=1):
    # mesmo shape usado pelo servidor: printer[2] = nome
    return [
        (0, "", PRINTER_TCP, ""),
        (0, "", PRINTER_FILE, ""),
    ]


def GetDefaultPrinter():
    return PRINTER_TCP


class _Job:
    def __init__(self, printer):
        self.printer = printer
        self.buffer = b""


def OpenPrinter(printer_name):
    return _Job(printer_name)


def StartDocPrinter(handle, level, doc_info):
    handle.doc_name = doc_info[0]
    return 1


def StartPagePrinter(handle):
    pass


def WritePrinter(handle, data):
    handle.buffer += data
    return len(data)


def EndPagePrinter(handle):
    pass


def EndDocPrinter(handle):
    if handle.printer == PRINTER_FILE:
        os.makedirs(_FILE_DIR, exist_ok=True)
        path = os.path.join(_FILE_DIR, f"job-{time.strftime('%Y%m%d-%H%M%S')}.bin")
        with open(path, "wb") as f:
            f.write(handle.buffer)
    else:
        with socket.create_connection((_EMULADOR_HOST, _EMULADOR_PORT), timeout=10) as s:
            s.sendall(handle.buffer)
    handle.buffer = b""


def ClosePrinter(handle):
    pass
