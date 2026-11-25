import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from templates.manter_categoria_ui import ManterCategoriaUI
from templates.manter_cliente_ui import ManterClienteUI
from templates.manter_produto_ui import ManterProdutoUI
from templates.reajustar_produto_ui import ReajustarProdutoUI
from view import View


class IndexUI:
    @staticmethod
    def Main() -> None:
        st.set_page_config(
            page_title="Comércio Eletrônico — POO Lista 09",
            page_icon="🛒",
            layout="wide",
        )
        View._garantir_estado()

        st.sidebar.title("Menu — Admin")
        opcao = st.sidebar.radio(
            "Selecione uma funcionalidade:",
            options=[
                "Início",
                "Manter Clientes",
                "Manter Categorias",
                "Manter Produtos",
                "Reajustar Preços",
            ],
        )

        if opcao == "Início":
            st.title("Sistema de Comércio Eletrônico")
            st.caption("Lista 09 — Programação Orientada a Objetos (Streamlit)")
            st.markdown(
                """
                Utilize o menu lateral para acessar os casos de uso do **Admin**:
                - **Manter Clientes**: listar, inserir, atualizar e excluir clientes.
                - **Manter Categorias**: listar, inserir, atualizar e excluir categorias.
                - **Manter Produtos**: listar, inserir, atualizar e excluir produtos.
                - **Reajustar Preços**: aplicar reajuste percentual geral ou por categoria.
                """
            )
        elif opcao == "Manter Clientes":
            ManterClienteUI.Main()
        elif opcao == "Manter Categorias":
            ManterCategoriaUI.Main()
        elif opcao == "Manter Produtos":
            ManterProdutoUI.Main()
        elif opcao == "Reajustar Preços":
            ReajustarProdutoUI.Main()


if __name__ == "__main__":
    IndexUI.Main()
