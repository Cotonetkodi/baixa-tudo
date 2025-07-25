# Documento de Arquitetura Técnica: Sistema de Partilha de Ficheiros

**Autor:** Manus AI

**Data:** 23 de julho de 2025

## 1. Introdução

Este documento detalha a arquitetura técnica proposta para o sistema de partilha de ficheiros, que permitirá aos utilizadores carregar ficheiros de até 5GB, categorizá-los, partilhá-los e fazer o download direto. O sistema incluirá um painel de administração para gestão de contas de armazenamento MEGA e monitorização do espaço disponível. O desenvolvimento será focado em tecnologias web modernas, com um backend em Python (Flask) e um frontend interativo, com deployment planeado para Render e gestão de código via GitHub.

## 2. Requisitos Funcionais

Os requisitos funcionais do sistema incluem:

*   **Upload de Ficheiros:**
    *   Suporte para ficheiros até 5GB.
    *   Funcionalidade de arrastar e largar (drag & drop) para múltiplos ficheiros.
    *   Seleção de categorias para cada ficheiro (vídeos, música, jogos, aplicações, livros, outros).
    *   Barra de progresso de upload em tempo real.
    *   Confirmação de upload concluído.
*   **Partilha e Download:**
    *   Geração de links diretos para partilha e download.
*   **Pesquisa de Ficheiros:**
    *   Funcionalidade de pesquisa por nome e categoria.
*   **Painel de Administração:**
    *   Login obrigatório com utilizador e palavra-passe.
    *   Adição e gestão de múltiplas contas MEGA para armazenamento.
    *   Monitorização do espaço de armazenamento das contas MEGA, com alertas para contas a ficarem cheias.

## 3. Arquitetura do Sistema

A arquitetura do sistema será dividida em três componentes principais:

1.  **Frontend (Cliente):** A interface de utilizador, acessível via navegador web.
2.  **Backend (Servidor):** A lógica de negócio, API e gestão de armazenamento.
3.  **Armazenamento:** O serviço de cloud MEGA para guardar os ficheiros.

```mermaid
graph TD
    A[Utilizador] -->|Acede via navegador| B(Frontend)
    B -->|Requisições API| C(Backend Flask)
    C -->|Upload/Download| D[MEGA Cloud Storage]
    C -->|Leitura/Escrita| E[Base de Dados SQLite]
    A -->|Acede via navegador| F(Painel de Administração)
    F -->|Requisições API (Autenticadas)| C
```

## 4. Tecnologias Escolhidas

*   **Frontend:** HTML, CSS, JavaScript (com React para componentes interativos e gestão de estado).
*   **Backend:** Python 3.x com o framework Flask.
*   **Armazenamento Cloud:** MEGA (utilizando uma biblioteca Python como `mega.py`).
*   **Base de Dados:** SQLite (para metadados dos ficheiros, informações de utilizador admin e detalhes das contas MEGA).
*   **Controlo de Versões:** Git e GitHub.
*   **Deployment:** Render (para hosting do backend e frontend).

## 5. Estrutura de Dados (SQLite)

Serão criadas as seguintes tabelas na base de dados SQLite:

### Tabela `users` (para administradores)

| Campo      | Tipo de Dados | Descrição                      |
| :--------- | :------------ | :----------------------------- |
| `id`       | INTEGER       | Chave primária, auto-incremento |
| `username` | TEXT          | Nome de utilizador único       |
| `password` | TEXT          | Hash da palavra-passe          |

### Tabela `mega_accounts`

| Campo        | Tipo de Dados | Descrição                                  |
| :----------- | :------------ | :----------------------------------------- |
| `id`         | INTEGER       | Chave primária, auto-incremento             |
| `email`      | TEXT          | Email da conta MEGA                        |
| `password`   | TEXT          | Palavra-passe da conta MEGA (encriptada)   |
| `total_space`| INTEGER       | Espaço total disponível (em bytes)         |
| `used_space` | INTEGER       | Espaço usado (em bytes)                    |
| `is_active`  | BOOLEAN       | Indica se a conta está ativa para uploads  |

### Tabela `files`

