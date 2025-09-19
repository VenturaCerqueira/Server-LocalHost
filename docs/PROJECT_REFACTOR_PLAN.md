# Plano de Refatoração e Organização do Projeto

## Objetivo
Dividir o arquivo grande `main_controller.py` em controladores menores, organizados por domínio, para melhorar a manutenção, legibilidade e escalabilidade do projeto.

## Estrutura Proposta

### 1. Controladores (Controllers)
Criar pastas e arquivos para cada domínio funcional, por exemplo:

- **controllers/**
  - **user_controller.py**  
    - Rotas e funções relacionadas a usuários, autenticação, perfil, login, logout, registro.
  - **database_controller.py**  
    - Rotas e funções relacionadas à gestão do banco de dados, importação, exportação, análise.
  - **file_controller.py**  
    - Rotas e funções para navegação de arquivos, upload, download, pastas seguras.
  - **system_links_controller.py**  
    - Rotas para gerenciamento de links de sistemas, portais, sincronização.
  - **admin_controller.py**  
    - Rotas administrativas, gerenciamento de papéis, permissões, dashboards.
  - **api_controller.py** (separado, já existente)
  - **auth_controller.py** (separado, já existente)

### 2. Serviços (Services)
Manter serviços que encapsulam lógica de negócio e acesso a dados, como já está organizado.

### 3. Scripts
Consolidar scripts em uma pasta única, com subpastas se necessário.

### 4. Testes
Organizar testes por domínio, refletindo a estrutura dos controladores.

### 5. Documentação
Criar um README.md ou documentação detalhada explicando a estrutura do projeto, responsabilidades de cada pasta e arquivo, e instruções para desenvolvimento e deploy.

## Próximos Passos

1. Mapear todas as rotas e funções do `main_controller.py` para os domínios acima.
2. Criar os novos arquivos controladores e mover o código para eles.
3. Atualizar o arquivo `__init__.py` para registrar os novos blueprints.
4. Testar cada parte para garantir que nada foi quebrado.
5. Documentar a nova estrutura no README.md.

---

Este plano visa organizar o projeto de forma profissional, facilitando a colaboração e manutenção futura.

Por favor, confirme se deseja que eu siga com este plano para a refatoração.
