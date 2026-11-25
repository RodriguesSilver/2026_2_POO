import pandas as pd
import streamlit as st
from view import View


class ManterClienteUI:
    @staticmethod
    def Main() -> None:
        st.header("Manter Cadastro de Clientes")
        aba = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])

        with aba[0]:
            ManterClienteUI.Listar()
        with aba[1]:
            ManterClienteUI.Inserir()
        with aba[2]:
            ManterClienteUI.Atualizar()
        with aba[3]:
            ManterClienteUI.Excluir()

    @staticmethod
    def Listar() -> None:
        clientes = View.cliente_listar()
        if not clientes:
            st.info("Nenhum cliente cadastrado.")
            return
        df = pd.DataFrame(
            [{"ID": c.id, "Nome": c.nome, "E-mail": c.email, "Telefone": c.fone} for c in clientes]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

    @staticmethod
    def Inserir() -> None:
        with st.form("form_cliente_inserir", clear_on_submit=True):
            nome = st.text_input("Nome")
            email = st.text_input("E-mail")
            fone = st.text_input("Telefone")
            submitted = st.form_submit_button("Inserir")

            if submitted:
                if not nome.strip():
                    st.error("Informe o nome do cliente.")
                    return
                cliente = View.cliente_inserir(nome, email, fone)
                st.success(f"Cliente '{cliente.nome}' (ID {cliente.id}) cadastrado com sucesso!")

    @staticmethod
    def Atualizar() -> None:
        clientes = View.cliente_listar()
        if not clientes:
            st.info("Nenhum cliente disponível para atualizar.")
            return

        selecionado = st.selectbox(
            "Selecione o cliente",
            options=clientes,
            format_func=lambda c: f"{c.id} - {c.nome}",
            key="upd_cliente_select",
        )
        if selecionado is None:
            return

        with st.form("form_cliente_atualizar"):
            nome = st.text_input("Nome", value=selecionado.nome)
            email = st.text_input("E-mail", value=selecionado.email)
            fone = st.text_input("Telefone", value=selecionado.fone)
            submitted = st.form_submit_button("Atualizar")

            if submitted:
                if not nome.strip():
                    st.error("O nome não pode ficar em branco.")
                    return
                if View.cliente_atualizar(selecionado.id, nome, email, fone):
                    st.success("Cliente atualizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Não foi possível atualizar o cliente.")

    @staticmethod
    def Excluir() -> None:
        clientes = View.cliente_listar()
        if not clientes:
            st.info("Nenhum cliente disponível para excluir.")
            return

        selecionado = st.selectbox(
            "Selecione o cliente para excluir",
            options=clientes,
            format_func=lambda c: f"{c.id} - {c.nome} ({c.email})",
            key="del_cliente_select",
        )
        if selecionado is None:
            return

        if st.button("Excluir Cliente", type="primary"):
            if View.cliente_excluir(selecionado.id):
                st.success("Cliente excluído com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao excluir cliente.")
