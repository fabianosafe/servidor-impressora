@echo off
echo ========================================
echo    CRIADOR DE EXECUTAVEL - SERVIDOR DE ETIQUETAS
echo ========================================
echo.

echo [1/4] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [2/4] Instalando PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/4] Instalando Auto-py-to-exe...
pip install auto-py-to-exe
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar Auto-py-to-exe
    pause
    exit /b 1
)

echo.
echo [4/4] Iniciando Auto-py-to-exe...
echo.
echo INSTRUCOES:
echo 1. Selecione o arquivo: etiqueta-server.py
echo 2. Escolha "One File" (um arquivo)
echo 3. Escolha "Window Based" (sem console)
echo 4. Nome do executavel: Servidor-Etiquetas
echo 5. Clique em "Convert .py to .exe"
echo.
echo Pressione qualquer tecla para abrir o Auto-py-to-exe...
pause >nul

auto-py-to-exe

echo.
echo Processo concluido!
echo O executavel sera criado na pasta "output"
pause 