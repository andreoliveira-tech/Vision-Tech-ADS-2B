## Context

O login existente usa Streamlit e deve manter rótulos, chaves, tipos, disabled, retornos e fluxo Python. Não há autorização para chamadas remotas.

## Goals / Non-Goals

Implementar composição visual corporativa e responsividade em 390 px. Não implementar recuperação de senha, novos controles, novos perfis ou alterações funcionais.

## Decisions

Manter o corpo original de render dentro de um contexto exclusivamente visual. Usar colunas e containers Streamlit; HTML apenas para marca, ilustração e texto estático. CSS condicionado à presença da raiz do login, sem alterações nos estilos globais existentes. SVG incorporado localmente, sem dependência externa. Prévia isolada com configuração fictícia e transporte HTTP bloqueado.

## Risks / Trade-offs

Seletores de estrutura Streamlit dependem da versão instalada. Capturas reais validam a versão disponível; futuras atualizações exigem revisão visual. Em celular há rolagem vertical para as duas áreas. Aceite visual é independente dos testes locais.

## Migration Plan

Backup externo verificado antes da alteração. Reversão limitada ao arquivo login_page.py e aos arquivos novos desta entrega; preservar demais alterações preexistentes.
