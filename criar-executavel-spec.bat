@echo off
echo ========================================
echo    CRIADOR DE EXECUTAVEL OTIMIZADO
echo    SERVIDOR DE ETIQUETAS
echo ========================================
echo.

echo [1/3] Instalando dependencias (versao flexivel)...
pip install -r requirements-flexivel.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [2/3] Instalando PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/3] Criando executavel otimizado...
echo.

REM Criar executavel usando arquivo .spec
pyinstaller servidor-etiquetas.spec

if %errorlevel% neq 0 (
    echo ERRO: Falha ao criar executavel
    pause
    exit /b 1
)

echo.
echo ========================================
echo    EXECUTAVEL CRIADO COM SUCESSO!
echo ========================================
echo.
echo Localizacao: dist\Servidor-Etiquetas.exe
echo.
echo Vantagens desta versao:
echo - Configuracao otimizada
echo - Inclui todas as dependencias necessarias
echo - Tamanho reduzido
echo - Melhor compatibilidade
echo.
echo Para testar, execute: testar-executavel.bat
echo Para distribuir, execute: distribuir-executavel.bat
echo.
pause 