| Campo          | Tipo de Dados | Descrição                                  |
| :------------- | :------------ | :----------------------------------------- |\n| `id`           | INTEGER       | Chave primária, auto-incremento             |
| `filename`     | TEXT          | Nome original do ficheiro                  |
| `mega_filename`| TEXT          | Nome do ficheiro no MEGA (para evitar conflitos) |
| `size`         | INTEGER       | Tamanho do ficheiro (em bytes)             |
| `category`     | TEXT          | Categoria do ficheiro (vídeos, música, etc.) |
| `upload_date`  | DATETIME      | Data e hora do upload                      |
| `mega_account_id`| INTEGER     | ID da conta MEGA onde o ficheiro está armazenado |
| `mega_file_id` | TEXT          | ID do ficheiro no MEGA (para download/partilha) |
| `share_link`   | TEXT          | Link de partilha gerado pelo MEGA          |

## 6. Fluxo de Upload de Ficheiros

Para lidar com ficheiros grandes (até 5GB), o processo de upload será otimizado:

1.  **Seleção de Ficheiros:** O utilizador seleciona um ou mais ficheiros via drag & drop ou seleção manual.
2.  **Pré-processamento no Frontend:** O frontend lê o ficheiro em chunks e envia cada chunk para o backend.
3.  **Backend Recebe Chunks:** O backend Flask recebe os chunks. Em vez de armazenar o ficheiro completo em memória ou no disco local do servidor (o que pode ser problemático para ficheiros grandes e para o ambiente do Render), o backend irá imediatamente retransmitir esses chunks para a API do MEGA.
4.  **Upload para MEGA:** A biblioteca `mega.py` (ou similar) será utilizada para realizar o upload dos chunks para a conta MEGA selecionada. Será implementada uma lógica para escolher a conta MEGA com mais espaço disponível e gerir o balanceamento de carga entre as contas.
5.  **Barra de Progresso:** O frontend receberá atualizações de progresso do backend (via WebSockets ou polling) para atualizar a barra de carregamento.
6.  **Confirmação e Metadados:** Após o upload completo para o MEGA, o backend registará os metadados do ficheiro (nome, tamanho, categoria, ID da conta MEGA, ID do ficheiro MEGA, link de partilha) na base de dados SQLite e enviará uma confirmação ao frontend.

## 7. Gestão de Contas MEGA

O painel de administração permitirá ao utilizador adicionar múltiplas contas MEGA. O sistema irá:

*   **Autenticação:** Autenticar-se em cada conta MEGA fornecida.
*   **Monitorização de Espaço:** Periodicamente, ou a pedido, consultar o espaço total e usado de cada conta MEGA através da API. Esta informação será armazenada na base de dados.
*   **Seleção de Conta para Upload:** Antes de cada upload, o backend consultará a tabela `mega_accounts` para identificar a conta com mais espaço livre disponível. Se uma conta estiver a ficar cheia (e.g., >90% de uso), será marcada para alerta no painel de administração e, se possível, evitada para novos uploads até que mais espaço esteja disponível ou uma nova conta seja adicionada.

## 8. Segurança

*   **Autenticação do Administrador:** O painel de administração será protegido por um sistema de login com nome de utilizador e palavra-passe. As palavras-passe serão armazenadas como hashes (e.g., usando `werkzeug.security.generate_password_hash`).
*   **Segurança da API:** Todos os endpoints da API para o painel de administração serão protegidos por tokens de sessão ou JWTs.
*   **MEGA API Keys:** As credenciais das contas MEGA serão armazenadas encriptadas na base de dados ou como variáveis de ambiente seguras no Render.
*   **Validação de Uploads:** Embora o MEGA lide com a segurança do armazenamento, o backend validará os tipos de ficheiro e tamanhos para evitar abusos.

## 9. Deployment (Render)

O sistema será configurado para deployment no Render. Isto envolverá:

*   **Repositório GitHub:** O código será mantido num repositório GitHub.
*   **Configuração do Render:** O Render será configurado para construir e implementar automaticamente o backend Flask e o frontend (se for uma SPA separada ou servida pelo Flask) a partir do repositório GitHub.
*   **Variáveis de Ambiente:** Credenciais sensíveis (e.g., chaves secretas, credenciais de admin) serão armazenadas como variáveis de ambiente seguras no Render.

## 10. Próximos Passos

Com base nesta arquitetura, os próximos passos incluem:

*   Configuração do ambiente de desenvolvimento.
*   Criação da estrutura básica do projeto Flask.
*   Implementação do modelo de base de dados.
*   Desenvolvimento do frontend e backend em paralelo.
*   Testes e otimização contínuos.




## 6.1. Detalhes da Integração com MEGA API

