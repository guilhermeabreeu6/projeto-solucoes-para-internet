# 💰 Sistema de Caixa Eletrônico e Cassino

Um sistema web completo desenvolvido em Flask que simula um caixa eletrônico bancário com funcionalidades de cassino integradas.

## 🚀 Funcionalidades

### 🏦 Sistema Bancário
- **Cadastro de usuários** com dados completos
- **Sistema de login** seguro com sessões
- **Operações bancárias**:
  - Depósito
  - Saque (com limite de cheque especial)
  - Consulta de saldo
  - Extrato detalhado
- **Sistema PIX**:
  - Cadastro de chave PIX
  - Transferências entre contas
  - Consulta de chave

### 🎲 Cassino
- **Jogo de dados** (Par ou Ímpar)
- **Sistema de apostas** integrado ao saldo bancário
- **Histórico de jogos** no extrato

### 💾 Persistência de Dados
- **Armazenamento em JSON** para manter dados entre reinicializações
- **Backup automático** de todas as transações
- **Carregamento automático** dos dados ao iniciar

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.x + Flask
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Template Engine**: Jinja2
- **Persistência**: JSON
- **Sessões**: Flask Sessions

## 📁 Estrutura do Projeto

```
projeto_caixa/
├── meu_caixa_web/
│   ├── app.py                 # Aplicação Flask principal
│   ├── models/
│   │   └── caixa_eletronico.py # Lógica de negócio
│   ├── templates/             # Templates HTML
│   │   ├── index.html         # Página inicial
│   │   ├── login.html         # Tela de login
│   │   ├── cadastro.html      # Cadastro de usuários
│   │   ├── dashboard.html     # Menu principal
│   │   ├── banco.html         # Operações bancárias
│   │   ├── casino.html        # Jogos do cassino
│   │   ├── perfil.html        # Perfil do usuário
│   │   ├── extrato.html       # Extrato bancário
│   │   └── resultado.html     # Resultados de operações
│   ├── static/                # Arquivos estáticos
│   └── clientes.json          # Base de dados (criado automaticamente)
├── .gitignore
└── README.md
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- Flask

### Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/SEU_USUARIO/projeto-caixa-eletronico.git
cd projeto-caixa-eletronico
```

2. **Instale as dependências**:
```bash
pip install flask
```

3. **Execute a aplicação**:
```bash
cd meu_caixa_web
python app.py
```

4. **Acesse no navegador**:
```
http://localhost:5000
```

## 📝 Como Usar

1. **Primeiro acesso**: Acesse a página inicial e clique em "Cadastrar"
2. **Cadastro**: Preencha os dados (nome, agência, conta, senha)
3. **Login**: Use os dados cadastrados para fazer login
4. **Menu Principal**: Escolha entre operações bancárias ou cassino
5. **Operações**: Realize depósitos, saques, PIX ou jogue no cassino

## 🎮 Regras do Cassino

- **Jogo**: Dado de 6 faces (Par ou Ímpar)
- **Aposta mínima**: R$ 0,01
- **Aposta máxima**: Limitada pelo saldo + limite disponível
- **Pagamento**: 1:1 (se apostar R$ 10 e ganhar, recebe R$ 10 de lucro)

## 🔒 Segurança

- **Sessões seguras** com chaves secretas
- **Validação de entrada** em todos os formulários
- **Proteção de rotas** com decorador `@login_required`
- **Limpeza automática** de sessões inconsistentes

## 📊 Dados de Exemplo

O sistema cria contas com saldo inicial de R$ 1.000,00 e limite de R$ 5.000,00.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido como projeto acadêmico para a disciplina de Soluções para Internet.

---

⭐ **Não esqueça de dar uma estrela se este projeto te ajudou!**