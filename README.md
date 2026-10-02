# POC de Provisionamento Automático de Acessos com LDAP

## 1. Apresentação

Este repositório documenta uma **Prova de Conceito (POC)** desenvolvida a partir de um estudo técnico sobre autenticação, identidade e provisionamento de acessos no ambiente **Facilit**.

O ponto de partida foi uma necessidade operacional identificada no processo atual: mesmo quando um colaborador já possui uma identidade corporativa, o acesso ao sistema ainda precisa ser criado manualmente. Esse procedimento exige que uma pessoa da equipe entre na aplicação, cadastre o usuário, associe um perfil e mantenha essas permissões atualizadas sempre que houver mudança de função.

A POC foi construída para responder à seguinte pergunta:

> É possível utilizar o LDAP como fonte central de identidade para autenticar usuários, criar automaticamente seus acessos no primeiro login e definir as permissões com base nos grupos corporativos?

O estudo demonstrou que essa automação é tecnicamente viável.

Nesta implementação, um usuário previamente cadastrado no LDAP consegue realizar o primeiro login na aplicação sem ter sido criado manualmente dentro dela. A aplicação consulta o diretório, valida as credenciais, cria o cadastro interno e atribui o perfil correspondente ao grupo LDAP.

A POC também comprovou que, quando um usuário muda de grupo no LDAP, sua permissão pode ser atualizada automaticamente no login seguinte, sem edição manual dentro do sistema.

---

## 2. Origem do estudo

O trabalho foi iniciado a partir de um levantamento anterior sobre a arquitetura de autenticação do ambiente Facilit.

Esse levantamento considerava uma estrutura em que:

- o sistema precisava reconhecer os usuários;
- as identidades deveriam ser centralizadas;
- os acessos deveriam ser organizados por grupos;
- as permissões precisavam ser aplicadas de forma padronizada;
- a solução deveria priorizar tecnologias open source;
- o processo atual de criação manual deveria ser reduzido.

Durante o estudo foram analisados dois caminhos principais:

1. integração direta com LDAP;
2. uso de uma camada de identidade baseada em OIDC, como o Keycloak.

O objetivo inicial não era escolher a solução mais complexa ou mais moderna, mas identificar a alternativa que atendesse à necessidade real com menor custo operacional e menor número de componentes.

---

## 3. Avaliação de LDAP e OIDC

### 3.1 LDAP

LDAP é um protocolo utilizado para consultar e manter informações em serviços de diretório.

Dentro desta proposta, o LDAP funciona como a fonte central de:

- usuários;
- nomes;
- e-mails;
- credenciais;
- grupos;
- vínculos de acesso.

O diretório informa à aplicação:

- se o usuário existe;
- se a senha está correta;
- a quais grupos ele pertence.

A aplicação utiliza essas informações para criar ou atualizar o cadastro interno e aplicar o perfil correspondente.

### 3.2 OIDC

OIDC, ou OpenID Connect, é uma camada de autenticação construída sobre OAuth 2.0.

Uma solução baseada em OIDC poderia utilizar um provedor de identidade, como o Keycloak, entre o LDAP e as aplicações.

O fluxo seria semelhante a:

```text
Usuário
  ↓
Aplicação
  ↓
Keycloak / OIDC
  ↓
LDAP ou Active Directory
```

Esse modelo é adequado quando existe necessidade de:

- Single Sign-On entre várias aplicações;
- autenticação por tokens;
- integração padronizada com sistemas modernos;
- federação de identidades;
- MFA centralizado;
- integração com aplicações que não suportam LDAP diretamente;
- uso de OIDC ou SAML.

### 3.3 Por que OIDC foi descartado nesta fase

OIDC e Keycloak não foram considerados tecnologias inadequadas.

Eles foram retirados do escopo atual porque não havia necessidade comprovada de adicionar uma nova camada de identidade neste momento.

O Superset, utilizado como aplicação representativa da POC, possui suporte direto a LDAP. Portanto, incluir Keycloak significaria adicionar:

- mais um serviço;
- mais configurações;
- mais pontos de falha;
- mais manutenção;
- mais consumo de recursos;
- mais complexidade operacional.

