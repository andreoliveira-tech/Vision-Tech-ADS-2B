# Apresentação Streamlit

## Purpose

Oferecer apresentação consistente e legível nas telas existentes da assistência
técnica, preservando navegação por perfil e segurança das operações já implementadas.

## ADDED Requirements

### Requirement: Identidade visual comum nas telas existentes
Login, Clientes, Equipamentos, Técnicos, OS, Serviços e painel técnico MUST
compartilhar paleta, hierarquia de títulos, formulários e feedback consistentes.
A aplicação MUST permanecer exclusivamente Streamlit, sem recursos visuais
externos obrigatórios ou funcionalidades de domínio adicionais.

#### Scenario: Navegação entre módulos
- **WHEN** usuário autorizado alterna entre as telas permitidas
- **THEN** encontra o mesmo padrão de navegação, títulos, botões e legibilidade

### Requirement: Apresentação preserva permissões e estados de operação
A padronização MUST preservar perfis, guardas, logout, payloads, confirmações,
seleção de registros e bloqueio de escrita incerta. MUST NOT adicionar requests
por mudanças visuais ou permitir ação desabilitada. Ação destrutiva MUST ter
texto explícito e distinção visual além de cor, sem contornar confirmação.

#### Scenario: Técnico acessa o painel
- **WHEN** técnico autenticado navega no sistema
- **THEN** vê somente a navegação vigente do técnico, sem gestão administrativa adicional

#### Scenario: Escrita permanece incerta após atualização visual
- **WHEN** ocorre rerun ou troca visual com operação incerta pendente
- **THEN** o bloqueio e a conferência explícita permanecem, sem reenvio automático

### Requirement: Layout permanece utilizável em tela pequena e teclado
A interface MUST manter campos, ações e mensagens utilizáveis em larguras de
390 e 1440 pixels. Tabelas largas MUST permitir rolagem local sem ocultar ações
da página. Navegação e ações MUST ter foco visível; texto normal MUST alcançar
contraste de 4,5:1 e texto grande 3:1 nos pares de cores controlados pelo tema.
Cor MUST NOT ser o único indicador de sucesso, erro, estado ou exclusão.

#### Scenario: Formulário em largura pequena
- **WHEN** a tela é exibida com 390 pixels de largura
- **THEN** os campos e botões são alcançáveis sem corte e mensagens permanecem legíveis

#### Scenario: Uso do teclado e distinção de erro
- **WHEN** usuário percorre os controles com teclado ou recebe erro de operação
- **THEN** o foco é identificável e a mensagem explica o resultado sem depender apenas da cor

### Requirement: Inicialização configura todos os módulos sem segredos
O iniciador local MUST fornecer configuração externa das seis URLs de grupos
quando ausentes e preservar valores já informados pelo operador. MUST NOT
armazenar credenciais, executar login, instalar dependências automaticamente,
habilitar exclusão pendente ou realizar validação de configuração por HTTP.
URL inválida MUST continuar sendo rejeitada pelos validadores existentes.

#### Scenario: URLs próprias já definidas
- **WHEN** operador inicia com URLs de grupos previamente configuradas
- **THEN** seus valores são preservados e o portal usa a configuração existente

#### Scenario: Inicialização com configuração padrão
- **WHEN** operador inicia sem URLs personalizadas
- **THEN** as seis configurações de grupos conhecidos são disponibilizadas sem login ou teste de rede automático do iniciador

### Requirement: Revisão visual distingue preview de validação remota
A revisão local MUST identificar dados fictícios e bloquear acesso ao Xano e
gravações reais. MUST cobrir as sete telas e estados de formulário, vazio,
erro, desabilitado e incerteza aplicáveis; teste de estado MUST NOT substituir
inspeção de aparência no navegador nem ser apresentado como nova homologação remota.

#### Scenario: Preview offline
- **WHEN** responsável abre a prévia para revisar as telas
- **THEN** vê a identificação fictícia e pode avaliar aparência sem alterar dados remotos
