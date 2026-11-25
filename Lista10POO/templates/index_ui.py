import sys
from pathlib import Path
import pandas as pd
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
    def _abrir_conta_ui() -> None:
        st.header("Abrir Conta")
        st.caption("Cadastre-se como cliente para acessar a loja e realizar compras.")
        with st.form("form_abrir_conta", clear_on_submit=True):
            nome = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            fone = st.text_input("Telefone")
            senha = st.text_input("Senha", value="1234", type="password")
            submitted = st.form_submit_button("Criar Conta")

            if submitted:
                ok, msg = View.abrir_conta(nome, email, fone, senha)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    @staticmethod
    def _entrar_ui() -> None:
        st.header("Entrar no Sistema")
        st.caption("Use o e-mail 'admin' para acessar como Admin ou o e-mail de um cliente.")
        with st.form("form_entrar_sistema"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha (opcional para clientes de teste)", type="password")
            submitted = st.form_submit_button("Entrar")

            if submitted:
                ok, msg = View.entrar(email, senha)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    @staticmethod
    def _listar_produtos_cliente_ui() -> None:
        st.header("Produtos Disponíveis")
        produtos = View.produto_listar()
        if not produtos:
            st.info("Nenhum produto cadastrado no momento.")
            return

        df = pd.DataFrame(
            [
                {
                    "ID": p.id,
                    "Descrição": p.descricao,
                    "Preço (R$)": f"{p.preco:.2f}",
                    "Estoque": p.estoque,
                    "Categoria": (
                        View.categoria_listar_por_id(p.id_categoria).descricao
                        if View.categoria_listar_por_id(p.id_categoria)
                        else "Sem categoria"
                    ),
                }
                for p in produtos
            ]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

    @staticmethod
    def _inserir_produto_carrinho_ui(cliente_id: int) -> None:
        st.header("Inserir Produto no Carrinho")
        produtos = [p for p in View.produto_listar() if p.estoque > 0]
        if not produtos:
            st.warning("Não há produtos com estoque disponível.")
            return

        with st.form("form_add_carrinho"):
            produto_sel = st.selectbox(
                "Escolha o produto",
                options=produtos,
                format_func=lambda p: f"{p.id} - {p.descricao} | R$ {p.preco:.2f} (Estoque: {p.estoque})",
            )
            qtd = st.number_input("Quantidade", min_value=1, max_value=int(produto_sel.estoque), value=1, step=1)
            submitted = st.form_submit_button("Adicionar ao Carrinho")

            if submitted:
                ok, msg = View.carrinho_inserir_produto(cliente_id, produto_sel.id, int(qtd))
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    @staticmethod
    def _visualizar_carrinho_ui(cliente_id: int) -> None:
        st.header("Meu Carrinho")
        itens = View.carrinho_itens(cliente_id)
        if not itens:
            st.info("Seu carrinho está vazio.")
            return

        df = pd.DataFrame(
            [
                {
                    "Produto": prod.descricao,
                    "Preço Unit. (R$)": f"{item.preco:.2f}",
                    "Qtd": item.qtd,
                    "Subtotal (R$)": f"{item.subtotal:.2f}",
                }
                for item, prod in itens
            ]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        total = sum(item.subtotal for item, _ in itens)
        st.subheader(f"Total do Carrinho: R$ {total:.2f}")

        if st.button("Limpar Carrinho", key="btn_limpar_carrinho"):
            View.carrinho_limpar(cliente_id)
            st.success("Carrinho limpo!")
            st.rerun()

    @staticmethod
    def _comprar_carrinho_ui(cliente_id: int) -> None:
        st.header("Confirmar Compra do Carrinho")
        itens = View.carrinho_itens(cliente_id)
        if not itens:
            st.info("Adicione itens ao carrinho antes de confirmar a compra.")
            return

        total = sum(item.subtotal for item, _ in itens)
        for item, prod in itens:
            st.write(f"- **{prod.descricao}**: {item.qtd}x de R$ {item.preco:.2f} = **R$ {item.subtotal:.2f}**")

        st.subheader(f"Total a Pagar: R$ {total:.2f}")
        if st.button("Confirmar Compra", type="primary", key="btn_confirmar_compra"):
            ok, msg = View.carrinho_comprar(cliente_id)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    @staticmethod
    def _listar_minhas_compras_ui(cliente_id: int) -> None:
        st.header("Minhas Compras")
        compras = View.venda_listar_compras_cliente(cliente_id)
        if not compras:
            st.info("Você ainda não concluiu nenhuma compra.")
            return

        for venda in compras:
            with st.expander(
                f"Compra #{venda.id} — {venda.data.strftime('%d/%m/%Y %H:%M')} — Total: R$ {venda.total:.2f}"
            ):
                itens = View.venda_itens_por_venda(venda.id)
                for item, prod in itens:
                    nome_prod = prod.descricao if prod else f"Produto #{item.id_produto}"
                    st.write(f"- {nome_prod}: {item.qtd}x R$ {item.preco:.2f} = R$ {item.subtotal:.2f}")

    @staticmethod
    def _listar_vendas_admin_ui() -> None:
        st.header("Todas as Vendas Realizadas")
        vendas = View.venda_listar_todas()
        if not vendas:
            st.info("Nenhuma venda concluída até o momento.")
            return

        for venda in vendas:
            cli = View.cliente_listar_por_id(venda.id_cliente) if venda.id_cliente else None
            nome_cli = cli.nome if cli else f"Cliente #{venda.id_cliente}"
            with st.expander(
                f"Venda #{venda.id} | Cliente: {nome_cli} | {venda.data.strftime('%d/%m/%Y %H:%M')} | Total: R$ {venda.total:.2f}"
            ):
                itens = View.venda_itens_por_venda(venda.id)
                for item, prod in itens:
                    nome_prod = prod.descricao if prod else f"Produto #{item.id_produto}"
                    st.write(f"- {nome_prod}: {item.qtd}x R$ {item.preco:.2f} = R$ {item.subtotal:.2f}")

    @staticmethod
    def Main() -> None:
        st.set_page_config(
            page_title="Comércio Eletrônico — POO Lista 10",
            page_icon="🛍️",
            layout="wide",
        )
        View._garantir_estado()

        perfil = View.get_perfil()
        usuario = View.get_usuario_logado()

        st.sidebar.title("Controle de Sessão")
        if usuario is not None:
            st.sidebar.success(f"Perfil: **{perfil}**\n\nUsuário: **{usuario.nome}** ({usuario.email})")
        else:
            st.sidebar.info(f"Perfil: **{perfil}**")

        if perfil == "Visitante":
            menu = st.sidebar.radio(
                "Menu do Visitante",
                options=["Entrar no sistema", "Abrir conta"],
            )
            if menu == "Entrar no sistema":
                IndexUI._entrar_ui()
            elif menu == "Abrir conta":
                IndexUI._abrir_conta_ui()

        elif perfil == "Admin":
            menu = st.sidebar.radio(
                "Menu do Admin",
                options=[
                    "Manter cadastro de categorias",
                    "Manter cadastro de produtos",
                    "Manter cadastro de clientes",
                    "Reajustar preço de produtos",
                    "Listar as vendas",
                    "Sair do sistema",
                ],
            )
            if menu == "Manter cadastro de categorias":
                ManterCategoriaUI.Main()
            elif menu == "Manter cadastro de produtos":
                ManterProdutoUI.Main()
            elif menu == "Manter cadastro de clientes":
                ManterClienteUI.Main()
            elif menu == "Reajustar preço de produtos":
                ReajustarProdutoUI.Main()
            elif menu == "Listar as vendas":
                IndexUI._listar_vendas_admin_ui()
            elif menu == "Sair do sistema":
                View.sair()
                st.rerun()

        elif perfil == "Cliente" and usuario is not None:
            menu = st.sidebar.radio(
                "Menu do Cliente",
                options=[
                    "Listar produtos",
                    "Inserir produto no carrinho",
                    "Visualizar o carrinho",
                    "Comprar o carrinho",
                    "Listar minhas compras",
                    "Sair do sistema",
                ],
            )
            if menu == "Listar produtos":
                IndexUI._listar_produtos_cliente_ui()
            elif menu == "Inserir produto no carrinho":
                IndexUI._inserir_produto_carrinho_ui(usuario.id)
            elif menu == "Visualizar o carrinho":
                IndexUI._visualizar_carrinho_ui(usuario.id)
            elif menu == "Comprar o carrinho":
                IndexUI._comprar_carrinho_ui(usuario.id)
            elif menu == "Listar minhas compras":
                IndexUI._listar_minhas_compras_ui(usuario.id)
            elif menu == "Sair do sistema":
                View.sair()
                st.rerun()


if __name__ == "__main__":
    IndexUI.Main()