Como o objetivo imediato era validar autenticação centralizada, criação automática de usuários e aplicação de permissões por grupos, a integração direta com LDAP foi suficiente.

A decisão adotada foi:

> Utilizar LDAP diretamente enquanto ele atender aos requisitos atuais. OIDC poderá ser reavaliado futuramente caso surjam necessidades de SSO, MFA, federação de identidade, tokens ou integração com várias aplicações.

---

## 4. Diretriz open source

O estudo priorizou tecnologias open source para facilitar:

- experimentação;
- auditoria;
- reprodutibilidade;
- independência de fornecedor;
- execução em ambiente local;
- controle da infraestrutura;
- redução de custos de licenciamento.

A POC utiliza:

| Tecnologia | Finalidade |
|---|---|
| OpenLDAP | Diretório central de usuários e grupos |
| phpLDAPadmin | Administração visual do LDAP |
| Apache Superset | Aplicação representativa integrada ao LDAP |
| PostgreSQL | Banco interno do Superset |
| Docker Compose | Orquestração dos serviços |
| Python e Flask-AppBuilder | Configuração de autenticação e papéis |

Todos os dados utilizados são fictícios e pertencem exclusivamente ao laboratório.

---

## 5. Problema observado

O fluxo manual pode ser representado da seguinte forma:

```text
Colaborador precisa de acesso
        ↓
Solicitação é encaminhada à equipe
        ↓
Usuário é criado manualmente no sistema
        ↓
Perfil é escolhido manualmente
        ↓
Acesso é liberado
        ↓
Mudanças futuras exigem nova intervenção
```

Esse processo pode gerar:

- aumento no tempo de atendimento;
- repetição de tarefas;
- erros de digitação;
- perfis incorretos;
- inconsistência entre sistemas;
- contas que permanecem ativas indevidamente;
- dificuldade de auditoria;
- dependência de conhecimento individual;
- maior volume de chamados operacionais.

---

## 6. Solução proposta

O fluxo proposto é:

```text
Usuário já existe no diretório corporativo
        ↓
Usuário acessa o sistema
        ↓
Sistema consulta o LDAP
        ↓
LDAP valida usuário e senha
        ↓
LDAP informa os grupos
        ↓
Sistema cria ou atualiza o cadastro
        ↓
Sistema aplica o perfil correspondente
```

Nesse modelo, o LDAP centraliza a identidade e os grupos.

A aplicação continua responsável por:

- executar a autenticação;
- criar o cadastro interno;
- associar os papéis;
- sincronizar mudanças;
- controlar as permissões próprias do sistema.

O LDAP não automatiza a aplicação sozinho. A automação acontece porque a aplicação foi configurada para utilizar o diretório como fonte de identidade.

---

## 7. Objetivo geral

Validar a viabilidade técnica de automatizar o provisionamento e a atualização de acessos por meio de integração LDAP.

---

## 8. Objetivos específicos

A POC foi desenvolvida para verificar se seria possível:

- autenticar usuários utilizando credenciais LDAP;
- criar automaticamente o cadastro interno no primeiro login;
- associar grupos LDAP a papéis da aplicação;
- testar diferentes níveis de acesso;
- atualizar automaticamente uma permissão após mudança de grupo;
- recusar credenciais inválidas;
- manter os dados após reinicialização dos containers;
- reproduzir o ambiente utilizando Docker Compose;
- documentar uma base para futura integração com o sistema real.

---

## 9. Hipótese

A hipótese adotada foi:

> Se a aplicação consultar o LDAP durante o login, criar automaticamente usuários válidos e mapear grupos para papéis internos, então será possível reduzir a necessidade de criação e manutenção manual de acessos.

---

## 10. Escopo da POC

A POC contempla:

- OpenLDAP;
- phpLDAPadmin;
- PostgreSQL;
- Apache Superset;
- autenticação LDAP;
- criação automática no primeiro login;
- mapeamento de grupos;
- sincronização de papéis;
- perfis Admin, Alpha e Gamma;
- recusa de senha incorreta;
- persistência por volumes Docker;
- alteração de permissão por mudança de grupo.

A POC não contempla:

