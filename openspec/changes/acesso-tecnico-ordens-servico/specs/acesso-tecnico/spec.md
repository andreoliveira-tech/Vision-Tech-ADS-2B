# Specification: Acesso do técnico e autenticação

## Purpose

Definir autenticação de colaboradores e técnicos e o acesso individual de técnicos às ordens de serviço atribuídas.

## ADDED Requirements

### Requirement: Auditoria de signup com campos explicitamente permitidos
O endpoint auth/signup MUST mapear metadata explicitamente com somente id,
created_at, name, email, account_id e role. MUST NOT encaminhar o usuário completo,
senha, recuperação, token ou campos futuros. MUST preservar GUID, criação do
usuário member sem perfil funcional ou vínculo, token com validade existente e
resposta authToken/user_id. MUST NOT alterar helper ou logs históricos.

#### Scenario: Cadastro legado preservado com auditoria limitada
- **WHEN** signup conclui o fluxo legado de criação e emissão de token
- **THEN** somente os seis campos permitidos são encaminhados à auditoria
- **AND** cadastro, token, resposta e ausência de concessão funcional são preservados

#### Scenario: Campo sensível ou futuro existe no usuário
- **WHEN** o objeto retornado pelo banco contém campos adicionais
- **THEN** esses campos não são copiados implicitamente para metadata

### Requirement: Recuperação explícita do painel técnico
O painel MUST distinguir falha de consulta de lista vazia confirmada. Após erro de leitura ou atualização, MUST NOT repetir chamadas em rerun e MUST exigir atualização explícita para recuperar dados e controles de escrita.

#### Scenario: Falha de consulta seguida de rerun
- **WHEN** a leitura falha e a tela é renderizada novamente
- **THEN** o aviso permanece, não é apresentada ausência de OS como resultado confirmado e nenhuma nova requisição é enviada sem ação explícita

#### Scenario: Atualização de status incerta
- **WHEN** o PATCH falha ou retorna resultado incompatível
- **THEN** dados e controles anteriores são invalidados e a recuperação exige o botão de atualização, sem PATCH ou GET automático

### Requirement: Autenticação real de colaboradores e técnicos
O sistema MUST autenticar colaboradores e técnicos por um mecanismo real integrado ao backend. A interface MUST distinguir sessão autenticada de sessão anônima, e MUST NOT conceder acesso por credenciais fictícias, valores locais fixos ou apenas pelo estado da interface.

#### Scenario: Login válido
- **WHEN** um colaborador ou técnico apresenta credenciais válidas ao mecanismo configurado
- **THEN** o sistema estabelece uma sessão autenticada e identifica seu perfil e, para técnico, sua associação ao cadastro de Técnico

#### Scenario: Login inválido
- **WHEN** as credenciais são inválidas ou o mecanismo de autenticação falha
- **THEN** o sistema não cria sessão autenticada nem libera recursos protegidos

#### Scenario: Usuário anônimo solicita área protegida
- **WHEN** uma sessão anônima tenta acessar consulta ou alteração de ordens
- **THEN** o backend rejeita a solicitação e a interface solicita autenticação sem expor dados protegidos

### Requirement: Perfis e autorização no backend
O sistema MUST aplicar permissões de colaborador e técnico no backend em cada operação protegida. O perfil técnico MUST limitar consulta e alteração de status às ordens atribuídas ao técnico associado à identidade autenticada. O perfil colaborador MUST poder acessar as operações gerais de gerenciamento do sistema; operações não implementadas nesta Change permanecem fora de seu escopo. A interface MUST NOT ser a única camada de autorização.

#### Scenario: Técnico consulta suas ordens
- **WHEN** um técnico autenticado consulta suas ordens
- **THEN** o backend retorna somente ordens cujo `id_tecnico` corresponda ao cadastro de Técnico associado à identidade autenticada

#### Scenario: Técnico tenta consultar ordem de outro técnico
- **WHEN** um técnico solicita uma ordem atribuída a outro técnico, diretamente ou por filtro adulterado
- **THEN** o backend rejeita ou omite a ordem sem revelar seus dados

