# Design

## Context

Ver proposal.md. portal.py já usa st.navigation filtrada pelo perfil e revalida
auth/me nas sessões autenticadas; não alterar esse fluxo. clientes_page.py
injeta styles.css e inclui marca/âncoras próprias na sidebar. As demais telas
usam widgets Streamlit nativos sem aplicação comum do tema. O iniciador define
somente Authentication, Clientes e Técnicos e sobrescreve valores externos.
config.py já oferece seis loaders HTTPS e opt-in separado de DELETE Equipamentos.

Design necessário porque a apresentação é transversal a páginas com estado e
autorização. A prévia anterior usou componentes reais e dados fictícios; ela
não é sessão autenticada real nem evidência de backend novo.

## Goals / Non-Goals

**Goals:** tema claro e navegação visual consistentes, reutilizando componentes
nativos e CSS local pequeno; configuração completa e preservação dos fluxos.

**Non-Goals:** clientes HTTP, auth_session, modelo de domínio, autenticação,
payloads, cálculos, novas funcionalidades, backend, publicação, novos serviços
externos ou ativação dos DELETEs ainda não homologados.

## Decisions

### Tema compartilhado com componentes nativos

Adicionar componente local de apresentação (frontend/apresentacao.py) e tema
em .streamlit/config.toml na raiz. Aplicar estilo no portal após set_page_config
e disponibilizar o componente às entradas diretas necessárias, sem duplicar
marca/menu ou usar flag persistente que omita CSS após rerun. Reutilizar
styles.css, retirar sua injeção exclusiva de Clientes e manter âncoras locais
quando úteis, separadas da navegação entre módulos do portal.

Preferir configuração/atributos suportados pelo Streamlit a seletores de DOM.
Onde CSS for necessário, limitar seletores ao contexto e testar versão instalada
no navegador; não introduzir JS ou bibliotecas para redesenhar widgets. Preservar
labels/keys usados pelos testes e não mover campos para dentro/fora de forms.

Alternativa de copiar CSS em cada página foi descartada pela duplicação e risco
de divergência. Não substituir a navegação por HTML que contorne os perfis.

### Paleta e layout

Base atual: marinho #17365D, azul #2563EB, fundo #F8FAFC, superfícies brancas,
texto escuro. Sucesso pode usar fundo #F0FDF4/texto #166534; verde #16A34A fica
como acento quando necessário. Destrutivo pode usar #B91C1C com texto claro,
sempre acompanhado de rótulo explícito e confirmação original. Medir contraste
dos pares efetivamente usados; não colocar texto branco sobre verde sem medir.

Manter hierarquia de títulos e espaços consistentes, largura confortável de
formulários/tabelas e rolagem local de tabelas largas. Em 390 px, reduzir margens
e permitir empilhamento nativo das colunas. Não ocultar mensagens ou controles
para simular responsividade. Aplicar foco visível a teclado e respeitar estados
disabled, sem CSS que faça ação indisponível parecer ativa.

Mensagens vazias, erro, carregamento e incerteza mantêm texto e significado.
Apresentação de carregamento apenas envolve operações já existentes; não
adicionar auto-refresh, polling, callbacks, reautenticação ou reenvios.

### Configuração do iniciador

Manter entrypoint atual e execução a partir da raiz, com ambiente .venv existente.
Usar defaults somente quando cada variável estiver ausente; completar URLs de
Equipamentos, OS e Serviços com os grupos já documentados/publicados. Não gravar
segredos, instalar pacotes, acessar Xano para conferir URLs ou atribuir valor à
flag XANO_EQUIPAMENTOS_DELETE_VALIDATED. URLs personalizadas inválidas não são
substituídas silenciosamente: o validador existente continua responsável por
rejeitar e orientar. Documentar execução e precedência em frontend/README.md.

### Verificação sem remotos

Testar componente e contratos afetados com AppTest, HTTP simulado e sockets
externos bloqueados. Congelar antes/depois inputs, keys, payloads, estados e
quantidade de chamadas dos caminhos afetados; não ajustar testes para aceitar
reenvio ou perda de confirmação. Reutilizar regressões aprovadas, repetindo
somente as relevantes para arquivos modificados.

Prévia local usa telas reais, dados fictícios identificados e bloqueio de rede
e gravações. Revisar sete telas em 1440 e 390 px, capturando screenshots,
incluindo rolagem até ações inferiores e estados negativos aplicáveis. Roteiro
de teclado/foco, contraste e clipping registrado; AppTest não comprova aparência.
Não abrir portal real autenticado para essa revisão, pois auth/me usa a rede.

## Risks / Trade-offs

- CSS pode depender de DOM Streamlit → preferir tema nativo e conferir navegador
  na versão instalada, sem mudanças de dependência nesta Change.
- Centralização pode duplicar navegação de Clientes → manter menu principal no
  portal e contextualizar âncoras sem duplicar marca global.
- Alteração visual pode afetar estado/confirmação → preservar chaves/estrutura
  dos forms e verificar regressões negativas sem rede.
- Preview pode parecer homologação remota → banner fictício e relatório de
  limite; não alterar contador nem encerrar pendências do backend.

## Migration Plan

Após aprovação, aplicar localmente tema/componente e integração das telas,
depois iniciador e documentação com testes por etapa. Revisar navegador offline
e apresentar resultado para aceite. Sem publicação ou Git. Reversão local deve
abranger somente os arquivos desta Change, preservando alterações anteriores;
não usar reset global nem mexer nas evidências históricas.