A integração com o MEGA será feita através da biblioteca `mega.py` [1], que oferece funcionalidades para login, upload, download, eliminação, pesquisa, partilha e renomeação/movimentação de ficheiros. Dada a limitação de 5GB por ficheiro, é crucial que o upload seja feito de forma eficiente, preferencialmente via streaming ou chunking, para evitar problemas de memória no servidor.

### 6.1.1. Autenticação e Gestão de Sessões

Cada conta MEGA adicionada pelo administrador será autenticada. A `mega.py` permite autenticação via email e palavra-passe. As sessões autenticadas serão geridas pelo backend, possivelmente armazenando tokens de sessão de forma segura para evitar re-autenticações constantes.

### 6.1.2. Upload de Ficheiros Grandes (Chunking/Streaming)

Para ficheiros de até 5GB, o método de upload deve ser robusto. A `mega.py` suporta uploads de ficheiros, e é importante verificar se a biblioteca lida internamente com o chunking para uploads eficientes. Caso contrário, será necessário implementar uma lógica de chunking no backend, onde o ficheiro é lido em partes e cada parte é enviada sequencialmente para o MEGA. Isso minimiza o uso de memória do servidor e permite uma barra de progresso mais precisa.

### 6.1.3. Obtenção de Links de Partilha

Após o upload bem-sucedido de um ficheiro para o MEGA, a API deve fornecer um link de partilha direto. Este link será armazenado na base de dados `files` e será usado para permitir o download direto pelos utilizadores.

### 6.1.4. Monitorização de Espaço

A `mega.py` permite obter informações sobre o espaço total e usado de uma conta MEGA. Esta funcionalidade será utilizada para popular os campos `total_space` e `used_space` na tabela `mega_accounts`. A monitorização será feita periodicamente ou a pedido do administrador, e alertas serão gerados quando o espaço de uma conta estiver a esgotar-se.

## Referências

