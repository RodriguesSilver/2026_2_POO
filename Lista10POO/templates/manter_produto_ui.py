from typing import Optional
import pandas as pd
import streamlit as st
from models import Categoria
from view import View


class ManterProdutoUI:
    @staticmethod
    def Main() -> None:
        st.header("Manter Cadastro de Produtos")
        aba = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])

        with aba[0]:
            ManterProdutoUI.Listar()
        with aba[1]:
            ManterProdutoUI.Inserir()
        with aba[2]:
            ManterProdutoUI.Atualizar()
        with aba[3]:
            ManterProdutoUI.Excluir()

    @staticmethod
    def _nome_categoria(id_categoria: Optional[int]) -> str:
        cat = View.categoria_listar_por_id(id_categoria)
        return cat.descricao if cat else "Sem categoria"

    @staticmethod
    def Listar() -> None:
        produtos = View.produto_listar()
        if not produtos:
            st.info("Nenhum produto cadastrado.")
            return

        df = pd.DataFrame(
            [
                {
                    "ID": p.id,
                    "Descrição": p.descricao,
                    "Preço (R$)": f"{p.preco:.2f}",
                    "Estoque": p.estoque,
                    "Categoria": ManterProdutoUI._nome_categoria(p.id_categoria),
                }
                for p in produtos
            ]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

    @staticmethod
    def Inserir() -> None:
        categorias = View.categoria_listar()
        opcoes_cat: list[Optional[Categoria]] = [None] + categorias

        with st.form("form_produto_inserir_l10", clear_on_submit=True):
            descricao = st.text_input("Descrição do produto")
            preco = st.number_input("Preço (R$)", min_value=0.0, step=0.50, format="%.2f")
            estoque = st.number_input("Estoque", min_value=0, step=1)
            cat_escolhida = st.selectbox(
                "Categoria",
                options=opcoes_cat,
                format_func=lambda c: "Sem categoria" if c is None else f"{c.id} - {c.descricao}",
            )
            submitted = st.form_submit_button("Inserir")

            if submitted:
                if not descricao.strip():
                    st.error("Informe a descrição do produto.")
                    return
                id_cat = cat_escolhida.id if cat_escolhida is not None else None
                prod = View.produto_inserir(descricao, preco, int(estoque), id_cat)
                st.success(f"Produto '{prod.descricao}' (ID {prod.id}) cadastrado!")

    @staticmethod
    def Atualizar() -> None:
        produtos = View.produto_listar()
        if not produtos:
            st.info("Nenhum produto disponível para atualizar.")
            return

        selecionado = st.selectbox(
            "Selecione o produto",
            options=produtos,
            format_func=lambda p: f"{p.id} - {p.descricao} (R$ {p.preco:.2f})",
            key="upd_prod_select_l10",
        )
        if selecionado is None:
            return

        categorias = View.categoria_listar()
        opcoes_cat: list[Optional[Categoria]] = [None] + categorias
        idx_cat = 0
        if selecionado.id_categoria is not None:
            for idx, c in enumerate(opcoes_cat):
                if c is not None and c.id == selecionado.id_categoria:
                    idx_cat = idx
                    break

        with st.form("form_produto_atualizar_l10"):
            descricao = st.text_input("Descrição", value=selecionado.descricao)
            preco = st.number_input(
                "Preço (R$)",
                min_value=0.0,
                step=0.50,
                value=float(selecionado.preco),
                format="%.2f",
            )
            estoque = st.number_input(
                "Estoque", min_value=0, step=1, value=int(selecionado.estoque)
            )
            cat_escolhida = st.selectbox(
                "Categoria",
                options=opcoes_cat,
                index=idx_cat,
                format_func=lambda c: "Sem categoria" if c is None else f"{c.id} - {c.descricao}",
            )
            submitted = st.form_submit_button("Atualizar")

            if submitted:
                if not descricao.strip():
                    st.error("A descrição não pode ficar em branco.")
                    return
                id_cat = cat_escolhida.id if cat_escolhida is not None else None
                if View.produto_atualizar(
                    selecionado.id, descricao, preco, int(estoque), id_cat
                ):
                    st.success("Produto atualizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao atualizar produto.")

    @staticmethod
    def Excluir() -> None:
        produtos = View.produto_listar()
        if not produtos:
            st.info("Nenhum produto disponível para excluir.")
            return

        selecionado = st.selectbox(
            "Selecione o produto para excluir",
            options=produtos,
            format_func=lambda p: f"{p.id} - {p.descricao} (R$ {p.preco:.2f})",
            key="del_prod_select_l10",
        )
        if selecionado is None:
            return

        if st.button("Excluir Produto", type="primary", key="btn_del_prod_l10"):
            if View.produto_excluir(selecionado.id):
                st.success("Produto excluído com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao excluir produto.")
