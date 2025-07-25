# Sistema de Partilha de Ficheiros - Documentação Completa

**Autor:** Manus AI  
**Data:** 23 de Julho de 2025  
**Versão:** 1.0  

## Índice

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Arquitetura Técnica](#arquitetura-técnica)
3. [Guia de Instalação](#guia-de-instalação)
4. [Manual de Utilizador](#manual-de-utilizador)
5. [Guia de Administração](#guia-de-administração)
6. [Deployment no Render](#deployment-no-render)
7. [Integração MEGA](#integração-mega)
8. [Resolução de Problemas](#resolução-de-problemas)
9. [Desenvolvimento Futuro](#desenvolvimento-futuro)

---

## Visão Geral do Projeto

O Sistema de Partilha de Ficheiros é uma aplicação web completa desenvolvida para permitir o upload, armazenamento e partilha de ficheiros até 5GB utilizando a infraestrutura do MEGA como backend de armazenamento. O sistema foi concebido com uma arquitetura moderna, interface intuitiva e funcionalidades avançadas de gestão.

### Objetivos Principais

O projeto foi desenvolvido com os seguintes objetivos fundamentais:

**Facilidade de Uso**: Criar uma interface intuitiva que permita aos utilizadores fazer upload de múltiplos ficheiros através de drag & drop, com feedback visual em tempo real através de barras de progresso e notificações interativas.

**Escalabilidade**: Implementar um sistema de gestão de múltiplas contas MEGA que permite balanceamento automático de carga e expansão horizontal do armazenamento disponível.

**Segurança**: Garantir que todas as credenciais são encriptadas, as sessões são seguras e existe controlo de acesso adequado ao painel de administração.

**Organização**: Proporcionar um sistema de categorização automática e pesquisa avançada que facilita a localização e gestão de ficheiros.

### Funcionalidades Principais

O sistema oferece um conjunto abrangente de funcionalidades divididas em três áreas principais:

**Área Pública**: Interface principal onde os utilizadores podem fazer upload de ficheiros, pesquisar conteúdo existente e aceder a links de partilha. A interface suporta upload simultâneo de múltiplos ficheiros com validação automática de tamanho e tipo.

**Área de Administração**: Painel completo para gestão do sistema, incluindo adição e remoção de contas MEGA, monitorização de espaço de armazenamento, visualização de estatísticas e gestão de ficheiros.

**API Backend**: Conjunto robusto de endpoints RESTful que suportam todas as operações do sistema, incluindo upload, pesquisa, eliminação e gestão de contas MEGA.




## Arquitetura Técnica

### Stack Tecnológico

O sistema foi desenvolvido utilizando uma stack moderna e robusta que garante performance, escalabilidade e facilidade de manutenção:

**Backend Framework**: Flask foi escolhido como framework principal devido à sua flexibilidade e facilidade de integração com outras tecnologias. O Flask fornece uma base sólida para APIs RESTful e permite extensibilidade através de blueprints modulares.

**Base de Dados**: SQLAlchemy como ORM (Object-Relational Mapping) com SQLite para desenvolvimento e testes. A arquitetura permite migração fácil para PostgreSQL ou MySQL em ambiente de produção sem alterações significativas no código.

**Frontend**: Interface desenvolvida em HTML5, CSS3 e JavaScript vanilla, garantindo compatibilidade universal e performance otimizada. A escolha por JavaScript vanilla elimina dependências externas e reduz o tamanho da aplicação.

**Comunicação em Tempo Real**: Flask-SocketIO implementa WebSockets para feedback em tempo real durante uploads, proporcionando uma experiência de utilizador superior com atualizações instantâneas de progresso.

**Armazenamento**: Integração com MEGA API através da biblioteca mega.py, permitindo armazenamento distribuído e escalável. O sistema suporta múltiplas contas MEGA com balanceamento automático de carga.

### Arquitetura de Componentes

O sistema segue uma arquitetura modular bem definida que separa responsabilidades e facilita manutenção:

**Camada de Apresentação**: Composta pelos ficheiros estáticos (HTML, CSS, JavaScript) que implementam a interface de utilizador. Esta camada é responsável pela interação com o utilizador, validação de formulários no lado cliente e comunicação com a API backend.

**Camada de Aplicação**: Implementada através de blueprints Flask que organizam as rotas em módulos funcionais. Inclui o blueprint de ficheiros para operações de upload e pesquisa, e o blueprint de administração para gestão do sistema.

**Camada de Serviços**: Contém a lógica de negócio principal, incluindo o serviço MEGA para gestão de armazenamento, serviços de encriptação para segurança de credenciais e utilitários diversos.

**Camada de Dados**: Modelos SQLAlchemy que definem a estrutura da base de dados e implementam as relações entre entidades. Inclui modelos para ficheiros, contas MEGA e administradores.

### Modelo de Dados

A base de dados foi concebida para suportar todas as funcionalidades do sistema de forma eficiente:

**Tabela Files**: Armazena metadados de todos os ficheiros carregados, incluindo nome original, nome no MEGA, tamanho, categoria, data de upload e referências para a conta MEGA utilizada.

**Tabela MegaAccounts**: Gere informações das contas MEGA configuradas, incluindo credenciais encriptadas, espaço total e utilizado, estado ativo/inativo e data da última atualização.

**Tabela Admins**: Controla acesso ao painel de administração com credenciais encriptadas e gestão de sessões seguras.

### Segurança

O sistema implementa múltiplas camadas de segurança para proteger dados e credenciais:

**Encriptação de Credenciais**: Todas as palavras-passe são encriptadas utilizando bcrypt com salt aleatório. As credenciais MEGA são encriptadas com Fernet (criptografia simétrica) antes de serem armazenadas na base de dados.

**Gestão de Sessões**: Implementação de sessões seguras com tokens únicos e expiração automática. O sistema valida permissões em cada pedido ao painel de administração.

**Validação de Entrada**: Validação rigorosa de todos os inputs, incluindo verificação de tipos de ficheiro, tamanhos máximos e sanitização de dados de formulários.

**CORS Configurado**: Cross-Origin Resource Sharing configurado adequadamente para permitir comunicação segura entre frontend e backend.


## Guia de Instalação

### Requisitos do Sistema

Antes de proceder com a instalação, certifique-se de que o sistema cumpre os seguintes requisitos:

**Sistema Operativo**: O sistema é compatível com Linux, macOS e Windows. Para integração real com MEGA, recomenda-se Linux ou macOS devido a melhor compatibilidade das dependências.

**Python**: Versão 3.8 ou 3.9 para integração real com MEGA. A versão atual (3.11) funciona com simulação MEGA para demonstração. Python 3.7 ou inferior não é suportado devido a dependências modernas.

**Memória**: Mínimo 512MB RAM disponível. Para uploads de ficheiros grandes (próximos de 5GB), recomenda-se 2GB RAM ou superior.

**Espaço em Disco**: Mínimo 1GB para a aplicação e dependências. Espaço adicional pode ser necessário para ficheiros temporários durante uploads.

**Conectividade**: Acesso à internet é obrigatório para comunicação com a API do MEGA e download de dependências.

### Instalação Local Detalhada

**Passo 1: Preparação do Ambiente**

Comece por criar um diretório dedicado para o projeto e navegar até ele:

```bash
mkdir file-sharing-system
cd file-sharing-system
```

Clone o repositório do projeto (substitua pela URL real do seu repositório):

```bash
git clone <url-do-repositorio> .
```

**Passo 2: Ambiente Virtual Python**

Crie um ambiente virtual isolado para evitar conflitos com outras instalações Python:

```bash
python -m venv venv
```

Ative o ambiente virtual:

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Verifique se o ambiente virtual está ativo (deve aparecer "(venv)" no prompt do terminal).

**Passo 3: Instalação de Dependências**

Atualize o pip para a versão mais recente:

```bash
pip install --upgrade pip
```

Instale todas as dependências do projeto:

```bash
pip install -r requirements.txt
```

Este comando instalará automaticamente todas as bibliotecas necessárias, incluindo Flask, SQLAlchemy, Flask-SocketIO, cryptography e outras dependências.

**Passo 4: Configuração de Ambiente**

Copie o ficheiro de exemplo de variáveis de ambiente:

```bash
cp .env.example .env
```

Edite o ficheiro `.env` com as suas configurações:

```bash
# Configurações da aplicação
SECRET_KEY=sua-chave-secreta-muito-longa-e-aleatoria
DATABASE_URL=sqlite:///app.db
FLASK_ENV=development

# Chave de encriptação para credenciais MEGA
ENCRYPTION_KEY=sua-chave-de-encriptacao-aleatoria

# Configurações opcionais
MAX_CONTENT_LENGTH=5368709120
DEBUG=True
```

**Importante**: Gere chaves aleatórias seguras para SECRET_KEY e ENCRYPTION_KEY. Nunca utilize as chaves de exemplo em produção.

**Passo 5: Inicialização da Base de Dados**

Execute a aplicação pela primeira vez para criar a base de dados e o administrador padrão:

```bash
python src/main.py
```

O sistema criará automaticamente:
- Base de dados SQLite (`app.db`)
- Tabelas necessárias
- Administrador padrão (utilizador: `admin`, palavra-passe: `admin123`)

**Passo 6: Verificação da Instalação**

Abra o navegador e aceda a:
- Site principal: `http://localhost:5000`
- Painel de administração: `http://localhost:5000/admin`

Se tudo estiver configurado corretamente, deverá ver a interface principal do sistema.

### Configuração para Desenvolvimento

Para desenvolvimento ativo, recomenda-se as seguintes configurações adicionais:

**Debug Mode**: Mantenha `DEBUG=True` no ficheiro `.env` para recarregamento automático e mensagens de erro detalhadas.

**Logs Detalhados**: Configure logging adicional editando o ficheiro `src/main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Base de Dados de Desenvolvimento**: Para testes, pode eliminar o ficheiro `app.db` a qualquer momento. Será recriado automaticamente na próxima execução.

### Resolução de Problemas de Instalação

**Erro de Dependências**: Se encontrar erros durante `pip install`, tente:

```bash
pip install --upgrade setuptools wheel
pip install -r requirements.txt --no-cache-dir
```

**Problemas com mega.py**: Para integração real com MEGA, pode ser necessário downgrade do Python:

```bash
# Instalar Python 3.9 usando pyenv (Linux/macOS)
pyenv install 3.9.16
pyenv local 3.9.16
```

**Permissões de Ficheiros**: Em sistemas Unix, certifique-se de que tem permissões adequadas:

```bash
chmod +x src/main.py
```

**Firewall/Antivírus**: Alguns antivírus podem bloquear a execução. Adicione exceção para o diretório do projeto.


## Manual de Utilizador

### Interface Principal

A interface principal do sistema foi concebida para ser intuitiva e acessível a utilizadores de todos os níveis técnicos. Ao aceder ao site, encontrará uma interface limpa e moderna com navegação clara entre as diferentes secções.

**Navegação Superior**: A barra de navegação contém três botões principais: "Upload" para carregar ficheiros, "Pesquisar" para encontrar conteúdo existente, e "Admin" para acesso ao painel de administração.

**Área de Upload**: A secção principal apresenta uma zona de drag & drop claramente identificada com instruções visuais. Esta área aceita ficheiros arrastados diretamente do explorador de ficheiros ou permite seleção através do botão "Selecionar Ficheiros".

**Feedback Visual**: O sistema fornece feedback constante através de animações suaves, mudanças de cor e ícones informativos que guiam o utilizador através de cada ação.

### Upload de Ficheiros

O processo de upload foi otimizado para ser rápido e intuitivo, suportando múltiplos ficheiros simultaneamente:

**Seleção de Ficheiros**: Existem duas formas de selecionar ficheiros para upload. A primeira é arrastar ficheiros diretamente da pasta do computador para a área designada na interface. A segunda é clicar no botão "Selecionar Ficheiros" e escolher através do diálogo padrão do sistema operativo.

**Validação Automática**: O sistema valida automaticamente cada ficheiro selecionado, verificando se o tamanho não excede o limite de 5GB. Ficheiros que excedam este limite são rejeitados com uma mensagem explicativa clara.

**Categorização**: Durante o processo de upload, é obrigatório selecionar uma categoria para cada ficheiro. As categorias disponíveis são: Vídeos, Música, Jogos, Aplicações, Livros e Outros. Esta categorização facilita a organização e pesquisa posterior.

**Progresso em Tempo Real**: Uma barra de progresso mostra o estado do upload em tempo real, incluindo percentagem concluída e velocidade de transferência. Para uploads múltiplos, cada ficheiro tem a sua própria barra de progresso.

**Confirmação de Conclusão**: Após conclusão bem-sucedida, o sistema apresenta uma notificação com o link de partilha do ficheiro. Este link pode ser copiado e partilhado com outros utilizadores para download direto.

### Sistema de Pesquisa

A funcionalidade de pesquisa permite localizar rapidamente ficheiros através de múltiplos critérios:

**Pesquisa por Nome**: A caixa de pesquisa principal aceita termos de busca que são comparados com os nomes dos ficheiros. A pesquisa é case-insensitive e suporta pesquisa parcial.

**Filtros por Categoria**: Um menu dropdown permite filtrar resultados por categoria específica ou visualizar todas as categorias simultaneamente. Este filtro pode ser combinado com pesquisa textual para resultados mais precisos.

**Resultados Organizados**: Os resultados são apresentados numa grelha organizada, mostrando nome do ficheiro, categoria, tamanho e data de upload. Cada resultado inclui botões para download direto e partilha.

**Paginação**: Para grandes volumes de ficheiros, o sistema implementa paginação automática para manter a performance da interface.

### Partilha e Download

O sistema facilita a partilha de ficheiros através de links diretos:

**Links de Partilha**: Cada ficheiro carregado gera automaticamente um link único de partilha que pode ser distribuído a outros utilizadores. Estes links permitem download direto sem necessidade de registo ou login.

**Download Direto**: Os links de partilha redirecionam diretamente para o MEGA, garantindo velocidades de download otimizadas e disponibilidade global.

**Gestão de Links**: No painel de administração, é possível visualizar e gerir todos os links de partilha ativos, incluindo estatísticas de acesso quando disponíveis.

### Experiência Mobile

A interface foi desenvolvida com design responsivo que se adapta automaticamente a dispositivos móveis:

**Layout Adaptativo**: Em dispositivos móveis, a interface reorganiza-se automaticamente para otimizar o espaço disponível. Botões tornam-se maiores para facilitar interação táctil.

**Upload Mobile**: O sistema suporta upload de ficheiros em dispositivos móveis, incluindo acesso à galeria de fotos, câmara e outros aplicativos de ficheiros.

**Navegação Táctil**: Todos os elementos da interface são otimizados para interação táctil, com áreas de toque adequadas e feedback visual apropriado.

### Acessibilidade

O sistema implementa práticas de acessibilidade para garantir usabilidade universal:

**Navegação por Teclado**: Toda a interface pode ser navegada utilizando apenas o teclado, com ordem de tabulação lógica e indicadores visuais claros.

**Contraste de Cores**: As cores foram escolhidas para garantir contraste adequado e legibilidade em diferentes condições de iluminação.

**Texto Alternativo**: Todas as imagens e ícones incluem texto alternativo para compatibilidade com leitores de ecrã.

**Mensagens Claras**: Todas as mensagens de erro e confirmação são escritas em linguagem clara e não técnica.


## Guia de Administração

### Acesso ao Painel de Administração

O painel de administração é a interface central para gestão do sistema, acessível apenas a utilizadores autorizados com credenciais válidas.

**Login Seguro**: Para aceder ao painel, navegue até `/admin` e introduza as credenciais de administrador. Por defeito, o sistema cria um utilizador `admin` com palavra-passe `admin123`. É fortemente recomendado alterar estas credenciais após a primeira utilização.

**Gestão de Sessões**: O sistema mantém sessões seguras com expiração automática. Após períodos de inatividade, será necessário fazer login novamente. A sessão é automaticamente invalidada quando o navegador é fechado.

**Segurança de Acesso**: Todas as páginas de administração verificam automaticamente as permissões. Tentativas de acesso não autorizado são registadas e bloqueadas.

### Gestão de Contas MEGA

A funcionalidade mais crítica do painel de administração é a gestão das contas MEGA que servem como backend de armazenamento:

**Adição de Contas**: Para adicionar uma nova conta MEGA, clique no botão "Adicionar Conta MEGA" e introduza o email e palavra-passe da conta. O sistema testa automaticamente a conectividade antes de guardar as credenciais.

**Validação de Credenciais**: Durante a adição, o sistema conecta-se à API do MEGA para verificar se as credenciais são válidas e obtém informações sobre o espaço disponível. Credenciais inválidas são rejeitadas com mensagem de erro explicativa.

**Encriptação de Dados**: Todas as credenciais MEGA são encriptadas antes de serem armazenadas na base de dados. A chave de encriptação é definida nas variáveis de ambiente e nunca é armazenada em texto simples.

**Monitorização de Espaço**: O painel apresenta informações detalhadas sobre cada conta MEGA, incluindo espaço total, espaço utilizado e percentagem de ocupação. Contas que se aproximam da capacidade máxima são destacadas visualmente.

**Atualização de Informações**: O botão "Atualizar" junto a cada conta permite sincronizar as informações de espaço com os servidores MEGA. Esta operação deve ser realizada regularmente para manter dados precisos.

**Remoção de Contas**: Contas MEGA podem ser removidas do sistema através do botão "Remover". Esta ação não afeta ficheiros já armazenados, mas impede novos uploads para essa conta.

### Balanceamento de Armazenamento

O sistema implementa balanceamento automático inteligente para otimizar a utilização das contas MEGA disponíveis:

**Seleção Automática**: Quando um utilizador faz upload de um ficheiro, o sistema seleciona automaticamente a conta MEGA com mais espaço disponível que possa acomodar o ficheiro.

**Distribuição de Carga**: O algoritmo de balanceamento considera não apenas o espaço disponível, mas também a distribuição equilibrada de ficheiros entre contas para evitar sobrecarga.

**Gestão de Falhas**: Se uma conta MEGA não estiver disponível durante um upload, o sistema tenta automaticamente outras contas disponíveis sem intervenção manual.

**Alertas de Capacidade**: O painel de administração destaca contas que atingem 80% ou mais da capacidade, permitindo ação proativa antes de ficarem completamente cheias.

### Monitorização do Sistema

O painel fornece ferramentas abrangentes para monitorizar a saúde e performance do sistema:

**Estatísticas Gerais**: A secção de estatísticas mostra métricas importantes como número total de ficheiros, espaço total utilizado, uploads recentes e distribuição por categoria.

**Logs de Atividade**: O sistema regista todas as ações importantes, incluindo uploads, eliminações, adições de contas MEGA e acessos ao painel de administração.

**Performance de Upload**: Métricas sobre velocidade média de upload, taxa de sucesso e tipos de erro mais comuns ajudam a identificar problemas de performance.

**Utilização por Categoria**: Gráficos mostram a distribuição de ficheiros por categoria, ajudando a compreender padrões de utilização.

### Gestão de Ficheiros

O painel permite gestão centralizada de todos os ficheiros no sistema:

**Visualização Completa**: Lista todos os ficheiros carregados com informações detalhadas incluindo nome, categoria, tamanho, data de upload e conta MEGA utilizada.

**Pesquisa Avançada**: Ferramentas de pesquisa permitem filtrar ficheiros por múltiplos critérios simultaneamente, incluindo data, categoria, tamanho e conta MEGA.

**Eliminação em Massa**: Funcionalidade para eliminar múltiplos ficheiros simultaneamente, útil para limpeza de conteúdo obsoleto ou gestão de espaço.

**Verificação de Integridade**: Ferramentas para verificar se ficheiros ainda existem nas contas MEGA correspondentes e identificar links quebrados.

### Configurações do Sistema

O painel permite ajustar várias configurações operacionais:

**Limites de Upload**: Configuração do tamanho máximo permitido para uploads, atualmente definido em 5GB mas ajustável conforme necessário.

**Categorias**: Gestão das categorias disponíveis para classificação de ficheiros, incluindo adição, remoção e renomeação de categorias.

**Políticas de Retenção**: Configuração de políticas automáticas para eliminação de ficheiros antigos ou não acedidos.

**Notificações**: Configuração de alertas automáticos para eventos importantes como contas MEGA cheias ou falhas de sistema.

### Backup e Manutenção

Procedimentos essenciais para manter a integridade e disponibilidade do sistema:

**Backup da Base de Dados**: Recomenda-se backup regular do ficheiro de base de dados SQLite. Em produção, considere backup automático para armazenamento externo.

**Sincronização MEGA**: Verificação periódica da sincronização entre a base de dados local e o estado real das contas MEGA.

**Limpeza de Ficheiros Temporários**: Remoção regular de ficheiros temporários criados durante uploads para libertar espaço em disco.

**Atualizações de Segurança**: Monitorização e aplicação de atualizações de segurança para todas as dependências do sistema.

### Resolução de Problemas Administrativos

Guia para resolver problemas comuns encontrados durante a administração:

**Contas MEGA Inacessíveis**: Se uma conta MEGA não responder, verifique as credenciais, conectividade de rede e estado da conta no site oficial do MEGA.

**Uploads Falhados**: Analise logs de erro para identificar causas, que podem incluir problemas de rede, contas cheias ou ficheiros corrompidos.

**Performance Lenta**: Monitorize utilização de recursos do servidor e considere otimizações como cache ou upgrade de hardware.

**Problemas de Sincronização**: Execute verificações manuais de integridade e sincronize informações de espaço com as contas MEGA.


## Deployment no Render

### Preparação para Deployment

O deployment no Render foi simplificado através de ficheiros de configuração pré-preparados que automatizam todo o processo de implementação.

**Verificação de Ficheiros**: Antes do deployment, confirme que os seguintes ficheiros estão presentes no repositório:
- `Procfile`: Define o comando de inicialização da aplicação
- `render.yaml`: Configuração automática para o Render
- `requirements.txt`: Lista todas as dependências Python necessárias
- `.gitignore`: Especifica ficheiros a excluir do controlo de versão

**Preparação do Repositório**: Certifique-se de que todo o código está commitado no Git e enviado para um repositório público no GitHub, GitLab ou Bitbucket. O Render necessita de acesso ao repositório para fazer deploy automático.

**Configuração de Variáveis**: Prepare as variáveis de ambiente necessárias que serão configuradas no painel do Render. Estas incluem chaves secretas, configurações de base de dados e outras configurações sensíveis.

### Deployment Automático

O método mais simples utiliza o ficheiro `render.yaml` incluído no projeto:

**Conexão do Repositório**: No painel do Render, selecione "New" e escolha "Blueprint". Cole a URL do seu repositório GitHub e o Render detectará automaticamente o ficheiro `render.yaml`.

**Configuração Automática**: O ficheiro `render.yaml` configura automaticamente:
- Tipo de serviço (Web Service)
- Ambiente Python
- Comandos de build e inicialização
- Variáveis de ambiente básicas
- Plano gratuito

**Processo de Build**: O Render executará automaticamente:
1. Clone do repositório
2. Instalação das dependências via `pip install -r requirements.txt`
3. Configuração do ambiente Python
4. Inicialização da aplicação via Gunicorn

**Monitorização**: Durante o deployment, pode acompanhar o progresso através dos logs em tempo real no painel do Render.

### Deployment Manual

Para maior controlo sobre o processo, pode configurar manualmente:

**Criação do Serviço**: No painel do Render, selecione "New" → "Web Service" e conecte o seu repositório.

**Configurações de Build**:
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT src.main:app`

**Configurações Avançadas**:
- **Auto-Deploy**: Ative para deployment automático em cada push
- **Health Check Path**: Configure para `/` para verificação de saúde
- **Instance Type**: Selecione conforme necessidades de performance

### Configuração de Variáveis de Ambiente

As variáveis de ambiente são cruciais para o funcionamento correto em produção:

**Variáveis Obrigatórias**:
```
SECRET_KEY=<chave-aleatoria-muito-longa>
DATABASE_URL=sqlite:///app.db
FLASK_ENV=production
ENCRYPTION_KEY=<chave-encriptacao-aleatoria>
```

**Geração de Chaves Seguras**: Utilize ferramentas online ou comandos Python para gerar chaves aleatórias:
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Configuração no Render**: No painel do serviço, vá a "Environment" e adicione cada variável individualmente. O Render oferece opção para gerar valores aleatórios automaticamente.

**Variáveis Opcionais**:
```
MAX_CONTENT_LENGTH=5368709120
DEBUG=False
PORT=10000
```

### Configuração de Base de Dados

Para produção, considere as seguintes opções de base de dados:

**SQLite (Padrão)**: Adequado para aplicações pequenas a médias. O ficheiro de base de dados é armazenado no sistema de ficheiros do Render, mas pode ser perdido durante redeploys.

**PostgreSQL (Recomendado)**: Para produção robusta, configure uma base de dados PostgreSQL:
1. Crie um serviço PostgreSQL no Render
2. Obtenha a URL de conexão
3. Atualize `DATABASE_URL` para apontar para PostgreSQL
4. Instale `psycopg2-binary` nas dependências

**Migração de Dados**: Para migrar de SQLite para PostgreSQL:
```bash
# Exportar dados SQLite
sqlite3 app.db .dump > backup.sql

# Importar para PostgreSQL (ajustar sintaxe conforme necessário)
psql $DATABASE_URL < backup.sql
```

### Otimizações de Performance

Para melhor performance em produção:

**Configuração Gunicorn**: O `Procfile` pode ser otimizado:
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 src.main:app
```

**Workers**: Número de workers baseado nos recursos disponíveis. Para o plano gratuito do Render, 2-4 workers são adequados.

**Timeout**: Aumente o timeout para uploads de ficheiros grandes.

**Configurações Flask**: Em produção, certifique-se de que:
- `DEBUG=False`
- `FLASK_ENV=production`
- Logs configurados adequadamente

### Monitorização e Logs

O Render fornece ferramentas abrangentes para monitorização:

**Logs em Tempo Real**: Acesse logs da aplicação diretamente no painel do Render para debugging e monitorização.

**Métricas de Performance**: Visualize CPU, memória e tráfego de rede através do dashboard integrado.

**Alertas**: Configure alertas para eventos importantes como falhas de deployment ou utilização excessiva de recursos.

**Health Checks**: O Render verifica automaticamente a saúde da aplicação através de pedidos HTTP regulares.

### Domínio Personalizado

Para utilizar um domínio próprio:

**Configuração DNS**: Configure registos CNAME no seu provedor DNS apontando para o domínio fornecido pelo Render.

**SSL/TLS**: O Render fornece certificados SSL gratuitos via Let's Encrypt, configurados automaticamente.

**Redirecionamentos**: Configure redirecionamentos de HTTP para HTTPS e de www para não-www conforme necessário.

### Backup e Recuperação

Estratégias para proteger dados em produção:

**Backup Automático**: Configure scripts para backup regular da base de dados para armazenamento externo (AWS S3, Google Drive, etc.).

**Versionamento**: Mantenha múltiplas versões de backup para permitir recuperação de pontos específicos no tempo.

**Teste de Recuperação**: Teste regularmente os procedimentos de recuperação para garantir que funcionam corretamente.

**Documentação**: Mantenha documentação atualizada dos procedimentos de backup e recuperação.

### Resolução de Problemas de Deployment

Problemas comuns e suas soluções:

**Falhas de Build**: Verifique logs de build para identificar dependências em falta ou conflitos de versão.

**Timeouts de Inicialização**: Aumente timeout no Render ou otimize tempo de inicialização da aplicação.

**Problemas de Conectividade**: Verifique configurações de rede e firewall, especialmente para conexões com APIs externas.

**Erros de Variáveis de Ambiente**: Confirme que todas as variáveis necessárias estão configuradas corretamente no painel do Render.

### Custos e Escalabilidade

Considerações financeiras e de crescimento:

**Plano Gratuito**: Adequado para desenvolvimento e testes, com limitações de recursos e tempo de atividade.

**Planos Pagos**: Para produção, considere planos pagos que oferecem maior disponibilidade, recursos e suporte.

**Escalabilidade Horizontal**: O Render suporta escalabilidade automática baseada em carga de trabalho.

**Otimização de Custos**: Monitorize utilização de recursos e otimize configurações para equilibrar performance e custos.


## Integração MEGA

### Configuração da API MEGA

A integração com o MEGA constitui o núcleo do sistema de armazenamento, proporcionando capacidade escalável e distribuída para ficheiros de grande dimensão.

**Versão Atual (Simulada)**: O sistema atual utiliza uma implementação simulada da API MEGA que replica todas as funcionalidades sem conectividade real. Esta abordagem permite demonstração completa das funcionalidades e desenvolvimento sem dependências externas.

**Migração para Produção**: Para implementação real, é necessário migrar para Python 3.8 ou 3.9 devido a incompatibilidades da biblioteca `mega.py` com versões mais recentes. O processo de migração envolve:

1. **Downgrade do Python**: Instalar Python 3.8 ou 3.9 no ambiente de produção
2. **Substituição do Serviço**: Alterar imports de `mega_service_mock` para `mega_service` nos ficheiros de rotas
3. **Instalação de Dependências**: Instalar `mega.py==1.0.7` e dependências relacionadas
4. **Teste de Conectividade**: Verificar conectividade com contas MEGA reais

**Configuração de Contas**: Para utilização real, são necessárias contas MEGA válidas com espaço suficiente. Recomenda-se:
- Múltiplas contas para redundância e balanceamento
- Contas com planos pagos para maior capacidade
- Credenciais dedicadas (não contas pessoais)
- Monitorização regular do espaço disponível

### Algoritmo de Balanceamento

O sistema implementa um algoritmo sofisticado para distribuir ficheiros entre múltiplas contas MEGA:

**Seleção por Espaço Disponível**: O algoritmo primário seleciona a conta com maior espaço livre que possa acomodar o ficheiro a carregar. Esta abordagem garante utilização eficiente do espaço total disponível.

**Distribuição Equilibrada**: Para ficheiros de tamanho similar, o sistema alterna entre contas para evitar concentração excessiva numa única conta, mesmo que tenha mais espaço disponível.

**Gestão de Falhas**: Se a conta selecionada falhar durante o upload, o sistema tenta automaticamente a próxima conta disponível sem intervenção do utilizador.

**Otimização de Performance**: O algoritmo considera também a performance histórica de cada conta, priorizando contas com melhor velocidade de upload.

### Segurança e Encriptação

A segurança das credenciais MEGA é fundamental para a integridade do sistema:

**Encriptação de Credenciais**: Todas as palavras-passe MEGA são encriptadas utilizando Fernet (criptografia simétrica) antes do armazenamento. A chave de encriptação é armazenada separadamente nas variáveis de ambiente.

**Gestão de Chaves**: A chave de encriptação deve ser:
- Gerada aleatoriamente com entropia suficiente
- Armazenada de forma segura (variáveis de ambiente, não no código)
- Rotacionada periodicamente em ambientes de alta segurança
- Nunca commitada no controlo de versão

**Validação de Acesso**: Antes de armazenar credenciais, o sistema testa a conectividade e valida permissões de acesso à conta MEGA.

**Auditoria**: Todos os acessos às contas MEGA são registados para auditoria e detecção de anomalias.

### Limitações e Considerações

**Limites da API**: A API do MEGA tem limitações que devem ser consideradas:
- Rate limiting para prevenir abuso
- Limites de largura de banda para contas gratuitas
- Restrições de tamanho de ficheiro (embora suporte até 5GB)
- Possíveis interrupções de serviço

**Dependências Externas**: O sistema depende da disponibilidade dos serviços MEGA, incluindo:
- Conectividade de rede estável
- Disponibilidade dos servidores MEGA
- Manutenção das contas configuradas

**Compliance e Legalidade**: Considere aspectos legais:
- Termos de serviço do MEGA
- Regulamentações de proteção de dados (GDPR, etc.)
- Políticas de retenção de dados
- Jurisdição dos dados armazenados

## Resolução de Problemas

### Problemas Comuns de Instalação

**Erro: "mega.py incompatível"**: Este erro ocorre em Python 3.10+ devido a mudanças na API asyncio. Soluções:
- Utilizar Python 3.8 ou 3.9 para integração real
- Manter versão simulada para desenvolvimento
- Aguardar atualização da biblioteca mega.py

**Erro: "Dependências não encontradas"**: Problemas de instalação de dependências:
```bash
# Limpar cache pip
pip cache purge

# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt --no-cache-dir
```

**Erro: "Base de dados bloqueada"**: SQLite pode bloquear em alguns sistemas:
- Verificar permissões de ficheiro
- Eliminar ficheiro `app.db` e reiniciar
- Considerar migração para PostgreSQL

### Problemas de Conectividade

**Timeouts de Upload**: Para ficheiros grandes ou conexões lentas:
- Aumentar timeout nas configurações Flask
- Verificar estabilidade da conexão de rede
- Considerar upload em chunks menores

**Falhas de Autenticação MEGA**: Problemas com credenciais:
- Verificar validade das credenciais no site MEGA
- Confirmar que a conta não está suspensa
- Testar conectividade manual

**Problemas de CORS**: Erros de Cross-Origin Resource Sharing:
- Verificar configuração CORS no Flask
- Confirmar que frontend e backend estão no mesmo domínio
- Ajustar configurações de segurança do navegador

### Problemas de Performance

**Uploads Lentos**: Otimizações para melhorar velocidade:
- Verificar largura de banda disponível
- Otimizar configurações de rede
- Considerar CDN para distribuição geográfica

**Interface Lenta**: Problemas de responsividade:
- Verificar recursos do servidor
- Otimizar consultas à base de dados
- Implementar cache quando apropriado

**Consumo Excessivo de Memória**: Para ficheiros grandes:
- Implementar streaming de upload
- Otimizar gestão de memória
- Considerar processamento assíncrono

## Desenvolvimento Futuro

### Funcionalidades Planeadas

**Autenticação de Utilizadores**: Implementar sistema completo de registo e login para utilizadores finais, permitindo:
- Gestão personalizada de ficheiros
- Quotas individuais de armazenamento
- Histórico de uploads por utilizador
- Partilha privada entre utilizadores

**API REST Completa**: Expandir a API atual para suportar:
- Autenticação via tokens JWT
- Endpoints para gestão de utilizadores
- Webhooks para notificações
- Documentação OpenAPI/Swagger

**Interface de Administração Avançada**: Melhorar o painel de administração com:
- Dashboard com métricas em tempo real
- Relatórios de utilização detalhados
- Gestão de utilizadores e permissões
- Configurações avançadas do sistema

**Otimizações de Performance**: Implementar melhorias técnicas:
- Cache Redis para metadados
- Processamento assíncrono de uploads
- Compressão automática de ficheiros
- CDN para distribuição global

### Melhorias Técnicas

**Base de Dados**: Migração para soluções mais robustas:
- PostgreSQL para produção
- Índices otimizados para pesquisa
- Particionamento para grandes volumes
- Backup automático e recuperação

**Segurança**: Reforçar aspectos de segurança:
- Autenticação de dois fatores
- Auditoria completa de ações
- Encriptação end-to-end
- Detecção de anomalias

**Escalabilidade**: Preparar para crescimento:
- Arquitetura de microserviços
- Load balancing automático
- Escalabilidade horizontal
- Monitorização avançada

### Roadmap de Desenvolvimento

**Fase 1 (Curto Prazo)**:
- Migração para Python 3.8/3.9
- Integração MEGA real
- Testes automatizados
- Documentação API

**Fase 2 (Médio Prazo)**:
- Sistema de utilizadores
- API REST completa
- Interface mobile nativa
- Integrações com outros serviços de cloud

**Fase 3 (Longo Prazo)**:
- Arquitetura distribuída
- Machine learning para otimizações
- Compliance avançado
- Expansão internacional

---

## Conclusão

O Sistema de Partilha de Ficheiros representa uma solução completa e moderna para gestão e partilha de ficheiros de grande dimensão. Através da integração com o MEGA como backend de armazenamento, o sistema oferece escalabilidade, redundância e performance adequadas para utilizações desde pequenos projetos até implementações empresariais.

A arquitetura modular e bem documentada facilita manutenção, extensão e personalização conforme necessidades específicas. O sistema atual, embora utilize simulação MEGA para demonstração, está preparado para migração rápida para ambiente de produção real.

Com funcionalidades abrangentes de upload, pesquisa, administração e monitorização, o sistema atende aos requisitos modernos de partilha de ficheiros, mantendo foco na usabilidade, segurança e performance.

**Autor**: Manus AI  
**Versão**: 1.0  
**Data**: 23 de Julho de 2025

