# Design — Proteção dos endpoints de Clientes

## Context

Consultar [a proposta](proposal.md). A arquitetura permanece Streamlit/Python → APIs Xano. Este documento registra retrospectivamente decisões já implementadas; não instrui nova publicação.

## Goals / Non-Goals

Garantir autorização antes de acessar dados de Clientes e preservar os contratos existentes. Não alterar o domínio, outros módulos, permissões remotas ou flags de exclusão; não ampliar a comprovação para concorrência e rollback.

## Decisions

1. **Autorização no backend:** as cinco rotas exigem autenticação Xano e consulta do perfil funcional antes da lógica de dados. Ocultar uma tela ou confiar no papel legado não substitui esse controle.
2. **Token da sessão no frontend:** o cliente HTTP envia Bearer nas operações e nas consultas de confirmação. Token ausente impede envio; 401 encerra sessão/cache e 403 interrompe o acesso. Falha de confirmação não anuncia sucesso nem repete uma escrita automaticamente.
3. **Publicação seletiva já realizada:** foram atualizados somente os cinco endpoints existentes, preservando contratos e demais definições, conforme os relatórios abaixo. Recriar recursos ou substituir outros módulos não fazia parte do escopo.
4. **Preservação das regras:** validação de Cliente e bloqueio por Equipamentos permanecem aplicáveis. Este encerramento não transforma controles sequenciais em garantia de integridade concorrente.

## Risks / Trade-offs

- Uma verificação frontend isolada não comprova segurança do backend → apoiar a conclusão nos cenários remotos de autorização já registrados.
- Resultado de escrita incerto pode incentivar reenvio → interromper o fluxo sem repetição automática.
- Evidências têm alcance delimitado → não afirmar inspeção integral de eventos, concorrência, rollback ou conclusão de outros módulos.

## Evidências e encerramento

Referências a partir da raiz do projeto:

- `docs/preview-remoto-protecao-clientes.md`: seleção de cinco atualizações, sem criação ou exclusão.
- `docs/publicacao-protecao-clientes.md`: publicação e preservação das definições anteriores.
- `docs/homologacao-clientes-leitura-conclusao.md`: leitura autorizada e negações de acesso.
- `docs/homologacao-clientes-escrita-conclusao-20261119.md`: escrita autorizada, negações e integração da tela via AppTest com APIs reais; não corresponde a sessão manual de navegador. Registra expressamente a conclusão das nove tarefas.

Nenhum teste funcional ou acesso remoto foi repetido para preparar estes documentos. Não foi executada nova migração nem rollback; qualquer operação futura exige autorização própria.