#### Scenario: Técnico tenta atualizar ordem não atribuída
- **WHEN** um técnico solicita alteração de status de uma ordem não associada ao seu cadastro
- **THEN** o backend rejeita a operação e mantém o status inalterado

#### Scenario: Colaborador acessa operações gerais
- **WHEN** um colaborador autenticado executa uma operação geral de gerenciamento existente
- **THEN** o backend autoriza o perfil colaborador e aplica as validações próprias da operação

### Requirement: Associação com o cadastro de Técnico existente
Cada identidade com perfil técnico MUST estar associada a exatamente um registro existente de Técnico. Essa associação MUST usar a identidade nativa do mecanismo de autenticação e o identificador do cadastro de Técnico, sem duplicar atributos de domínio nem introduzir entidade de negócio adicional. Identidades sem associação válida MUST NOT receber acesso de técnico.

#### Scenario: Associação válida
- **WHEN** a sessão identifica um técnico com associação válida a `id_tecnico`
- **THEN** consultas e autorização usam esse identificador para determinar as OS atribuídas

#### Scenario: Associação ausente ou inválida
- **WHEN** a identidade tem perfil técnico, mas não há cadastro associado ou o cadastro não existe
- **THEN** o backend nega acesso de técnico e não retorna ordens

### Requirement: Área de acompanhamento do técnico
A aplicação MUST oferecer ao técnico autenticado uma área para acompanhar as ordens atribuídas. Cada item apresentado MUST incluir os dados do equipamento relacionado, o problema relatado e o status atual da ordem. A área MUST apresentar apenas ordens autorizadas para aquele técnico.

#### Scenario: Exibição de ordem atribuída
- **WHEN** o técnico autenticado abre sua área de acompanhamento
- **THEN** cada ordem retornada exibe equipamento, problema relatado e status atual

#### Scenario: Técnico sem ordens atribuídas
- **WHEN** a consulta autorizada não encontra ordens para o técnico
- **THEN** a área informa que não há ordens atribuídas sem exibir ordens de terceiros

### Requirement: Atualização autorizada do status
O sistema MUST permitir que o técnico atualize o status de uma ordem atribuída somente por operação autenticada e autorizada no backend. A atualização MUST usar os estados de OS definidos pelo domínio e MUST rejeitar ordem não atribuída, estado inválido ou perfil sem permissão. A interface MUST refletir o resultado confirmado pelo backend.

#### Scenario: Técnico atualiza sua ordem
- **WHEN** o técnico autenticado envia um status válido para uma ordem atribuída
- **THEN** o backend verifica a associação e a permissão, persiste a alteração e retorna o status confirmado

#### Scenario: Status inválido
- **WHEN** o técnico envia valor fora dos estados definidos para OS
- **THEN** o backend rejeita a alteração e preserva o status anterior

#### Scenario: Atualização sem autorização
- **WHEN** a identidade não tem perfil técnico ou a ordem não está atribuída a ela
- **THEN** o backend rejeita a alteração sem modificar a ordem


### Requirement: Sessao temporaria e navegacao por perfil
O Streamlit MUST armazenar o token apenas durante a sessao do processo, identificar o usuario exclusivamente por `auth/me` e oferecer logout local. MUST NOT guardar senha ou inferir perfil pela interface. A expiracao MUST limpar a sessao local e bloquear paginas protegidas.

#### Scenario: Perfil colaborador navega
- **WHEN** `auth/me` retorna perfil funcional `colaborador`
- **THEN** a navegacao apresenta somente as paginas administrativas previstas para colaborador

#### Scenario: Perfil tecnico navega
- **WHEN** `auth/me` retorna perfil `tecnico` e `id_tecnico` valido
- **THEN** a navegacao apresenta o painel de OS do tecnico

#### Scenario: Logout local
- **WHEN** o usuario seleciona Sair
- **THEN** o Streamlit remove token, identidade e estado protegido da sessao local
- **AND** o sistema nao declara que o token foi revogado no Xano sem endpoint de revogacao