- implantação no sistema real;
- ambiente de produção;
- usuários ou dados reais;
- alta disponibilidade;
- integração com RH;
- MFA;
- Single Sign-On;
- LDAPS ou StartTLS;
- auditoria corporativa completa;
- testes de carga;
- processo definitivo de desligamento;
- federação de identidades.

---

## 11. Arquitetura lógica

```text
Usuário
  |
  | login
  v
Apache Superset
  |
  | consulta, bind e grupos
  v
OpenLDAP
  |
  | usuários e grupos
  v
Diretório de identidades

Apache Superset
  |
  | metadados internos
  v
PostgreSQL

Administrador
  |
  | interface web
  v
phpLDAPadmin
  |
  | administração do diretório
  v
OpenLDAP
```

---

## 12. Função dos componentes

### 12.1 OpenLDAP

Responsável por armazenar:

- identidades;
- credenciais;
- atributos;
- grupos;
- associações entre usuários e grupos.

### 12.2 phpLDAPadmin

Utilizado para visualizar e administrar o diretório durante o laboratório.

### 12.3 Apache Superset

Utilizado como aplicação representativa.

O Superset permitiu demonstrar:

- login LDAP;
- criação automática;
- lista de usuários;
- perfis internos;
- sincronização de permissões.

O Superset não representa necessariamente o sistema final do Facilit. Ele foi usado para validar o conceito técnico.

### 12.4 PostgreSQL

Armazena os dados internos do Superset, como:

- usuários provisionados;
- papéis;
- permissões;
- configurações;
- objetos da aplicação.

A senha corporativa continua sendo validada pelo LDAP.

### 12.5 Docker Compose

Responsável por:

- criar a rede;
- iniciar os serviços;
- conectar os containers;
- definir portas;
- manter os volumes;
- facilitar a reprodução do ambiente.

---

## 13. Estrutura do diretório LDAP

```text
dc=empresa,dc=test
├── ou=usuarios
│   ├── uid=admin.poc
│   ├── uid=analista.poc
│   ├── uid=funcionario.poc
│   └── uid=mudanca.poc
└── ou=grupos
    ├── cn=sistema_admins
    ├── cn=sistema_analistas
    └── cn=sistema_leitores
```

---

## 14. Mapeamento de grupos e papéis

| Grupo LDAP | Papel no Superset | Finalidade |
|---|---|---|
| `sistema_admins` | `Admin` | Administração completa |
| `sistema_analistas` | `Alpha` | Criação e análise de conteúdo |
| `sistema_leitores` | `Gamma` | Acesso restrito |

O papel padrão Gamma foi mantido como fallback para grupos não reconhecidos, mas um gerenciador de segurança customizado foi utilizado para evitar o acúmulo indevido de papéis.

Resultado final:

```text
admin.poc       → Admin
analista.poc    → Alpha
funcionario.poc → Gamma
mudanca.poc     → Gamma e depois Alpha
```

---

## 15. Testes executados

### 15.1 Autenticação administrativa

O usuário `admin.poc` foi autenticado pelo LDAP e recebeu o papel `Admin`.

**Resultado:** aprovado.

### 15.2 Provisionamento no primeiro login

O usuário `funcionario.poc` existia no LDAP, mas não existia no Superset.

Após o primeiro login:

- as credenciais foram validadas;
- o cadastro interno foi criado;
- o papel Gamma foi aplicado.

**Resultado:** aprovado.

### 15.3 Perfil Alpha

O usuário `analista.poc` foi associado ao grupo `sistema_analistas`.

Após o login, recebeu o papel Alpha.

**Resultado:** aprovado.

### 15.4 Atualização de permissão

O usuário `mudanca.poc` foi criado inicialmente no grupo `sistema_leitores`.

Resultado inicial:

```text
Gamma
```

Depois, ele foi removido do grupo de leitores e adicionado ao grupo de analistas.

No login seguinte, o papel foi atualizado para:

```text
Alpha
```

Nenhuma alteração manual foi realizada dentro do Superset.

**Resultado:** aprovado.

### 15.5 Senha inválida

Foi realizado um teste com uma senha incorreta.

O LDAP retornou credenciais inválidas e o acesso foi recusado.

