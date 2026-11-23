# Proposal

## Why

Clientes aplica identidade visual própria, enquanto login e demais telas usam
o padrão nativo, tornando a navegação inconsistente. O iniciador também deixa
três URLs de módulos sem configuração; esses pontos precisam ser concluídos
para a demonstração do MVP em 21/11/2026.

## What Changes

- Aplicar identidade visual comum a login, Clientes, Equipamentos, Técnicos,
  OS, Serviços e painel técnico, preservando Streamlit e a paleta existente.
- Uniformizar cabeçalhos, navegação permitida por perfil, formulários, tabelas,
  feedback e distinção visual de ações destrutivas, sem mudar fluxo de negócio.
- Revisar largura pequena, contraste, foco visível e estados desabilitados.
- Completar configuração das seis URLs no iniciador local, preservando valores
  fornecidos pelo ambiente e sem incluir credenciais ou habilitar DELETE pendente.
- Testar regressões locais afetadas e revisar as sete telas no navegador com
  dados fictícios e transporte isolado, sem chamadas ao Xano.

## Capabilities

### New Capabilities

- `apresentacao-streamlit`: apresentação e navegação visual consistentes das
  telas existentes, com legibilidade e preservação de estados/contratos.

### Modified Capabilities

Nenhuma: os requisitos de configuração, cadastro e edição de Clientes e de
gestão de Serviços permanecem; a configuração continua externa e validada.
Não alterar specs principais nem encerrar homologações pendentes do backend.

## Impact

frontend/styles.css, portal.py, clientes_page.py, login_page.py, módulos *_ui.py
e eventualmente wrappers de páginas; componente comum de apresentação;
configuração de tema Streamlit, iniciar-local.cmd, testes e README de execução.
Sem alterações em clientes HTTP, autenticação, payloads, backend ou domínio.
Sem dashboard, gráficos, novos cadastros, novas dependências ou recursos externos.

Usar marinho #17365D, azul #2563EB e fundo #F8FAFC como base; verde de sucesso
e vermelho destrutivo com contraste verificado, sem depender apenas de cor.
Manter seletores, chaves de widget/estado, confirmação, bloqueios incertos,
guardas e quantidade de requests dos fluxos aprovados. Preview usa dados
fictícios claramente identificados; não substitui teste real de backend.

Planejamento local apenas; contador 375 preservado. Aplicação, testes e revisão
visual virão em etapa autorizada própria, sem publicação ou Git implícitos.