### Requirement: Dados apresentados no painel tecnico
Cada OS autorizada apresentada no painel MUST mostrar `id_os`, equipamento, marca, modelo, problema relatado, status atual e data de entrada. Os dados MUST vir das APIs; ausencia ou indisponibilidade dos detalhes do equipamento MUST ser informada sem inventar atributos.

#### Scenario: Painel mostra os campos previstos
- **WHEN** a API retorna OS atribuida e os detalhes do equipamento existem
- **THEN** a tela mostra numero da OS, equipamento, marca, modelo, problema, status e data de entrada

#### Scenario: Detalhe de equipamento indisponivel
- **WHEN** a API de Equipamentos nao consegue confirmar os detalhes associados
- **THEN** a interface informa a indisponibilidade sem inventar marca ou modelo

#### Scenario: Dados de equipamento na listagem protegida do tecnico
- **WHEN** um tecnico autenticado solicita `GET /minhas-ordens`
- **THEN** o backend valida a identidade e o vinculo do tecnico antes de filtrar as OS atribuidas
- **AND** inclui tipo, marca e modelo do equipamento associado na resposta autorizada
- **AND** o Streamlit nao consulta um endpoint publico de Equipamentos para compor o painel

#### Scenario: Equipamento da OS autorizada não pode ser confirmado
- **WHEN** a consulta autorizada não encontra o Equipamento referenciado pela OS
- **THEN** o backend interrompe a composição com erro, sem devolver dados inventados ou lista parcial como sucesso

#### Scenario: Tipo obrigatório e detalhes opcionais no painel
- **WHEN** a listagem técnica inclui um Equipamento existente
- **THEN** tipo corresponde ao cadastro relacionado e marca/modelo preservam seus valores, inclusive null quando opcionais
- **AND** uma resposta com tipo null é rejeitada pela interface, sem liberar atualização de status nem repetir a consulta automaticamente

### Requirement: Provisionamento protegido de perfis funcionais
O backend MUST manter `user.role=admin/member` e os contratos de autenticacao nativa intactos. O perfil funcional e a autoridade de provisionamento MUST residir em `user_application_profile`; a associacao ao cadastro de negocio existente MUST residir em `user_tecnico`. Essas tabelas sao infraestrutura tecnica e nao alteram as cinco entidades de negocio.

`user_application_profile.user_id` MUST ser FK obrigatoria e UNIQUE; `perfil_aplicacao` MUST aceitar somente `colaborador` ou `tecnico`; `pode_provisionar_perfis` MUST ser privado. O provisionador MUST gravar explicitamente `false` ao criar um perfil, e somente o valor estritamente `true` MUST autorizar provisionamento (ausencia/null nega). `user_tecnico.user_id` e `user_tecnico.id_tecnico` MUST ser FKs obrigatorias e UNIQUE. Signup publico MUST continuar criando somente `user` com papel legado `member`, sem criar perfil nem associacao. Usuario sem perfil funcional MUST ter acesso negado.

Somente usuario autenticado com papel legado `admin`, perfil funcional `colaborador` e `pode_provisionar_perfis=true` MUST provisionar outro usuario da mesma conta. A aplicacao MUST NOT aceitar o sinalizador como entrada. Provisionamento de `tecnico` MUST validar cadastro existente e associacao exclusiva. A constraint UNIQUE MUST impedir duplicidade sob concorrencia; consulta previa isolada nao e suficiente. Atualizacao de perfil e associacao MUST ser atomica. Mapeamento da violacao concorrente para HTTP conflito permanece pendente de confirmacao do erro e constraint no runtime Xano.

O provisionador MUST bloquear as identidades existentes do operador e alvo em ordem crescente de ID dentro da transação, antes de ler os perfis e vínculos usados nas decisões. MUST exigir comparação estrita `=== true` para o sinalizador. Todas as validações MUST ocorrer antes das gravações. A auditoria de sucesso MUST ser uma operação DB dentro da mesma transação. Erros desconhecidos MUST propagar sem catch genérico ou tradução presumida; o mapeamento específico de UNIQUE requer evidência de runtime para as três constraints das tabelas técnicas.

