@echo off
echo Instalando dependencias do servidor de etiquetas...
echo.

echo Instalando Flask...
:: py -m pip install flask==2.3.3
py -m pip install flask

echo.
echo Instalando Flask-CORS...
:: py -m pip install flask-cors==4.0.0
py -m pip install flask-cors

echo.
echo Instalando pywin32...
:: py -m pip install pywin32==306
py -m pip install pywin32

echo.
echo Instalando pyperclip...
:: py -m pip install pyperclip==1.8.2
py -m pip install pyperclip

echo.
echo Dependencias instaladas com sucesso!
echo.
echo Para executar o servidor, use:
echo py etiqueta-server.py
echo.
pause 