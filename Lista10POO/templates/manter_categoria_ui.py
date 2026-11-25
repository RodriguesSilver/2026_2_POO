import pandas as pd
import streamlit as st
from view import View


class ManterCategoriaUI:
    @staticmethod
    def Main() -> None:
        st.header("Manter Cadastro de Categorias")
        aba = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])

        with aba[0]:
            ManterCategoriaUI.Listar()
        with aba[1]:
            ManterCategoriaUI.Inserir()
        with aba[2]:
            ManterCategoriaUI.Atualizar()
        with aba[3]:
            ManterCategoriaUI.Excluir()

    @staticmethod
    def Listar() -> None:
        categorias = View.categoria_listar()
        if not categorias:
            st.info("Nenhuma categoria cadastrada.")
            return
        df = pd.DataFrame([{"ID": c.id, "Descrição": c.descricao} for c in categorias])
        st.dataframe(df, use_container_width=True, hide_index=True)

    @staticmethod
    def Inserir() -> None:
        with st.form("form_categoria_inserir_l10", clear_on_submit=True):
            descricao = st.text_input("Descrição da categoria")
            submitted = st.form_submit_button("Inserir")

            if submitted:
                if not descricao.strip():
                    st.error("Informe a descrição da categoria.")
                    return
                cat = View.categoria_inserir(descricao)
                st.success(f"Categoria '{cat.descricao}' (ID {cat.id}) cadastrada!")

    @staticmethod
    def Atualizar() -> None:
        categorias = View.categoria_listar()
        if not categorias:
            st.info("Nenhuma categoria disponível para atualizar.")
            return

        selecionada = st.selectbox(
            "Selecione a categoria",
            options=categorias,
            format_func=lambda c: f"{c.id} - {c.descricao}",
            key="upd_cat_select_l10",
        )
        if selecionada is None:
            return

        with st.form("form_categoria_atualizar_l10"):
            descricao = st.text_input("Descrição", value=selecionada.descricao)
            submitted = st.form_submit_button("Atualizar")

            if submitted:
                if not descricao.strip():
                    st.error("A descrição não pode ficar em branco.")
                    return
                if View.categoria_atualizar(selecionada.id, descricao):
                    st.success("Categoria atualizada com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao atualizar categoria.")

    @staticmethod
    def Excluir() -> None:
        categorias = View.categoria_listar()
        if not categorias:
            st.info("Nenhuma categoria disponível para excluir.")
            return

        selecionada = st.selectbox(
            "Selecione a categoria para excluir",
            options=categorias,
            format_func=lambda c: f"{c.id} - {c.descricao}",
            key="del_cat_select_l10",
        )
        if selecionada is None:
            return

        if st.button("Excluir Categoria", type="primary", key="btn_del_cat_l10"):
            if View.categoria_excluir(selecionada.id):
                st.success("Categoria excluída com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao excluir categoria.")
