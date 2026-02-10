import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import webbrowser
import win32print
import win32con
import pyperclip

class EtiquetaServer:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor de Impressão de Etiquetas")
        
        # Configurar tamanho mínimo e permitir redimensionamento automático
        self.root.minsize(400, 400)  # Tamanho mínimo
        # Removido geometry fixo para permitir altura automática
        
        # Variáveis de controle
        self.server_running = False
        self.server_thread = None
        self.app = None
        
        # Configurações do servidor
        # self.host = "localhost"
        self.host = "0.0.0.0"
        self.port = 5000
        
        # Variável para armazenar o último comando ZPL recebido
        self.ultimo_comando_zpl = ""
        
        # Variável para armazenar a impressora selecionada
        self.impressora_selecionada = ""
        
        # Variável para controlar impressão automática
        self.impressao_automatica = False
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # ===== CONTROLES DO SERVIDOR =====
        server_frame = ttk.LabelFrame(main_frame, text="Controle do Servidor", padding="10")
        server_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Configurar colunas para melhor distribuição
        server_frame.columnconfigure(1, weight=1)
        
        # Status do servidor
        ttk.Label(server_frame, text="Status:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.status_var = tk.StringVar(value="Desativado")
        self.status_label = ttk.Label(server_frame, textvariable=self.status_var, 
                                     foreground="red", font=("Arial", 10, "bold"))
        self.status_label.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Botão ativar/desativar na mesma linha do status
        self.toggle_button = ttk.Button(server_frame, text="Ativar Servidor", 
                                       command=self.toggle_server, style="Accent.TButton")
        self.toggle_button.grid(row=0, column=2, pady=2, padx=(20, 0), sticky=tk.E)
        
        # Endereço do servidor
        ttk.Label(server_frame, text="Endereço:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.address_var = tk.StringVar(value=f"http://{self.host}:{self.port}")
        ttk.Label(server_frame, textvariable=self.address_var, 
                 font=("Arial", 9, "italic")).grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Botão abrir no navegador na mesma linha do endereço
        self.browser_button = ttk.Button(server_frame, text="Testar resposta no Navegador", 
                                        command=self.abrir_navegador, state="disabled")
        self.browser_button.grid(row=1, column=2, pady=2, padx=(20, 0), sticky=tk.E)
        
        # ===== LOG DE REQUISIÇÕES =====
        log_frame = ttk.LabelFrame(main_frame, text="Log de Requisições", padding="10")
        log_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=3)  # Coluna da caixa de texto com peso maior
        log_frame.columnconfigure(1, weight=0)  # Coluna dos botões sem expansão
        log_frame.rowconfigure(0, weight=1)
        
        # Área de texto para log (largura reduzida)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=60, 
                                                font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        
        # Frame para botões à direita da caixa de texto
        buttons_frame = ttk.Frame(log_frame)
        buttons_frame.grid(row=0, column=1, sticky=(tk.N, tk.E), padx=(0, 0))
        
        # Botões organizados verticalmente
        ttk.Button(buttons_frame, text="Limpar Log", 
                  command=self.limpar_log, width=15).grid(row=0, column=0, pady=(0, 8), sticky=tk.W)
        
        ttk.Button(buttons_frame, text="Copiar Log", 
                  command=self.copiar_log, width=15).grid(row=1, column=0, pady=(0, 8), sticky=tk.W)
        
        ttk.Button(buttons_frame, text="Imprimir ZPL", 
                  command=self.imprimir_zpl, width=15).grid(row=2, column=0, pady=(0, 8), sticky=tk.W)
        
        ttk.Button(buttons_frame, text="Copiar ZPL", 
                  command=self.copiar_zpl, width=15).grid(row=3, column=0, pady=(0, 8), sticky=tk.W)
        
        ttk.Button(buttons_frame, text="Abrir Labelary", 
                  command=self.abrir_labelary, width=15).grid(row=4, column=0, pady=(0, 0), sticky=tk.W)
        
        # ===== CONFIGURAÇÕES =====
        config_frame = ttk.LabelFrame(main_frame, text="Configurações da Impressora", padding="10")
        config_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Porta
        ttk.Label(config_frame, text="Porta:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.port_var = tk.StringVar(value=str(self.port))
        port_entry = ttk.Entry(config_frame, textvariable=self.port_var, width=10)
        port_entry.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Host
        ttk.Label(config_frame, text="Host:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.host_var = tk.StringVar(value=self.host)
        host_entry = ttk.Entry(config_frame, textvariable=self.host_var, width=15)
        host_entry.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Impressora
        ttk.Label(config_frame, text="Impressora:").grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Frame para impressora
        printer_frame = ttk.Frame(config_frame)
        printer_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # Combobox para selecionar impressora
        self.printer_var = tk.StringVar()
        self.printer_combo = ttk.Combobox(printer_frame, textvariable=self.printer_var, 
                                         state="readonly", width=30)
        self.printer_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.printer_combo.bind('<<ComboboxSelected>>', self.on_printer_change)
        
        # Botão para atualizar lista de impressoras
        ttk.Button(printer_frame, text="🔄", width=3, 
                  command=self.atualizar_impressoras).pack(side=tk.LEFT, padx=(5, 0))
        
        # Switch para impressão automática
        ttk.Label(config_frame, text="Impressão Automática:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.impressao_auto_var = tk.BooleanVar(value=False)
        self.impressao_auto_check = ttk.Checkbutton(config_frame, 
                                                   text="Imprimir automaticamente ao receber etiqueta",
                                                   variable=self.impressao_auto_var,
                                                   command=self.on_impressao_auto_change)
        self.impressao_auto_check.grid(row=3, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Carregar impressoras na inicialização
        self.atualizar_impressoras()
    
    def atualizar_impressoras(self):
        """Atualiza a lista de impressoras disponíveis"""
        try:
            impressoras = []
            for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
                impressoras.append(printer[2])
            
            if impressoras:
                self.printer_combo['values'] = impressoras
                if not self.printer_var.get() or self.printer_var.get() not in impressoras:
                    self.printer_var.set(impressoras[0])
                    self.impressora_selecionada = impressoras[0]
                
                self.adicionar_log(f"✅ {len(impressoras)} impressora(s) encontrada(s)")
            else:
                self.printer_combo['values'] = ["Nenhuma impressora encontrada"]
                self.printer_var.set("Nenhuma impressora encontrada")
                self.impressora_selecionada = ""
                self.adicionar_log("⚠️ Nenhuma impressora encontrada no sistema")
                
        except Exception as e:
            self.printer_combo['values'] = ["Erro ao carregar impressoras"]
            self.printer_var.set("Erro ao carregar impressoras")
            self.impressora_selecionada = ""
            self.adicionar_log(f"❌ Erro ao carregar impressoras: {str(e)}")
    
    def on_printer_change(self, event=None):
        """Callback quando a impressora é alterada"""
        self.impressora_selecionada = self.printer_var.get()
        if self.impressora_selecionada and self.impressora_selecionada != "Nenhuma impressora encontrada":
            self.adicionar_log(f"🖨️ Impressora selecionada: {self.impressora_selecionada}")
    
    def on_impressao_auto_change(self):
        """Callback quando o switch de impressão automática é alterado"""
        self.impressao_automatica = self.impressao_auto_var.get()
        status = "ativada" if self.impressao_automatica else "desativada"
        self.adicionar_log(f"⚙️ Impressão automática {status}")
        
    def processar_comando_zpl(self, dados):
        """Processa comando ZPL recebido do frontend"""
        try:
            # Extrair dados da requisição
            config = dados.get('config', {})
            comando_zpl = dados.get('comando_zpl', '')
            
            # Configurações da impressora (vindas do frontend)
            modelo = config.get('modelo', 'ZPLII')
            dpi = config.get('dpi', '203')
            temperatura = config.get('temperatura', '10')
            velocidade = config.get('velocidade', '-1')
            margem_esquerda = config.get('margem_esquerda', '0')
            backfeed = config.get('backfeed', '0')
            origem = config.get('origem', '0')
            pagina_codigo = config.get('pagina_codigo', '0')
            limpar_memoria = config.get('limpar_memoria', True)
            copias = config.get('copias', '1')
            avanco = config.get('avanco', '0')
            
            # Armazenar o comando ZPL para uso posterior
            self.ultimo_comando_zpl = comando_zpl
            
            # Retornar comando ZPL recebido do frontend
            return comando_zpl
            
        except Exception as e:
            return f"ERRO AO PROCESSAR ZPL: {str(e)}"
    
    def toggle_server(self):
        """Ativa ou desativa o servidor"""
        if not self.server_running:
            self.iniciar_servidor()
        else:
            self.parar_servidor()
    
    def iniciar_servidor(self):
        """Inicia o servidor Flask em uma thread separada"""
        try:
            self.port = int(self.port_var.get())
            self.host = self.host_var.get()
            
            # Criar aplicação Flask
            self.app = Flask(__name__)
            CORS(self.app)  # Habilitar CORS
            
            # Configurar rotas
            self.configurar_rotas()
            
            # Iniciar servidor em thread separada
            self.server_thread = threading.Thread(target=self.executar_servidor, daemon=True)
            self.server_thread.start()
            
            # Atualizar interface
            self.server_running = True
            self.status_var.set("Ativado")
            self.status_label.config(foreground="green")
            self.toggle_button.config(text="Desativar Servidor")
            self.browser_button.config(state="normal")
            self.address_var.set(f"http://{self.host}:{self.port}")
            
            # Ativar impressão automática por padrão quando servidor é iniciado
            self.impressao_auto_var.set(True)
            self.impressao_automatica = True
            
            self.adicionar_log("Servidor iniciado com sucesso!")
            self.adicionar_log("⚙️ Impressão automática ativada por padrão")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar servidor:\n{str(e)}")
            self.adicionar_log(f"ERRO: {str(e)}")
    
    def parar_servidor(self):
        """Para o servidor"""
        try:
            self.server_running = False
            self.status_var.set("Desativado")
            self.status_label.config(foreground="red")
            self.toggle_button.config(text="Ativar Servidor")
            self.browser_button.config(state="disabled")
            
            self.adicionar_log("Servidor parado.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao parar servidor:\n{str(e)}")
    
    def executar_servidor(self):
        """Executa o servidor Flask"""
        try:
            self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
        except Exception as e:
            self.adicionar_log(f"ERRO NO SERVIDOR: {str(e)}")
    
    def configurar_rotas(self):
        """Configura as rotas do Flask"""
        
        @self.app.route('/', methods=['GET'])
        def home():
            return jsonify({
                "status": "Servidor de Impressao de Etiquetas funcionando!",
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/receive', methods=['POST'])
        def receive_data():
            try:
                # Obter dados da requisição
                if request.is_json:
                    data = request.get_json()
                else:
                    data = request.form.to_dict()
                
                # Adicionar timestamp
                data['_timestamp'] = datetime.now().isoformat()
                data['_method'] = request.method
                data['_headers'] = dict(request.headers)
                
                # Verificar se é uma requisição de etiqueta
                if data.get('tipo') == 'etiqueta_impressao':
                    # Processar comando ZPL recebido
                    comando_zpl = self.processar_comando_zpl(data)
                    
                    # Mostrar no log
                    self.adicionar_log(f"=== REQUISIÇÃO DE ETIQUETA ===\n")
                    self.adicionar_log(f"Configuração: {json.dumps(data.get('config', {}), indent=2, ensure_ascii=False)}")
                    self.adicionar_log(f"=== COMANDO ZPL RECEBIDO ===\n{comando_zpl}\n")
                    
                    # Verificar se impressão automática está ativada
                    if self.impressao_automatica:
                        try:
                            self.imprimir_zpl_automatico(comando_zpl)
                        except Exception as e:
                            self.adicionar_log(f"❌ Erro na impressão automática: {str(e)}")
                else:
                    # Mostrar no log (requisição normal)
                    self.adicionar_log(f"Requisição recebida: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
                return jsonify({
                    "status": "Dados recebidos com sucesso!",
                    "data": data
                })
                
            except Exception as e:
                error_msg = f"Erro ao processar requisição: {str(e)}"
                self.adicionar_log(f"ERRO: {error_msg}")
                return jsonify({"error": error_msg}), 500
        
        @self.app.route('/test', methods=['GET'])
        def test():
            return jsonify({
                "message": "Teste de conexão",
                "timestamp": datetime.now().isoformat()
            })
    
    def adicionar_log(self, mensagem):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}\n"
        
        # Adicionar na thread principal
        self.root.after(0, lambda: self.log_text.insert(tk.END, log_entry))
        self.root.after(0, lambda: self.log_text.see(tk.END))
    
    def limpar_log(self):
        """Limpa o log"""
        self.log_text.delete(1.0, tk.END)
    
    def copiar_log(self):
        """Copia o conteúdo do log para a área de transferência"""
        try:
            log_content = self.log_text.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(log_content)
            messagebox.showinfo("Log Copiado", "Conteúdo do log copiado para a área de transferência!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar log:\n{str(e)}")
    
    def imprimir_zpl(self):
        """Envia o último comando ZPL para a impressora"""
        try:
            if not self.ultimo_comando_zpl:
                messagebox.showwarning("Aviso", "Nenhum comando ZPL recebido ainda. Envie uma etiqueta primeiro.")
                return
            
            self.imprimir_zpl_automatico(self.ultimo_comando_zpl)
            messagebox.showinfo("Sucesso", f"Comando ZPL enviado para impressora: {self.impressora_selecionada}")
                
        except Exception as e:
            error_msg = f"Erro ao imprimir ZPL: {str(e)}"
            messagebox.showerror("Erro de Impressão", error_msg)
            self.adicionar_log(f"❌ {error_msg}")
    
    def imprimir_zpl_automatico(self, comando_zpl):
        """Envia comando ZPL específico para a impressora (usado para impressão automática)"""
        # Verificar se há impressora selecionada
        if not self.impressora_selecionada or self.impressora_selecionada == "Nenhuma impressora encontrada":
            raise Exception("Nenhuma impressora selecionada. Selecione uma impressora nas configurações.")
        
        # Verificar se a impressora ainda existe
        impressoras_disponiveis = []
        try:
            for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
                impressoras_disponiveis.append(printer[2])
        except:
            pass
        
        if self.impressora_selecionada not in impressoras_disponiveis:
            raise Exception(f"Impressora '{self.impressora_selecionada}' não está mais disponível. Atualize a lista de impressoras.")
        
        # Abrir a impressora
        handle = win32print.OpenPrinter(self.impressora_selecionada)
        try:
            # Iniciar um trabalho de impressão RAW
            hJob = win32print.StartDocPrinter(handle, 1, ("Etiqueta ZPL", None, "RAW"))
            win32print.StartPagePrinter(handle)
            win32print.WritePrinter(handle, comando_zpl.encode("ascii"))
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            
            self.adicionar_log(f"🖨️ Etiqueta impressa automaticamente na impressora: {self.impressora_selecionada}")
            
        finally:
            win32print.ClosePrinter(handle)
    
    def copiar_zpl(self):
        """Copia o último comando ZPL para a área de transferência"""
        try:
            if not self.ultimo_comando_zpl:
                messagebox.showwarning("Aviso", "Nenhum comando ZPL recebido ainda. Envie uma etiqueta primeiro.")
                return
            
            # Copiar para a área de transferência usando pyperclip
            pyperclip.copy(self.ultimo_comando_zpl)
            
            messagebox.showinfo("ZPL Copiado", "Comando ZPL copiado para a área de transferência!\n\nAgora você pode colar no site de visualização.")
            self.adicionar_log("✅ Comando ZPL copiado para área de transferência")
            
        except Exception as e:
            error_msg = f"Erro ao copiar ZPL: {str(e)}"
            messagebox.showerror("Erro", error_msg)
            self.adicionar_log(f"❌ {error_msg}")
    
    def abrir_navegador(self):
        """Abre o servidor no navegador"""
        try:
            url = f"http://{self.host}:{self.port}"
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir navegador:\n{str(e)}")
    
    def abrir_labelary(self):
        """Abre o site do Labelary Viewer no navegador"""
        try:
            url = "https://labelary.com/viewer.html"
            webbrowser.open(url)
            self.adicionar_log("🌐 Labelary Viewer aberto no navegador")
        except Exception as e:
            error_msg = f"Erro ao abrir Labelary Viewer: {str(e)}"
            messagebox.showerror("Erro", error_msg)
            self.adicionar_log(f"❌ {error_msg}")

def main():
    root = tk.Tk()
    app = EtiquetaServer(root)
    root.mainloop()

if __name__ == "__main__":
    main()