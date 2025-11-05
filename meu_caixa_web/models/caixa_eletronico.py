# models/caixa_eletronico.py

from datetime import datetime
import json
import os

class CaixaEletronico:
    def __init__(self):
        # O cliente será armazenado aqui após o login
        self.cliente_logado = None 
        # Arquivo onde serão salvos os dados dos clientes
        self.arquivo_dados = 'clientes.json'
        # Carrega os dados existentes ou cria um dicionário vazio
        self.clientes = self._carregar_dados() 

    def _timestamp(self):
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    def _carregar_dados(self):
        """Carrega os dados dos clientes do arquivo JSON"""
        try:
            if os.path.exists(self.arquivo_dados):
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                print(f"✅ Dados carregados: {len(dados)} clientes encontrados")
                return dados
            else:
                print("📁 Arquivo de dados não encontrado. Criando novo banco de dados.")
                return {}
        except (json.JSONDecodeError, Exception) as e:
            print(f"❌ Erro ao carregar dados: {e}. Criando novo banco de dados.")
            return {}

    def _salvar_dados(self):
        """Salva os dados dos clientes no arquivo JSON"""
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(self.clientes, f, indent=2, ensure_ascii=False)
            print(f"💾 Dados salvos: {len(self.clientes)} clientes")
        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")

    def cadastrar_cliente(self, nome, agencia, conta, senha):
        if conta in self.clientes:
            return "❌ Conta já cadastrada."
            
        self.clientes[conta] = {
            "nome": nome.strip(),
            "agencia": agencia.strip(),
            "conta": conta.strip(),
            "senha": senha.strip(),
            "saldo": 1000.00,  # Saldo inicial fictício
            "limite": 5000.0,
            "chave_pix": None,
            "extrato": [f"{self._timestamp()} - Saldo Inicial +R$ 1000.00"]
        }
        # Salva os dados após cadastrar um novo cliente
        self._salvar_dados()
        return "✅ Cliente cadastrado com sucesso! Use a conta e senha para logar."

    def login(self, agencia, conta, senha):
        if conta in self.clientes and \
           self.clientes[conta]["agencia"] == agencia.strip() and \
           self.clientes[conta]["senha"] == senha.strip():
            
            self.cliente_logado = self.clientes[conta]
            return True
        else:
            self.cliente_logado = None
            return False

    # --- Funções que operam no cliente logado (self.cliente_logado) ---

    def consultar_saldo(self):
        if not self.cliente_logado:
            return "❌ Erro: Nenhum cliente logado."
        
        saldo = self.cliente_logado["saldo"]
        return f"R$ {saldo:.2f}"

    def get_dados_cliente(self):
        if not self.cliente_logado:
            return None
        
        c = self.cliente_logado
        limite_usado = abs(c["saldo"]) if c["saldo"] < 0 else 0
        
        dados = {
            "nome": c["nome"],
            "agencia": c["agencia"],
            "conta": c["conta"],
            "saldo": c["saldo"],
            "limite_total": c["limite"],
            "limite_disponivel": c["limite"] - limite_usado,
            "chave_pix": c["chave_pix"] if c["chave_pix"] else "Nenhuma"
        }
        return dados

    def depositar(self, valor):
        if not self.cliente_logado:
            return "❌ Erro: Nenhum cliente logado."
        
        try:
            valor = float(valor)
        except ValueError:
            return "❌ Valor inválido."

        if valor <= 0:
            return "❌ O valor deve ser maior que zero."

        self.cliente_logado["saldo"] += valor
        self.cliente_logado["extrato"].append(f"{self._timestamp()} - Depósito +R$ {valor:.2f}")
        # Salva os dados após depósito
        self._salvar_dados()
        return f"✅ Depósito de R$ {valor:.2f} realizado. Novo saldo: R$ {self.cliente_logado['saldo']:.2f}"

    def sacar(self, valor):
        if not self.cliente_logado:
            return "❌ Erro: Nenhum cliente logado."

        try:
            valor = float(valor)
        except ValueError:
            return "❌ Valor inválido."

        if valor <= 0:
            return "❌ O valor deve ser maior que zero."
        
        if self.cliente_logado["saldo"] - valor < -self.cliente_logado["limite"]:
            return "❌ Limite insuficiente (incluindo cheque especial)."

        self.cliente_logado["saldo"] -= valor
        self.cliente_logado["extrato"].append(f"{self._timestamp()} - Saque -R$ {valor:.2f}")
        # Salva os dados após saque
        self._salvar_dados()
        return f"✅ Saque de R$ {valor:.2f} realizado. Novo saldo: R$ {self.cliente_logado['saldo']:.2f}"

    def mostrar_extrato(self):
        if not self.cliente_logado:
            return ["❌ Erro: Nenhum cliente logado."]
        
        if self.cliente_logado["extrato"]:
            return self.cliente_logado["extrato"]
        else:
            return ["Nenhuma movimentação registrada."]
    
    def fazer_pix(self, chave_destino, valor):
        if not self.cliente_logado:
            return "❌ Erro: Nenhum cliente logado."
            
        c = self.cliente_logado
        try:
            valor = float(valor)
        except ValueError:
            return "❌ Valor inválido. Digite um número."

        if valor <= 0:
            return "❌ O valor deve ser maior que zero."

        # Verifica limite (considerando saldo e limite)
        if c["saldo"] - valor < -c["limite"]: 
            return "❌ Limite insuficiente para realizar o PIX."

        # **Simulação de Transferência:**
        # 1. Busca pelo destino (no modelo em memória)
        cliente_destino = None
        for conta, dados in self.clientes.items():
            if dados.get("chave_pix") == chave_destino:
                cliente_destino = dados
                break
                
        if not cliente_destino:
             # Se não encontrar a chave destino, simula falha
             return "❌ Chave PIX de destino não encontrada."
                
        # 2. Executa a transação (saque do remetente)
        c["saldo"] -= valor
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        c["extrato"].append(f"{timestamp} - PIX enviado para {chave_destino} -R$ {valor:.2f}")

        # 3. Executa a transação (depósito no destino)
        cliente_destino["saldo"] += valor
        cliente_destino["extrato"].append(f"{timestamp} - PIX recebido de {c['nome']} +R$ {valor:.2f}")

        # Salva os dados após transação PIX
        self._salvar_dados()
        return f"✅ PIX de R$ {valor:.2f} enviado com sucesso para {chave_destino}."

    def gerenciar_pix(self, nova_chave=None):
        # 'self.cliente_logado' deve ser o objeto/dicionário do cliente logado
        c = self.cliente_logado
        
        # 1. Cadastro/Atualização
        if nova_chave and nova_chave.strip():
            # Lógica de cadastro (em memória)
            c["chave_pix"] = nova_chave.strip()
            # Salva os dados após cadastrar/atualizar chave PIX
            self._salvar_dados()
            return f"✅ Chave PIX '{nova_chave}' cadastrada/atualizada com sucesso!"
        
        # 2. Consulta (Se não houver nova chave, retorna a atual)
        else:
            return c.get("chave_pix", "Nenhuma chave cadastrada") # Retorna a chave ou 'Nenhuma chave cadastrada'
    
    # Novo método para o Casino
    def atualizar_saldo_casino(self, ganho_ou_perda):
        if not self.cliente_logado:
            return "❌ Erro: Nenhum cliente logado."
            
        self.cliente_logado["saldo"] += ganho_ou_perda
        
        if ganho_ou_perda > 0:
            self.cliente_logado["extrato"].append(f"{self._timestamp()} - Casino (Ganho) +R$ {abs(ganho_ou_perda):.2f}")
        else:
            self.cliente_logado["extrato"].append(f"{self._timestamp()} - Casino (Perda) -R$ {abs(ganho_ou_perda):.2f}")
        
        # Salva os dados após atualização do casino
        self._salvar_dados()
        return self.cliente_logado["saldo"]


