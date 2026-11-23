# login-erp-visual Specification

## Purpose

Oferecer uma apresentação corporativa responsiva no login, preservando os widgets reais e todo o comportamento de acesso existente.

## Requirements

### Requirement: Login corporativo exclusivamente visual
O sistema SHALL apresentar login em duas áreas no desktop, com marca e ilustração local à esquerda e os widgets Streamlit existentes à direita, preservando integralmente o comportamento anterior.

#### Scenario: Acesso em desktop
- **WHEN** o login é exibido em 1440 px
- **THEN** as duas áreas são apresentadas lado a lado e o botão Entrar permanece um widget real

#### Scenario: Acesso móvel
- **WHEN** o login é exibido em 390 px
- **THEN** as áreas são empilhadas sem rolagem horizontal, com foco visível por teclado e controles de pelo menos 44 px

#### Scenario: Configuração indisponível
- **WHEN** a configuração de autenticação está ausente
- **THEN** o botão permanece desabilitado e o aviso original é preservado

#### Scenario: Isolamento visual
- **WHEN** a raiz do login não está presente
- **THEN** os novos seletores de CSS não se aplicam às demais páginas
