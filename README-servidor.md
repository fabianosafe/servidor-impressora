# Servidor de Etiquetas

## Descrição
Servidor Python com interface gráfica que recebe requisições HTTP e exibe os dados recebidos em tempo real.

## Funcionalidades

### Interface Gráfica
- **Botão Ativar/Desativar**: Controla o servidor
- **Status Visual**: Mostra se o servidor está ativo (verde) ou inativo (vermelho)
- **Log em Tempo Real**: Exibe todas as requisições recebidas
- **Configurações**: Permite alterar host e porta
- **Botões de Controle**: Limpar log e copiar conteúdo

### Endpoints da API
- `GET /` - Teste de funcionamento
- `POST /receive` - Recebe dados e exibe no log
- `GET /test` - Teste de conexão

## Como Usar

### 1. Instalar Dependências (Windows)
**Opção 1 - Arquivo Batch (Recomendado):**
```bash
instalar-dependencias.bat
```

**Opção 2 - Comando Manual:**
```bash
py -m pip install flask==2.3.3 flask-cors==4.0.0
```

### 2. Executar o Servidor (Windows)
```bash
py etiqueta-server.py
```

### 3. Ativar o Servidor
- Clique no botão "Ativar Servidor"
- O status mudará para "Ativado" (verde)
- O servidor estará disponível em `http://localhost:5000`

### 4. Enviar Requisições
Exemplo de requisição do Next.js:
```javascript
fetch('http://localhost:5000/receive', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Dados do Next.js',
    timestamp: new Date().toISOString()
  })
})
```

## Configurações

### Host e Porta
- **Host padrão**: localhost
- **Porta padrão**: 5000
- Pode ser alterado na interface

### CORS
- Habilitado para comunicação com aplicações web
- Aceita requisições de qualquer origem

## Log de Requisições

### Formato
```
[HH:MM:SS] Requisição recebida: {
  "message": "Dados do Next.js",
  "timestamp": "2024-01-15T10:30:45.123Z",
  "_timestamp": "2024-01-15T10:30:45.123Z",
  "_method": "POST",
  "_headers": {...}
}
```

### Informações Adicionais
- Timestamp automático
- Método HTTP
- Headers da requisição
- Dados originais

## Controles da Interface

### Botões
- **Ativar/Desativar Servidor**: Controla o servidor
- **Abrir no Navegador**: Abre o servidor no navegador
- **Limpar Log**: Remove todo o conteúdo do log
- **Copiar Log**: Copia o log para a área de transferência

### Status
- **Verde**: Servidor ativo
- **Vermelho**: Servidor inativo

## Exemplo de Uso no Next.js

```javascript
// Componente React
const enviarDados = async (dados) => {
  try {
    const response = await fetch('http://localhost:5000/receive', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    });
    
    const resultado = await response.json();
    console.log('Resposta:', resultado);
    
  } catch (error) {
    console.error('Erro:', error);
  }
};

// Uso
enviarDados({
  tipo: 'etiqueta',
  conteudo: 'Texto da etiqueta',
  quantidade: 1
});
```

## Troubleshooting

### Erro de Porta em Uso
- Altere a porta nas configurações
- Verifique se outro processo está usando a porta 5000

### Erro de CORS
- O servidor já tem CORS habilitado
- Verifique se está usando a URL correta

### Servidor Não Inicia
- Verifique se as dependências estão instaladas
- Verifique se a porta está disponível
- Consulte o log de erros na interface

### Python não reconhecido
- Use `py` em vez de `python` no Windows
- Exemplo: `py etiqueta-server.py`

## Estrutura do Projeto
```
servidor-impressora/
├── etiqueta-server.py           # Servidor principal
├── requirements.txt             # Dependências
├── instalar-dependencias.bat   # Instalador Windows
├── README-servidor.md          # Esta documentação
└── ... (outros arquivos)
``` 