**Resultado:** aprovado.

### 15.6 Persistência

Os containers foram desligados com:

```bash
docker compose down
```

Depois foram iniciados novamente.

Os usuários, grupos e cadastros permaneceram disponíveis.

**Resultado:** aprovado.

---

## 16. Resultado consolidado

| Requisito | Resultado |
|---|---|
| Autenticação LDAP | Aprovado |
| Cadastro automático | Aprovado |
| Papel Admin | Aprovado |
| Papel Alpha | Aprovado |
| Papel Gamma | Aprovado |
| Atualização Gamma para Alpha | Aprovado |
| Senha inválida recusada | Aprovado |
| Persistência | Aprovado |

---

## 17. Resposta à ideia inicial

A ideia inicial foi confirmada no laboratório.

Foi possível substituir o cadastro manual dentro da aplicação por um fluxo em que:

- a identidade existe no LDAP;
- o login é validado pelo LDAP;
- o cadastro interno é criado automaticamente;
- a permissão é atribuída pelo grupo;
- mudanças de função são refletidas no login seguinte.

Portanto, a proposta é tecnicamente viável.

Entretanto, a POC não significa que o sistema real já está automatizado.

O próximo passo é analisar o sistema utilizado pelo Facilit para determinar:

- se possui suporte LDAP nativo;
- se permite criação automática;
- como armazena usuários;
- como representa papéis;
- onde a integração deve ser configurada ou desenvolvida;
- quais requisitos de segurança devem ser aplicados.

---

## 18. Proposta para a próxima fase

A próxima fase deve ser um levantamento técnico do sistema real.

### Etapa 1 — Descoberta

- identificar tecnologias;
- analisar autenticação atual;
- localizar banco e tabela de usuários;
- identificar papéis;
- verificar suporte LDAP;
- identificar ambiente de homologação.

### Etapa 2 — Mapeamento

- definir grupos corporativos;
- relacionar grupos e papéis;
- definir responsáveis;
- definir fallback;
- definir fluxo de aprovação.

### Etapa 3 — Homologação

- integrar LDAP;
- testar login;
- testar criação automática;
- testar mudança de grupo;
- testar bloqueio;
- testar logs;
- testar rollback.

### Etapa 4 — Piloto

- selecionar poucos usuários;
- acompanhar resultados;
- corrigir inconsistências;
- validar segurança.

### Etapa 5 — Produção

- implantar gradualmente;
- documentar operação;
- monitorar;
- reduzir o fluxo manual;
- manter plano de contingência.

---

## 19. Considerações de segurança

O laboratório utiliza configurações simplificadas.

Em produção será necessário:

- utilizar LDAPS ou StartTLS;
- proteger segredos;
- usar conta de bind somente leitura;
- restringir portas;
- aplicar menor privilégio;
- registrar logs;
- definir expiração;
- definir desligamento;
- executar backups;
- revisar grupos;
- testar rollback;
- considerar alta disponibilidade.

---

## 20. Conclusão

A POC demonstrou que uma integração LDAP direta pode atender à necessidade atual de autenticação centralizada e provisionamento automático sem exigir, neste momento, uma camada OIDC adicional.

A escolha por LDAP direto foi adequada para o escopo porque:

- o Superset oferece integração nativa;
- os requisitos eram autenticação, grupos e papéis;
- a solução utiliza componentes open source;
- o ambiente permaneceu simples;
- os resultados foram comprovados;
- a complexidade adicional do Keycloak não era necessária.

OIDC continua sendo uma possibilidade futura, e não uma tecnologia descartada definitivamente.

Ele deverá ser reavaliado caso o projeto passe a exigir:

- SSO;
- MFA;
- integração com várias aplicações;
- tokens;
- SAML;
- federação de identidades;
- identidade central para serviços modernos.

Com base nos testes realizados, recomenda-se avançar para o levantamento do sistema real e para uma implementação controlada em ambiente de homologação.

---

# 21. Como executar a POC em outra máquina

Esta seção apresenta o procedimento completo para reproduzir o laboratório a partir de um clone limpo do repositório.

## 21.1 Pré-requisitos

A máquina deve possuir:

