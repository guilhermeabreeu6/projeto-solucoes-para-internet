# app.py

# Importações necessárias:
from flask import Flask, render_template, request, redirect, url_for, session
import sys
import os
# Adiciona o diretório pai ao Python path para encontrar o módulo models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.caixa_eletronico import CaixaEletronico
import random
from functools import wraps

app = Flask(__name__)
# 1. CONFIGURAÇÃO DE SESSÃO: Chave obrigatória para o uso de 'session'
app.secret_key = 'sua_chave_secreta_muito_segura' 

# 2. Instância Única da Classe
caixa = CaixaEletronico() 

# 3. FUNÇÃO AUXILIAR PARA PROTEÇÃO DE ROTA (Opcional, mas limpa)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            # Se não estiver logado, redireciona para a página de login
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------------------------------
# ROTAS DE ACESSO (Login, Cadastro, Index)
# ----------------------------------------------------

@app.route("/")
def index():
    # Verifica se há uma sessão válida E se o cliente ainda está logado no sistema
    if 'logged_in' in session and session['logged_in'] and 'conta_logada' in session:
        # Verifica se o cliente logado ainda existe na sessão do caixa
        if hasattr(caixa, 'cliente_logado') and caixa.cliente_logado is not None:
            return redirect(url_for('menu_principal'))
        else:
            # Se não há cliente logado no sistema, limpa a sessão
            session.pop('logged_in', None)
            session.pop('conta_logada', None)
    
    # Mostra a tela de boas-vindas por padrão
    return render_template("index.html")

@app.route("/home")
def home():
    """Página inicial do site (opcional)"""
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        # ... (Lógica de cadastro)
        nome = request.form.get("nome")
        agencia = request.form.get("agencia")
        conta = request.form.get("conta")
        senha = request.form.get("senha")
        resultado = caixa.cadastrar_cliente(nome, agencia, conta, senha)
        
        return render_template("resultado.html", resultado=resultado, link_text="Fazer Login", link=url_for('login'))
        
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        agencia = request.form.get("agencia")
        conta = request.form.get("conta")
        senha = request.form.get("senha")
        
        if caixa.login(agencia, conta, senha):
            session['logged_in'] = True
            session['conta_logada'] = conta 
            return redirect(url_for('menu_principal'))
        else:
            return render_template("resultado.html", resultado="❌ Login ou Senha inválidos.", link_text="Tentar Novamente", link=url_for('login'))
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    # Limpa a sessão do Flask
    session.pop('logged_in', None)
    session.pop('conta_logada', None)
    
    # Limpa o cliente logado do sistema de caixa
    caixa.cliente_logado = None
    
    return redirect(url_for('index'))  # Volta para a tela de boas-vindas


# ----------------------------------------------------
# ROTAS PROTEGIDAS 
# ----------------------------------------------------

@app.route("/menu_principal")
@login_required # Garante que só usuários logados acessam
def menu_principal():
    """
    Esta função agora serve como o menu principal (Banco vs. Cassino).
    Ela mostra o Saldo/Nome e os botões de navegação.
    """
    dados = caixa.get_dados_cliente()
    # Usa o 'dashboard.html' para mostrar o saldo e os dois botões
    return render_template("dashboard.html", dados=dados)

# ----------------------------------------------------
# ROTAS DO BANCO
# ----------------------------------------------------

@app.route("/acessar_banco")
@login_required
def acessar_banco():
    """Página principal do banco com opções de depósito, saque, PIX e extrato"""
    dados = caixa.get_dados_cliente()
    return render_template("banco.html", dados=dados)

@app.route("/acessar_cassino") 
@login_required
def acessar_cassino():
    """Redireciona para a página do cassino"""
    return redirect(url_for('casino_page'))

@app.route("/perfil")
@login_required  
def perfil():
    """Exibe informações do perfil do cliente"""
    dados = caixa.get_dados_cliente()
    return render_template("perfil.html", dados=dados)

# ----------------------------------------------------
# ROTAS DE OPERAÇÕES BANCÁRIAS
# ----------------------------------------------------

@app.route("/deposito")
@login_required
def pagina_deposito():
    """Página para realizar depósitos"""
    dados = caixa.get_dados_cliente()
    return render_template("deposito.html", dados=dados)

@app.route("/saque")
@login_required
def pagina_saque():
    """Página para realizar saques"""
    dados = caixa.get_dados_cliente()
    return render_template("saque.html", dados=dados)

@app.route("/depositar", methods=["POST"])
@login_required
def depositar():
    valor = request.form["valor"] # Recebe como string, a validação é feita na classe
    resultado = caixa.depositar(valor)
    # Redireciona de volta para o banco após depósito
    return render_template("resultado.html", resultado=resultado, link_text="Voltar ao Banco", link=url_for('acessar_banco'))


