# Sistema de Gestão de Franquias

## Descrição

O Sistema de Gestão de Franquias é uma aplicação web desenvolvida em Python e Django para gerenciamento operacional de franquias. O sistema permite o controle centralizado de usuários, produtos, estoque e vendas, oferecendo uma solução completa para administração de unidades franqueadas.

O projeto foi desenvolvido com foco em organização, segurança, escalabilidade e facilidade de manutenção.

---

## Principais Funcionalidades

### Gestão de Franquias
- Cadastro e gerenciamento de franquias
- Associação de usuários às unidades
- Controle operacional por franquia

### Gestão de Usuários
- Sistema de autenticação integrado ao Django
- Perfis de acesso:
  - Administrador
  - Gestor
  - Operador
- Controle de permissões por função

### Gestão de Produtos
- Cadastro de produtos
- Controle de preços
- Ativação e inativação de produtos
- Consulta rápida de informações

### Controle de Estoque
- Controle de entrada e saída de mercadorias
- Estoque individual por franquia
- Atualização automática após vendas
- Validação de disponibilidade antes da venda

### Ponto de Venda (PDV)
- Pesquisa de produtos
- Carrinho de compras
- Cálculo automático de totais
- Suporte a múltiplas formas de pagamento:
  - Dinheiro
  - Cartão
  - PIX
- Cálculo automático de troco
- Emissão de comprovante de venda

### Gestão de Vendas
- Registro completo das transações
- Histórico de vendas
- Controle dos itens vendidos
- Atualização automática do estoque

---

## Tecnologias Utilizadas

- Python 3
- Django
- SQLite3
- HTML5
- CSS3
- JavaScript

---

## Estrutura do Projeto

```text
franquias/
│
├── franquias/
├── usuarios/
├── produtos/
├── estoque/
├── vendas/
│
├── templates/
├── static/
│
├── manage.py
└── requirements.txt
```

---

## Instalação

### Clonar o repositório

```bash
git clone https://github.com/vieira1herbert/gruponatureza
cd gruponatureza
```

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

Linux ou macOS:

```bash
source venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Configuração do Banco de Dados

Aplicar as migrações:

```bash
python manage.py makemigrations
python manage.py migrate
```

Criar usuário administrador:

```bash
python manage.py createsuperuser
```

---

## Execução do Projeto

Iniciar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

A aplicação estará disponível em:

```text
http://127.0.0.1:8000/
```

Painel administrativo:

```text
http://127.0.0.1:8000/admin/
```

---

## Fluxo Operacional

1. Cadastro de franquias e usuários.
2. Cadastro de produtos.
3. Abastecimento de estoque por franquia.
4. Realização de vendas através do PDV.
5. Atualização automática do estoque.
6. Registro das vendas no sistema.
7. Consulta de histórico e informações gerenciais.

---

## Segurança

O sistema implementa recursos de segurança fornecidos pelo Django:

- Autenticação de usuários
- Controle de permissões por perfil
- Proteção contra CSRF
- Validação de dados no servidor
- Controle transacional para operações críticas
- Verificação de estoque antes da conclusão da venda

---

## Possíveis Evoluções

- Dashboard gerencial
- Relatórios em PDF
- Integração com impressoras térmicas
- Leitura de código de barras
- API REST
- Integração com sistemas ERP
- Controle financeiro
- Multiempresa
- Aplicação mobile

---
