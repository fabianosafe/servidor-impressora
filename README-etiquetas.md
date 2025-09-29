# Funcionalidade de Impressão de Etiquetas

## Descrição
O servidor de etiquetas agora suporta receber requisições específicas para impressão de etiquetas com comandos ZPL gerados automaticamente.

## Como Funciona

### 1. Requisição do Frontend
O frontend (Next.js) gera o comando ZPL e envia uma requisição POST para `/receive` com o tipo `etiqueta_impressao`:

```javascript
{
  "tipo": "etiqueta_impressao",
  "config": {
    "modelo": "ZPLII",
    "dpi": "203",
    "temperatura": "10",
    "velocidade": "-1",
    "margem_esquerda": "0",
    "backfeed": "0",
    "origem": "0",
    "pagina_codigo": "0",
    "limpar_memoria": true,
    "copias": "1",
    "avanco": "0"
  },
  "comando_zpl": "^XA\n^MMD\n^PW394\n^LL118\n^LS0\n^FO20,20^BQN,2,6\n^FDQA,12345^FS\n^FO120,20^A0N,25,25^FD001 - Placa de Mármore^FS\n^FO120,50^A0N,20,20^FDINT-2024-001 - LOTE2024-001^FS\n^FO120,80^A0N,20,20^FDJoão Silva - 15/01/2024 10:30:45^FS\n^XZ"
}
```

### 2. Processamento do Comando ZPL
O servidor recebe e processa o comando ZPL gerado pelo frontend para uma etiqueta de 3cm x 10cm com:

- **QRCode** (lado esquerdo): contém o ID do lote do produto
- **Textos** (lado direito):
  - Linha 1: Código - Nome do Produto
  - Linha 2: Lote Interno - Lote Fabricante
  - Linha 3: Usuário - Data/Hora

### 3. Exibição no Log
O servidor exibe no log:
- Configuração da impressora
- Comando ZPL recebido do frontend

## Estrutura da Etiqueta

### Dimensões
- **Largura**: 10cm (799 dots em 203 DPI)
- **Altura**: 3cm (240 dots em 203 DPI)

### Layout
```
┌─────────────────────────────────────┐
│ [QRCode] │ Código - Nome Produto   │
│          │ Lote Int - Lote Fab     │
│          │ Usuário - Data/Hora     │
└─────────────────────────────────────┘
```

### Posicionamento ZPL
- QRCode: `^FO20,20^BQN,4,8` (posição 20,20) - tamanho aumentado
- Texto linha 1: `^FO350,30^A0N,25,25` (posição 350,30)
- Texto linha 2: `^FO350,70^A0N,20,20` (posição 350,70)
- Texto linha 3: `^FO350,110^A0N,20,20` (posição 350,110)

## Uso no Frontend

### Botão de Impressão
No formulário de catalogação, cada item do histórico tem um botão "Etiqueta" que:

1. Coleta os dados do movimento
2. Gera o comando ZPL no frontend
3. Envia o comando ZPL para o servidor
4. Exibe confirmação de sucesso

### Geração do Comando ZPL
O frontend gera o comando ZPL com:
- **QRCode**: ID do lote do produto ou ID do movimento
- **Código**: Código do produto
- **Nome**: Descrição do produto
- **Lotes**: Interno e fabricante
- **Usuário**: Nome do usuário que catalogou
- **Data/Hora**: Data e hora da catalogação

## Configurações da Impressora

Todas as configurações vêm do frontend:
- **Modelo**: ZPLII (padrão)
- **DPI**: 203 (padrão para impressoras de etiquetas)
- **Temperatura**: 10 (ajustável)
- **Velocidade**: -1 (automática)
- **Margem**: 0 (sem margem)
- **Cópias**: 1 (padrão)

## Controles da Interface

### Botões Disponíveis
- **Ativar/Desativar Servidor**: Controla o servidor
- **Abrir no Navegador**: Abre o servidor no navegador
- **Limpar Log**: Remove todo o conteúdo do log
- **Copiar Log**: Copia o log para a área de transferência
- **Imprimir ZPL**: Envia o último comando ZPL para a impressora
- **Copiar ZPL**: Copia o último comando ZPL para a área de transferência

### Como Usar os Novos Botões

#### Botão "Imprimir ZPL"
1. **Configure a impressora** nas configurações do servidor
2. Envie uma etiqueta do frontend
3. Clique em "Imprimir ZPL" no servidor
4. O comando será enviado para a impressora selecionada
5. Confirmação será exibida no log

#### Botão "Copiar ZPL"
1. Envie uma etiqueta do frontend
2. Clique em "Copiar ZPL" no servidor
3. O comando ZPL será copiado para a área de transferência
4. Cole no [Labelary Viewer](https://labelary.com/viewer.html) para visualizar

### Configuração de Impressora

#### Seleção de Impressora
- **Combobox**: Lista todas as impressoras disponíveis no sistema
- **Botão 🔄**: Atualiza a lista de impressoras
- **Seleção automática**: A primeira impressora é selecionada automaticamente

#### Verificações de Segurança
- Verifica se a impressora selecionada ainda está disponível
- Valida se há impressora selecionada antes de imprimir
- Exibe mensagens de erro específicas para problemas de impressora

## Próximos Passos

1. ✅ **Implementar Impressão Real**: Conectado com a impressora física
2. **Configurações Dinâmicas**: Permitir ajuste de configurações via interface
3. **Diferentes Tipos de Etiqueta**: Suportar outros layouts
4. **Preview**: Mostrar preview da etiqueta antes de imprimir

## Troubleshooting

### Servidor Não Responde
- Verificar se o servidor está ativo
- Verificar se a porta 5000 está disponível
- Verificar logs do servidor

### Comando ZPL Inválido
- Verificar se todos os dados da etiqueta estão presentes
- Verificar se o QRCode não está vazio
- Verificar se os textos não excedem o tamanho da etiqueta

### Erro de CORS
- O servidor já tem CORS habilitado
- Verificar se a URL está correta (http://localhost:5000)

### Problemas de Impressora
- **Nenhuma impressora encontrada**: Verificar se há impressoras instaladas no Windows
- **Impressora não disponível**: Atualizar lista de impressoras com o botão 🔄
- **Erro de impressão**: Verificar se a impressora está ligada e conectada
- **Permissões**: Verificar se o usuário tem permissão para imprimir

### Problemas de Layout
- **Texto cortado**: Ajustar posicionamento ZPL no frontend (catalogacao-form.tsx)
- **QR Code muito grande**: Reduzir tamanho do QR Code (parâmetro 2,6)
- **Texto muito pequeno**: Aumentar tamanho da fonte (parâmetros 20,20, 18,18)
- **Espaçamento inadequado**: Ajustar posições X,Y dos elementos 