@app.route("/sacar", methods=["POST"])
@login_required
def sacar():
    valor = request.form["valor"]
    resultado = caixa.sacar(valor)
    return render_template("resultado.html", resultado=resultado, link_text="Voltar ao Banco", link=url_for('acessar_banco'))


@app.route("/extrato")
@login_required
def mostrar_extrato():
    extrato_lista = caixa.mostrar_extrato()
    return render_template("extrato.html", extrato=extrato_lista) # Você precisará criar 'extrato.html'



# Rota para renderizar o formulário de PIX
@app.route("/pix")
@login_required
def pix_page():
    # Passa o saldo para a tela de PIX 
    dados = caixa.get_dados_cliente()
    return render_template("pix.html", dados=dados)

# Rota para processar o envio do PIX
@app.route("/fazer_pix", methods=["POST"])
@login_required
def fazer_pix():
    chave = request.form.get("chave_destino")
    valor = request.form.get("valor")
    
    resultado = caixa.fazer_pix(chave, valor)
    
    # Retorna para o template de resultado (sucesso ou erro)
    return render_template("resultado.html", 
                           resultado=resultado, 
                           link_text="Voltar ao Banco", 
                           link=url_for('acessar_banco'))

# Rota para cadastrar/consultar a chave PIX
@app.route("/gerenciar_pix", methods=["GET", "POST"])
@login_required
def gerenciar_pix():
    if request.method == "POST":
        nova_chave = request.form.get("nova_chave")
        resultado = caixa.gerenciar_pix(nova_chave)
        
        return render_template("resultado.html", 
                               resultado=resultado, 
                               link_text="Voltar ao Perfil", 
                               link=url_for('perfil'))
        
    # Se for GET, apenas exibe a chave atual
    resultado = caixa.gerenciar_pix(None) # Passa None para a função consultar
    return render_template("resultado.html", 
                           resultado=resultado, 
                           link_text="Voltar ao Perfil", 
                           link=url_for('perfil'))


# ----------------------------------------------------
# ROTAS DO CASINO 
# ----------------------------------------------------

@app.route("/casino")
@login_required
def casino_page():
    dados = caixa.get_dados_cliente()
    # Passa o saldo atualizado para o template do casino
    return render_template("casino.html", saldo=dados['saldo'])

@app.route("/apostar", methods=["POST"])
@login_required
def apostar():
    try:
        aposta = float(request.form["aposta"])
        escolha_usuario = request.form["escolha"]
    except (ValueError, KeyError, TypeError):
        return render_template("resultado.html", resultado="❌ Erro: Valor de aposta ou escolha inválida.", link_text="Tentar Novamente", link=url_for('casino_page'))

    # 1. Checa se o saldo é suficiente (A lógica de limite está na classe, mas checamos aposta positiva)
    if aposta <= 0:
        return render_template("resultado.html", resultado="❌ A aposta deve ser maior que zero.", link_text="Tentar Novamente", link=url_for('casino_page'))

    # 2. Lançamento do Dado
    dado = random.randint(1, 6)
    
    if dado % 2 == 0:
        resultado_dado = "par"
    else:
        resultado_dado = "ímpar"

    # 3. Determinar o ganho/perda e atualizar o saldo
    if escolha_usuario == resultado_dado:
        ganho_ou_perda = aposta
        mensagem = f"🎉 Parabéns! O dado deu {dado} ({resultado_dado}). Você ganhou R${ganho_ou_perda:.2f}!"
    else:
        # Tenta aplicar a perda, a classe checa o limite
        if caixa.cliente_logado["saldo"] - aposta < -caixa.cliente_logado["limite"]:
            return render_template("resultado.html", resultado=f"❌ Limite insuficiente para esta aposta. Saldo: R$ {caixa.cliente_logado['saldo']:.2f}", link_text="Voltar ao Casino", link=url_for('casino_page'))
            
        ganho_ou_perda = -aposta
        mensagem = f"😔 Que pena! O dado deu {dado} ({resultado_dado}). Você perdeu R${aposta:.2f}."

    # Atualiza o saldo e registra no extrato
    novo_saldo = caixa.atualizar_saldo_casino(ganho_ou_perda)
    
    return render_template(
        "resultado.html", 
        resultado=mensagem, 
        detalhe_saldo=f"Seu novo saldo é: R$ {novo_saldo:.2f}",
        link_text="Voltar ao Casino", 
        link=url_for('casino_page')
    )

# ----------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)