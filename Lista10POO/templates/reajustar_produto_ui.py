from typing import Optional
import pandas as pd
import streamlit as st
from models import Categoria
from view import View


class ReajustarProdutoUI:
    @staticmethod
    def Main() -> None:
        st.header("Reajustar Preço de Produtos")
        ReajustarProdutoUI.Reajustar()

    @staticmethod
    def Reajustar() -> None:
        produtos = View.produto_listar()
        if not produtos:
            st.info("Nenhum produto cadastrado para reajustar.")
            return

        categorias = View.categoria_listar()
        opcoes_cat: list[Optional[Categoria]] = [None] + categorias

        with st.form("form_reajustar_preco_l10"):
            percentual = st.number_input(
                "Percentual de reajuste (%) — use valores negativos para desconto",
                min_value=-99.0,
                max_value=1000.0,
                value=10.0,
                step=1.0,
                format="%.2f",
            )
            cat_filtro = st.selectbox(
                "Aplicar a qual escopo?",
                options=opcoes_cat,
                format_func=lambda c: "Todos os produtos" if c is None else f"Categoria: {c.descricao}",
            )
            submitted = st.form_submit_button("Aplicar Reajuste")

            if submitted:
                id_cat = cat_filtro.id if cat_filtro is not None else None
                qtd = View.produto_reajustar(percentual, id_cat)
                st.success(f"Reajuste de {percentual:+.2f}% aplicado a {qtd} produto(s)!")

        st.subheader("Tabela Atual de Produtos")
        df = pd.DataFrame(
            [
                {
                    "ID": p.id,
                    "Descrição": p.descricao,
                    "Preço Atual (R$)": f"{p.preco:.2f}",
                    "Estoque": p.estoque,
                }
                for p in View.produto_listar()
            ]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
