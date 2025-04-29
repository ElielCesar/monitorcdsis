import streamlit as st
import requests
from database import criar_tabela, adicionar_url, listar_urls, excluir_url
from time import sleep
from requests.exceptions import SSLError

st.set_page_config(page_title='Monitor CDSIS')

# Criar tabela se não existir
criar_tabela()

# Título da página
st.title('Monitor CDSIS')

# Input para adicionar nova URL
url = st.text_input('Digite a URL a ser monitorada: ')

if st.button('Adicionar URL'):

    if url:
        adicionar_url(url)
        placeholder = st.empty()
        with placeholder:
            st.success('URL adiconado com sucesso!', icon="✅")
        sleep(1)
        placeholder.empty()

    else:
        placeholder = st.empty()
        with placeholder:
            st.error('Por favor, digite uma URL válida', icon="🚨")
        sleep(2)
        placeholder.empty()


# linha divisória horizontal simples
st.divider()

# traz do banco de dados, as urls cadastradas -> tupla (id, url)
dados = listar_urls()


# Teste coletivo de URLs
if st.button('Testar todas'):
    for (id, url) in dados:
        try:
            resposta = requests.get(url, timeout=7)

            if resposta.status_code != 200:
                st.info(f'{url} offline', icon="🚨")

            else:
                st.success(f'{url} online ✅')

        except SSLError:
            st.warning(f'{url} possui erro de certificado SSL ❌', icon="🔒")

        except ConnectionError:
            st.error(f'{url} está indisponível ou incorreta (erro de conexão) 🔌', icon="📡")

    sleep(5)
    st.rerun()

st.write("### Lista de serviços monitorados")


# Criar o cabeçalho da tabela
col1, col2, col3, col4 = st.columns([1, 5, 1, 1, ])

with col1:
    st.write("**Testar**")
with col2:
    st.write("**URL**")
with col3:
    st.write("**Status**")
with col4:
    st.write("**Excluir**")


# Teste individual de URLs
if dados:

    for (id, url) in dados:
        col1, col2, col3, col4 = st.columns([1, 5, 1, 1,])

        with col1:
            if st.button('Testar', key=f'testar_{id}'):
                try:
                    resposta = requests.get(url, timeout=5)
                    if resposta.status_code == 200:
                        st.session_state[f"status_{id}"] = "✅ Online"
                    else:
                        st.session_state[f"status_{id}"] = "❌ Offline"
                except:
                    st.session_state[f"status_{id}"] = "❌ Offline"

        with col2:
            nova_url = st.write(f'{url}', value=url, key=f"url_{id}")

        with col3:
            st.write(st.session_state.get(f"status_{id}", "..."))

        with col4:
            if st.button("🗑️", key=f"excluir_{id}"):
                excluir_url(id)
                st.rerun()

else:
    st.info('Nenhuma URL cadastrada ainda!', icon="🚨")
