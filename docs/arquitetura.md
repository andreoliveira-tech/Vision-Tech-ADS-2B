# Arquitetura do Sistema de Assistência Técnica

## Objetivo

Organizar os atendimentos de uma única assistência técnica por meio dos módulos Clientes, Equipamentos, Técnicos, Ordens de Serviço e Serviços. O painel Minhas Ordens atende ao perfil Técnico.

Este documento descreve o código e os contratos locais disponíveis. Sua leitura não representa nova verificação do backend remoto.

## Tecnologias

| Tecnologia | Responsabilidade |
| --- | --- |
| Python | Implementação da aplicação e integração HTTP |
| Streamlit | Interface, formulários, navegação e estado da sessão |
| Requests | Comunicação HTTP com as APIs |
| Xano | Backend privado: autenticação, autorização, APIs e persistência |
| XanoScript | Representação das definições do backend no projeto de origem |
| Git e GitHub | Controle de versão e compartilhamento |
| OpenSpec | Organização das especificações e do desenvolvimento incremental |

## Comunicação entre as partes

```text
Navegador
    |
    v
Aplicação Streamlit / Python
    |
    | APIs HTTPS
    v
Backend Xano
    |
    v
Persistência no Xano
```

O navegador apresenta a interface Streamlit. O código Python envia as requisições ao Xano e interpreta as respostas. O frontend não acessa diretamente o banco de dados.

## Entrada e organização do frontend

O comando de execução está no [README](../README.md). O ponto de entrada é `frontend/Clientes.py`, que executa `portal.py` e abre o portal completo, apesar do nome do arquivo de entrada.

| Arquivos | Responsabilidade |
| --- | --- |
| `Clientes.py` e `portal.py` | Inicialização e navegação conforme o perfil |
| `login_page.py`, `login_erp.py` e `login_erp.css` | Formulário real e apresentação do login |
| `clientes_page.py`, `pages/` e arquivos `*_ui.py` | Telas e ações explícitas do usuário |
| Arquivos `*_api.py` | Envio HTTP, tratamento de erros e interpretação dos contratos |
| `config.py` | Leitura e validação da configuração externa |
| `auth_session.py` | Estado da sessão e exigência de perfil na interface |
| `apresentacao.py`, `styles.css` e `assets/` | Apresentação compartilhada e recurso visual local |

As regras de autorização e os dados pertencem ao backend privado. Ocultar uma página no frontend não substitui autorização no servidor.

## Configuração externa

A execução real exige os endereços HTTPS legítimos dos grupos de Autenticação, Clientes, Equipamentos, Técnicos, Ordens de Serviço e Serviços. Os nomes das seis variáveis estão no README; valores privados não são distribuídos.

O aplicativo lê variáveis do processo e não carrega arquivos `.env` automaticamente. A configuração visual fica em `.streamlit/config.toml`, separada dos endereços das APIs.

A exclusão de Equipamentos depende também de `XANO_EQUIPAMENTOS_DELETE_VALIDATED=true`. Sem essa configuração explícita, o controle de exclusão não é habilitado. Não ativar em outro backend sem a verificação correspondente.

## Autenticação e perfis

O formulário envia as credenciais ao serviço de autenticação configurado. O token retornado é mantido no estado da sessão Streamlit e enviado como Bearer nas chamadas protegidas; nenhum valor de token integra esta documentação.

O portal consulta a identidade autenticada antes de liberar a navegação em uma sessão existente. O comando Sair limpa o estado local; isso não significa revogação do token no servidor.

| Perfil | Permissões previstas nos contratos e fontes locais |
| --- | --- |
| Colaborador | Gestão dos cinco módulos, respeitando as operações indisponíveis |
| Técnico | Consulta somente das OS atribuídas e atualização do status dessas OS |
| Sem perfil funcional válido | Sem acesso administrativo |

A identidade do Técnico precisa estar vinculada a um cadastro de Técnico válido. O vínculo não é definido livremente pelo usuário no painel.

Esses controles são coerentes com os resultados anteriormente documentados no projeto de origem. A presença de controles no frontend não comprova proteção integral, nem este documento substitui verificações do backend. Permanecem verificações adicionais de segurança pendentes.

## Dependências e limites da distribuição

- O arquivo `frontend/requirements.txt` declara Streamlit e Requests em intervalos de versões.
- A tabela de OS utiliza Pandas, disponível como dependência transitiva do Streamlit no ambiente documentado.
- O ambiente documentado utiliza Python 3.13 e Streamlit 1.66; a seleção não declara instalação limpa ou compatibilidade integral com todas as versões admitidas pelos intervalos.
- Esta pasta distribui somente uma seleção revisada do frontend e documentação pública, sem o histórico Git original.
- O backend, suas definições privadas, banco de dados, credenciais e registros reais não são distribuídos. Não é possível recriar o backend apenas com esta pasta.
- Não há versão pública implantada do aplicativo. O uso real exige configuração legítima, conectividade e conta autorizada.
- Exclusões de OS e Técnicos permanecem indisponíveis por segurança, mesmo havendo controles preparados na interface.
- As imagens aprovadas do login pertencem à prévia isolada e não comprovam uma sessão integrada.

Consulte o [modelo de domínio](modelo-dominio.md) e o README para as funcionalidades e limitações.
