"""Apresentação local compartilhada; não lê sessão nem executa HTTP."""
from pathlib import Path
from html import escape
import streamlit as st

STATUS_CORES = {
    'Aguardando avaliação': ('#713F12', '#FEF3C7'),
    'Em manutenção': ('#1E40AF', '#DBEAFE'),
    'Aguardando peça': ('#713F12', '#FEF3C7'),
    'Concluído': ('#166534', '#DCFCE7'),
    'Entregue': ('#334155', '#E2E8F0'),
}


def status_rotulo(valor):
    return 'Concluída' if valor == 'Concluído' else valor


def badge_status(valor):
    frente, fundo = STATUS_CORES.get(valor, ('#334155', '#E2E8F0'))
    return f'<span class="os-badge" style="color:{frente};background:{fundo}">{escape(str(status_rotulo(valor)))}</span>'


def filtrar_ordens(ordens, status='Todos', tecnico='Todos', busca=''):
    busca = busca.strip().casefold()
    return [o for o in ordens if (status == 'Todos' or o['status'] == status)
            and (tecnico == 'Todos' or o['id_tecnico'] == tecnico)
            and (not busca or busca in f"{o['id_os']} {o['id_equipamento']} {o['problema_relatado']}".casefold())]


def indicadores_ordens(ordens):
    itens = [('Total de OS', len(ordens), '#334155'),
             ('Aguardando avaliação', sum(o['status'] == 'Aguardando avaliação' for o in ordens), '#713F12'),
             ('Em manutenção', sum(o['status'] == 'Em manutenção' for o in ordens), '#1E40AF'),
             ('Concluídas', sum(o['status'] == 'Concluído' for o in ordens), '#166534')]
    st.markdown('<div class="os-kpis">'+''.join(
        f'<div class="os-kpi"><span><i style="background:{cor}"></i>{nome}</span><strong>{total}</strong></div>'
        for nome, total, cor in itens)+'</div>', unsafe_allow_html=True)


def destaque_status(chave_cartao, atual, valores):
    # Apenas aparência: não retira widgets do form nem comunica alterações ao Python.
    seletores = [f'.st-key-{chave_cartao}:has(input[aria-label="Atualizar status"][value="{status_rotulo(v)}"][aria-expanded="false"]) [data-testid=stFormSubmitButton] button'
                 for v in valores if v != atual]
    st.markdown('<style>'+','.join(seletores)+'{background:#2563EB!important;border-color:#2563EB!important;color:white!important;}'
                +','.join(s+' p' for s in seletores)+'{color:white!important;}</style>', unsafe_allow_html=True)


def aplicar_tema():
    # Reaplicar em cada execução: nenhuma flag persistente esconde o CSS em rerun.
    css = Path(__file__).with_name('styles.css').read_text(encoding='utf-8')
    st.markdown('<style>'+css+'</style>', unsafe_allow_html=True)


def marca():
    st.sidebar.markdown(
        '<div class="system-brand"><div class="brand-symbol">AT</div>'
        '<div><strong>Assistência Técnica</strong><span>Gestão de atendimento</span></div></div>',
        unsafe_allow_html=True)


def botao_destrutivo(rotulo, **kwargs):
    # Mantém label, key, disabled e retorno do botão; somente agrupa o estilo.
    with st.container(key='acao_destrutiva'):
        return st.button(rotulo, **kwargs)