#### Scenario: Provisionamentos concorrentes do mesmo usuario
- **WHEN** duas chamadas deste provisionador alteram o mesmo alvo, inclusive sem perfil/vinculo inicial
- **THEN** os locks das identidades serializam as decisões e o estado é lido depois da aquisição dos locks
- **AND** a ordem crescente de ID é a mesma para operador e alvo em todas as chamadas

#### Scenario: Falha de auditoria DB
- **WHEN** a gravação de event_log falha durante o provisionamento
- **THEN** a transação deve reverter perfil e vínculo, e o erro deve propagar
- **AND** esse rollback permanece sujeito a validação no runtime isolado antes de publicação

#### Scenario: Administrador provisiona colaborador
- **WHEN** provisionador autorizado atribui `colaborador` a outro usuario da mesma conta
- **THEN** o backend grava o perfil tecnico de autorizacao sem alterar `user.role` nem criar associacao tecnica

#### Scenario: Administrador provisiona tecnico com associacao valida
- **WHEN** provisionador autorizado atribui `tecnico` e informa cadastro existente sem associacao concorrente
- **THEN** o backend grava perfil e associacao exclusiva atomicamente

#### Scenario: Perfil tecnico invalido ou duplicado
- **WHEN** o cadastro tecnico nao existe ou ja esta associado
- **THEN** o backend rejeita a operacao e preserva as associacoes existentes

#### Scenario: Requisicoes concorrentes tentam associar o mesmo tecnico
- **WHEN** duas requisicoes tentam associar o mesmo `id_tecnico` a usuarios diferentes
- **THEN** a constraint UNIQUE permite no maximo uma associacao persistida; mapeamento da requisicao perdedora para resposta de conflito requer verificacao de runtime

#### Scenario: Member ou admin comum tenta elevar privilegios
- **WHEN** usuario sem a combinacao `admin` + perfil `colaborador` + `pode_provisionar_perfis=true` tenta provisionar qualquer alvo
- **THEN** o backend rejeita sem modificar perfil ou associacao

#### Scenario: Tentativa de auto provisionamento ou outra conta
- **WHEN** provisionador autorizado informa a si mesmo ou usuario de outra conta como alvo
- **THEN** o backend rejeita sem gravar alteracoes

#### Scenario: Signup, criacao de conta ou papel legado manipulam perfil
- **WHEN** signup, `POST /account` ou `admin/user_role` recebem ou alteram dados funcionais
- **THEN** contratos legados permanecem preservados e nenhum perfil funcional, sinalizador ou vinculo e concedido

### Requirement: Auditoria de login com campos explicitamente permitidos
O endpoint auth/login MUST enviar à auditoria somente id, created_at, name, email, account_id e role, mapeados explicitamente a partir do usuário. MUST NOT encaminhar o objeto de usuário completo, senha protegida ou em texto puro, dados de recuperação, tokens ou campos futuros não autorizados. A correção MUST preservar GUID, validação de senha, criação e expiração do token e formato da resposta. MUST NOT alterar create_event_log, auth/me ou o provisionador da etapa 06.

#### Scenario: Login válido produz auditoria sem senha
- **WHEN** credenciais válidas são verificadas pelo fluxo existente
- **THEN** o endpoint mantém a resposta authToken/user_id e grava metadados somente com os seis campos permitidos

#### Scenario: Credenciais inválidas continuam negadas
- **WHEN** a senha fornecida não corresponde ao usuário
- **THEN** a validação existente rejeita antes da emissão de token ou gravação de auditoria de sucesso

#### Scenario: Recursos não incluídos na correção
- **WHEN** o pacote isolado de auditoria de login é preparado
- **THEN** ele contém somente a atualização do endpoint de login pelo GUID existente
- **AND** signup e limpeza de logs anteriores permanecem pendentes de autorização própria