[1] 3v1n0/mega.py: Simple mega python APIs. GitHub. Disponível em: [https://github.com/3v1n0/mega.py](https://github.com/3v1n0/mega.py)




## 5.1. Detalhes da Estrutura de Dados e Base de Dados

A escolha do SQLite como base de dados é justificada pela sua simplicidade e facilidade de integração com aplicações Flask, sendo ideal para gerir metadados e configurações. Para um ambiente de produção no Render, o SQLite é adequado para dados que não exigem alta concorrência ou escalabilidade distribuída, como os metadados de ficheiros e as configurações de contas MEGA.

### 5.1.1. Tabela `users`

Esta tabela armazenará as credenciais de login para o painel de administração. A palavra-passe será armazenada como um hash seguro para proteção contra acessos não autorizados. A gestão de utilizadores será mínima, focada apenas no administrador principal.

### 5.1.2. Tabela `mega_accounts`

Esta tabela é crucial para a gestão do armazenamento. Cada registo representará uma conta MEGA que o administrador adicionou. Os campos `total_space` e `used_space` serão atualizados regularmente para refletir o estado atual do armazenamento. O campo `is_active` permitirá ao administrador desativar temporariamente uma conta se necessário, por exemplo, se estiver a atingir o limite de espaço ou se houver problemas de autenticação.

### 5.1.3. Tabela `files`

Esta tabela armazenará todos os metadados dos ficheiros carregados. É importante notar que os ficheiros em si não serão armazenados na base de dados, apenas as suas informações. O `mega_filename` é um campo importante para garantir que os nomes dos ficheiros no MEGA sejam únicos e não causem conflitos. O `mega_file_id` e o `share_link` são essenciais para a funcionalidade de download e partilha direta.

## 5.2. Considerações sobre a Base de Dados

*   **Migrações:** Para futuras atualizações do esquema da base de dados, será considerada a utilização de uma ferramenta de migração como o Flask-Migrate (baseado no Alembic).
*   **Backup:** Embora o SQLite seja um ficheiro único, é importante considerar uma estratégia de backup para o ficheiro da base de dados, especialmente antes de grandes atualizações ou para recuperação de desastres.
*   **Performance:** Para o volume de dados esperado (metadados de ficheiros), o SQLite deve oferecer performance adequada. Se o número de ficheiros e contas MEGA crescer exponencialmente, uma base de dados mais robusta (como PostgreSQL) poderá ser considerada no futuro, mas para a fase inicial, o SQLite é suficiente.




## 6.2. Funcionalidades Detalhadas e Requisitos de Segurança

### 6.2.1. Funcionalidades Detalhadas

*   **Upload de Ficheiros:**
    *   **Seleção:** Interface intuitiva para seleção de ficheiros, com suporte a múltiplos ficheiros e drag-and-drop. O frontend deve pré-validar o tamanho do ficheiro para evitar uploads desnecessários de ficheiros maiores que 5GB.
    *   **Categorização:** Um dropdown ou botões de rádio para o utilizador selecionar a categoria do ficheiro antes do upload. As categorias serão predefinidas (vídeos, música, jogos, aplicações, livros, outros).
    *   **Barra de Progresso:** Utilização de WebSockets (via Flask-SocketIO) ou polling para comunicar o progresso do upload do backend para o frontend em tempo real. Isso proporcionará uma experiência de utilizador fluida.
    *   **Confirmação:** Após o upload bem-sucedido, uma mensagem de confirmação será exibida ao utilizador, possivelmente com o link de partilha do ficheiro.

*   **Partilha e Download:**
    *   **Links Diretos:** Os links de partilha gerados pelo MEGA serão apresentados ao utilizador após o upload e estarão disponíveis na página de pesquisa. Estes links permitirão o download direto sem a necessidade de autenticação no site.

*   **Pesquisa de Ficheiros:**
    *   **Interface de Pesquisa:** Um campo de texto para pesquisa por nome de ficheiro e um filtro por categoria. A pesquisa será realizada na base de dados SQLite.
    *   **Resultados:** Os resultados da pesquisa serão exibidos de forma paginada, mostrando o nome do ficheiro, categoria, tamanho, data de upload e o link de partilha.

*   **Painel de Administração:**
    *   **Autenticação:** Implementação de um sistema de login seguro com nome de utilizador e palavra-passe (hash).
    *   **Gestão de Contas MEGA:** Interface para adicionar, editar e remover contas MEGA. Ao adicionar uma conta, o sistema tentará autenticar-se e obter as informações de espaço.
    *   **Monitorização de Espaço:** Exibição clara do espaço total e usado para cada conta MEGA. Alertas visuais (e.g., cor vermelha) para contas que estão a ficar cheias (e.g., >90% de uso). Possibilidade de forçar uma atualização do espaço de uma conta.
    *   **Gestão de Ficheiros (Opcional, Fase Futura):** Numa fase futura, pode ser considerada a funcionalidade de listar e gerir (eliminar) ficheiros diretamente do painel de administração, embora a gestão primária seja via MEGA.

### 6.2.2. Requisitos de Segurança Detalhados

*   **Proteção contra Ataques Comuns:**
    *   **CSRF (Cross-Site Request Forgery):** Utilização de tokens CSRF no Flask para proteger formulários e requisições POST.
    *   **XSS (Cross-Site Scripting):** Sanitização de todas as entradas de utilizador antes de serem exibidas na interface.
    *   **SQL Injection:** Utilização de ORM (Object-Relational Mapping) como SQLAlchemy com Flask-SQLAlchemy para interagir com a base de dados, prevenindo injeções SQL.
*   **Armazenamento Seguro de Credenciais:**
    *   **Palavras-passe de Administrador:** Armazenadas como hashes seguros (e.g., SHA256 com salt) usando `werkzeug.security.generate_password_hash` e `check_password_hash`.
    *   **Credenciais MEGA:** As palavras-passe das contas MEGA serão armazenadas encriptadas na base de dados. Uma chave de encriptação será armazenada como variável de ambiente segura no Render.
*   **Controlo de Acesso:**
    *   **Autenticação:** Todas as rotas do painel de administração e endpoints de API sensíveis serão protegidos por autenticação baseada em sessão ou JWTs. Apenas utilizadores autenticados e autorizados terão acesso.
    *   **Autorização:** Embora o sistema comece com um único administrador, a arquitetura deve permitir a expansão para múltiplos níveis de utilizadores, se necessário.
*   **Validação de Dados:**
    *   **Uploads:** Validação rigorosa do lado do servidor para tipos de ficheiro (MIME types) e tamanhos para evitar o upload de ficheiros maliciosos ou excessivamente grandes.
*   **Logging e Monitorização:**
    *   Implementação de logging para registar eventos importantes do sistema, como tentativas de login falhadas, uploads bem-sucedidos/falhados, e erros da API MEGA. Isso ajudará na auditoria e na identificação de potenciais problemas de segurança.


