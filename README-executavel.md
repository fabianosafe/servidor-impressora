# 🚀 Criando Executável do Servidor de Etiquetas

Este guia explica como criar um executável standalone do servidor de etiquetas para distribuição.

## 📋 Pré-requisitos

- Python 3.7+ instalado
- Windows 10/11
- Conexão com internet (para baixar dependências)

## 🛠️ Métodos de Criação

### Método 1: Interface Gráfica (Recomendado para iniciantes)

1. **Execute o script:**
   ```
   criar-executavel.bat
   ```

2. **Siga as instruções na tela:**
   - Selecione: `etiqueta-server.py`
   - Escolha: "One File" (um arquivo)
   - Escolha: "Window Based" (sem console)
   - Nome: `Servidor-Etiquetas`
   - Clique: "Convert .py to .exe"

### Método 2: Linha de Comando (Avançado)

1. **Execute o script:**
   ```
   criar-executavel-direto.bat
   ```

2. **Aguarde a conclusão automática**

## 📁 Resultado

Após a criação, você terá:

```
dist/
└── Servidor-Etiquetas.exe  (arquivo único ~50-100MB)
```

## 📦 Distribuição

### Para o usuário final:

1. **Copie apenas o arquivo:** `Servidor-Etiquetas.exe`
2. **Envie por email, pendrive, etc.**
3. **O usuário só precisa clicar duas vezes no arquivo**

### Vantagens do executável:

✅ **Não precisa instalar Python**
✅ **Não precisa instalar dependências**
✅ **Funciona em qualquer Windows**
✅ **Interface gráfica completa**
✅ **Todas as funcionalidades incluídas**

## 🔧 Configurações do Executável

### Parâmetros usados:

```bash
pyinstaller --onefile          # Um arquivo único
            --windowed         # Sem console (interface gráfica)
            --name "Servidor-Etiquetas"  # Nome do executável
            --add-data "README-*.md;."   # Incluir documentação
```

### Incluído no executável:

- ✅ Python interpreter
- ✅ tkinter (interface gráfica)
- ✅ Flask (servidor web)
- ✅ win32print (impressão)
- ✅ pyperclip (área de transferência)
- ✅ flask-cors (CORS)
- ✅ Seu código Python

## 🚨 Solução de Problemas

### Erro: "Falha ao instalar dependências"
- Verifique se o Python está instalado
- Execute: `python --version`
- Tente: `pip install --upgrade pip`

### Erro: "Falha ao criar executável"
- Verifique se há espaço em disco (precisa ~2GB)
- Feche outros programas
- Execute como administrador

### Antivírus detecta como vírus
- Adicione exceção no antivírus
- É um falso positivo comum
- O código é seguro

### Executável não abre
- Verifique se o Windows Defender não bloqueou
- Execute como administrador
- Verifique se há impressoras instaladas

## 📊 Tamanho do Executável

- **Tamanho típico:** 50-100MB
- **Razão:** Inclui Python + todas as dependências
- **Vantagem:** Funciona sem instalação

## 🔄 Atualizações

Para atualizar o executável:

1. **Modifique o código:** `etiqueta-server.py`
2. **Execute novamente:** `criar-executavel.bat`
3. **Distribua o novo:** `Servidor-Etiquetas.exe`

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs** no console
2. **Teste o código Python** diretamente
3. **Verifique as dependências** no `requirements.txt`

---

## 🎯 Resumo Rápido

1. **Execute:** `criar-executavel.bat`
2. **Configure:** Interface gráfica
3. **Aguarde:** Criação do executável
4. **Distribua:** `Servidor-Etiquetas.exe`
5. **Pronto!** Usuário só clica duas vezes 