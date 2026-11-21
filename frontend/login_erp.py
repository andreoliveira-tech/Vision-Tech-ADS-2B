"""Somente composição do login, sem sessão, configuração ou chamadas HTTP."""
from base64 import b64encode
from contextlib import contextmanager
from pathlib import Path
import streamlit as st


@contextmanager
def layout_login():
    directory = Path(__file__).parent
    css = (directory / 'login_erp.css').read_text(encoding='utf-8')
    image = b64encode((directory / 'assets/login-bancada.svg').read_bytes()).decode('ascii')
    st.markdown('<style>' + css + '</style>', unsafe_allow_html=True)
    with st.container(key='at_erp_login'):
        left, right = st.columns([1, 1], gap='small')
        with left:
            with st.container(key='at_erp_brand'):
                st.markdown(
                    '<section class="at-erp-story" aria-label="Apresentação do sistema">'
                    '<div class="at-erp-brand"><span class="at-erp-mark">AT</span>'
                    '<div>ASSISTÊNCIA TÉCNICA<span>GESTÃO DE ATENDIMENTOS</span></div></div>'
                    '<div class="at-erp-message"><span class="at-erp-eyebrow">ORGANIZAÇÃO EM CADA ETAPA</span>'
                    '<h2>Seu atendimento. <br>Sua equipe. <br>Tudo conectado.</h2>'
                    '<p>Do primeiro contato à conclusão do serviço, <br>uma visão clara de cada atendimento.</p></div>'
                    f'<img class="at-erp-art" src="data:image/svg+xml;base64,{image}" '
                    'alt="Ilustração de uma bancada de assistência técnica com notebook, monitor e ferramentas">'
                    '<ul class="at-erp-modules" aria-label="Módulos do sistema">'
                    '<li><span aria-hidden="true">01</span> Clientes</li>'
                    '<li><span aria-hidden="true">02</span> Equipamentos</li>'
                    '<li><span aria-hidden="true">03</span> Ordens de Serviço</li>'
                    '<li><span aria-hidden="true">04</span> Serviços</li>'
                    '<li><span aria-hidden="true">05</span> Técnicos</li></ul>'
                    '<p class="at-erp-footnote">Tecnologia para organizar. Clareza para atender.</p></section>',
                    unsafe_allow_html=True,
                )
        with right:
            with st.container(key='at_erp_access'):
                with st.container(key='at_erp_form'):
                    st.markdown(
                        '<div class="at-erp-welcome"><span class="at-erp-logo" aria-label="AT">AT</span>'
                        '<p class="at-erp-system">Sistema de Assistência Técnica</p>'
                        '<h2>Acesse o sistema</h2>'
                        '<p>Entre com sua conta para continuar.</p></div>',
                        unsafe_allow_html=True,
                    )
                    yield