- Git;
- Docker Engine;
- Docker Compose;
- Linux ou WSL2.

Verifique:

```bash
git --version
docker --version
docker compose version
docker ps
```

O comando `docker ps` pode mostrar uma tabela vazia. Isso apenas significa que nenhum container está em execução.

## 21.2 Clonar o repositório

```bash
git clone https://github.com/yaraxavier/poc-ldap-provisionamento.git
cd poc-ldap-provisionamento
```

Se o repositório estiver privado, o usuário precisa ter permissão de acesso no GitHub.

## 21.3 Criar o arquivo de configuração local

O arquivo `.env` não é enviado ao GitHub.

Crie-o a partir do modelo:

```bash
cp .env.example .env
```

Confirme:

```bash
ls -la
```

Devem aparecer:

```text
.env
.env.example
README.md
docker-compose.yml
ldap/
superset/
```

As credenciais incluídas no `.env.example` são fictícias e exclusivas do laboratório.

## 21.4 Iniciar toda a infraestrutura

Execute:

```bash
docker compose up -d --build
```

Na primeira execução, o processo pode levar alguns minutos.

Esse comando:

1. constrói a imagem personalizada do Superset;
2. inicia o OpenLDAP;
3. importa automaticamente os usuários e grupos;
4. inicia o PostgreSQL;
5. executa as migrações do Superset;
6. inicializa os papéis e permissões;
7. inicia a aplicação.

## 21.5 Verificar os serviços

```bash
docker compose ps -a
```

Resultado esperado:

```text
openldap       healthy
postgres       healthy
phpldapadmin   Up
superset-init  Exited (0)
superset       healthy
```

O estado `superset-init Exited (0)` é esperado. Esse container executa as migrações e a inicialização do Superset e encerra quando conclui.

## 21.6 Verificar a saúde do Superset

```bash
curl http://localhost:8088/health
```

Resultado esperado:

```text
OK
```

# 22. Endereços do laboratório

| Serviço | Endereço |
|---|---|
| Superset | `http://localhost:8088` |
| phpLDAPadmin | `http://localhost:8082` |
| LDAP | `ldap://localhost:3890` |
| PostgreSQL | `localhost:5433` |

# 23. Credenciais do laboratório

## 23.1 Superset

| Usuário | Senha | Grupo inicial | Papel esperado |
|---|---|---|---|
| `admin.poc` | `admin123` | `sistema_admins` | Admin |
| `analista.poc` | `analista123` | `sistema_analistas` | Alpha |
| `funcionario.poc` | `poc123` | `sistema_leitores` | Gamma |
| `mudanca.poc` | `mudanca123` | `sistema_leitores` | Gamma |

Todas as contas são fictícias e exclusivas da POC.

## 23.2 phpLDAPadmin

Acesse:

```text
http://localhost:8082
```

Credenciais:

```text
Login DN: cn=admin,dc=empresa,dc=test
Senha: admin_poc_2026
```

# 24. Como reproduzir os testes

## 24.1 Teste de administrador

Acesse:

```text
http://localhost:8088
```

Entre com:

```text
Usuário: admin.poc
Senha: admin123
```

Resultado esperado:

```text
Papel: Admin
```

## 24.2 Teste de provisionamento automático de leitor

O usuário `funcionario.poc` existe inicialmente apenas no LDAP.

Entre com:

```text
Usuário: funcionario.poc
Senha: poc123
```

Resultado esperado:

```text
O usuário é criado automaticamente no Superset.
Papel recebido: Gamma.
```

Depois, entre novamente como `admin.poc` e acesse:

```text
Configurações
→ Segurança
→ Lista de usuários
```

O usuário `funcionario.poc` deverá aparecer com o papel Gamma.

## 24.3 Teste de provisionamento automático de analista

Entre com:

```text
Usuário: analista.poc
Senha: analista123
```

Resultado esperado:

```text
O usuário é criado automaticamente.
Papel recebido: Alpha.
```

## 24.4 Teste de senha incorreta

Tente entrar com:

```text
Usuário: funcionario.poc
Senha: senha_errada
```

Resultado esperado:

```text
Acesso recusado.
```

Também é possível validar diretamente no LDAP:

```bash
docker compose exec openldap ldapwhoami \
  -x \
  -H ldap://localhost:389 \
  -D "uid=funcionario.poc,ou=usuarios,dc=empresa,dc=test" \
  -w "senha_errada"
```

Resultado esperado:

```text
ldap_bind: Invalid credentials (49)
```

## 24.5 Teste de mudança automática de permissão

O usuário `mudanca.poc` começa no grupo `sistema_leitores` e recebe Gamma no primeiro login.

Entre com:

```text
Usuário: mudanca.poc
Senha: mudanca123
```

Confirme que ele recebeu Gamma.

Depois, execute:

```bash
docker compose exec -T openldap ldapmodify \
  -x \
  -H ldap://localhost:389 \
  -D "cn=admin,dc=empresa,dc=test" \
  -w "admin_poc_2026" \
  -f /dev/stdin < ldap/10-mover-mudanca-para-analistas.ldif
```

Confirme o novo grupo:

```bash
docker compose exec openldap ldapsearch \
  -x \
  -LLL \
  -H ldap://localhost:389 \
  -D "cn=admin,dc=empresa,dc=test" \
  -w "admin_poc_2026" \
  -b "uid=mudanca.poc,ou=usuarios,dc=empresa,dc=test" \
  -s base \
  uid cn memberOf
```

Resultado esperado:

```text
memberOf: cn=sistema_analistas,ou=grupos,dc=empresa,dc=test
```

Saia da conta `mudanca.poc` e entre novamente.

Resultado esperado:

```text
Gamma → Alpha
```

Esse teste comprova que a permissão pode ser atualizada apenas pela alteração do grupo LDAP, sem edição manual no Superset.

## 24.6 Teste de persistência

Pare os containers:

```bash
docker compose down
```

Suba novamente:

```bash
docker compose up -d
```

Confira:

```bash
docker compose ps -a
```

Entre novamente no Superset.

Resultado esperado:

```text
Usuários, grupos e cadastros continuam disponíveis.
```

Não utilize `-v`, porque essa opção remove os volumes.

# 25. Possível erro 500 no navegador

Ao testar instalações diferentes usando o mesmo endereço `localhost:8088`, o navegador pode reutilizar uma sessão antiga do Superset.

Nesse caso:

1. abra uma janela anônima;
2. acesse diretamente `http://localhost:8088/login/`;
3. ou apague os cookies e dados do site `localhost`.

Esse erro tende a não ocorrer em uma máquina que nunca executou o Superset anteriormente.

# 26. Comandos operacionais

## 26.1 Verificar containers

```bash
docker compose ps -a
```

## 26.2 Ver logs do Superset

```bash
docker compose logs --tail=200 superset
```

## 26.3 Ver logs do OpenLDAP

```bash
docker compose logs --tail=200 openldap
```

## 26.4 Parar sem apagar os dados

```bash
docker compose down
```

## 26.5 Subir novamente

```bash
docker compose up -d
```

## 26.6 Apagar completamente o laboratório

```bash
docker compose down -v --remove-orphans
```

Esse comando remove containers, rede, volumes LDAP, banco PostgreSQL e dados internos do Superset.

Para reconstruir:

```bash
docker compose up -d --build
```

# 27. Fluxo resumido para avaliação

```bash
git clone https://github.com/yaraxavier/poc-ldap-provisionamento.git
cd poc-ldap-provisionamento
cp .env.example .env
docker compose up -d --build
docker compose ps -a
curl http://localhost:8088/health
```

Depois:

```text
Abrir http://localhost:8088
Testar Admin, Alpha e Gamma
Executar o teste de mudança Gamma → Alpha
```

# 28. Critérios de sucesso

A POC pode ser considerada validada quando:

- o OpenLDAP estiver saudável;
- o PostgreSQL estiver saudável;
- o Superset responder `OK` em `/health`;
- `admin.poc` receber Admin;
- `analista.poc` receber Alpha;
- `funcionario.poc` receber Gamma;
- a senha incorreta for recusada;
- `mudanca.poc` mudar de Gamma para Alpha após alteração do grupo;
- os dados persistirem após reinicialização dos containers.

