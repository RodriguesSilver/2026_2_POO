from typing import Dict, List, Optional
import streamlit as st

from models import (
    Categoria,
    CategoriaDAO,
    Cliente,
    ClienteDAO,
    Produto,
    ProdutoDAO,
    Venda,
    VendaDAO,
    VendaItem,
    VendaItemDAO,
)


class View:
    @staticmethod
    def _garantir_estado() -> Dict[str, Dict[int, object]]:
        if "db_ecommerce" not in st.session_state:
            st.session_state["db_ecommerce"] = {
                "clientes": {},
                "categorias": {},
                "produtos": {},
                "vendas": {},
                "venda_itens": {},
            }
            View.cliente_inserir("Ana Silva", "ana@email.com", "(84) 99999-1111")
            View.cliente_inserir("Bruno Costa", "bruno@email.com", "(84) 98888-2222")

            cat_elec = View.categoria_inserir("Eletrônicos")
            cat_livros = View.categoria_inserir("Livros")

            View.produto_inserir("Mouse Sem Fio", 79.90, 15, cat_elec.id)
            View.produto_inserir("Teclado Mecânico", 249.00, 8, cat_elec.id)
            View.produto_inserir("Python Fluente", 120.00, 12, cat_livros.id)

        return st.session_state["db_ecommerce"]

    @staticmethod
    def _daos():
        db = View._garantir_estado()
        return (
            ClienteDAO(db["clientes"]),
            CategoriaDAO(db["categorias"]),
            ProdutoDAO(db["produtos"]),
            VendaDAO(db["vendas"]),
            VendaItemDAO(db["venda_itens"]),
        )

    @staticmethod
    def cliente_listar() -> List[Cliente]:
        cliente_dao, _, _, _, _ = View._daos()
        return cliente_dao.listar()

    @staticmethod
    def cliente_listar_por_id(cliente_id: int) -> Optional[Cliente]:
        cliente_dao, _, _, _, _ = View._daos()
        return cliente_dao.listar_por_id(cliente_id)

    @staticmethod
    def cliente_inserir(nome: str, email: str, fone: str) -> Cliente:
        cliente_dao, _, _, _, _ = View._daos()
        cliente = Cliente(id=0, nome=nome.strip(), email=email.strip(), fone=fone.strip())
        return cliente_dao.inserir(cliente)

    @staticmethod
    def cliente_atualizar(cliente_id: int, nome: str, email: str, fone: str) -> bool:
        cliente_dao, _, _, _, _ = View._daos()
        cliente = Cliente(
            id=cliente_id, nome=nome.strip(), email=email.strip(), fone=fone.strip()
        )
        return cliente_dao.atualizar(cliente)

    @staticmethod
    def cliente_excluir(cliente_id: int) -> bool:
        cliente_dao, _, _, _, _ = View._daos()
        return cliente_dao.excluir(cliente_id)

    @staticmethod
    def categoria_listar() -> List[Categoria]:
        _, categoria_dao, _, _, _ = View._daos()
        return categoria_dao.listar()

    @staticmethod
    def categoria_listar_por_id(categoria_id: Optional[int]) -> Optional[Categoria]:
        if categoria_id is None:
            return None
        _, categoria_dao, _, _, _ = View._daos()
        return categoria_dao.listar_por_id(categoria_id)

    @staticmethod
    def categoria_inserir(descricao: str) -> Categoria:
        _, categoria_dao, _, _, _ = View._daos()
        categoria = Categoria(id=0, descricao=descricao.strip())
        return categoria_dao.inserir(categoria)

    @staticmethod
    def categoria_atualizar(categoria_id: int, descricao: str) -> bool:
        _, categoria_dao, _, _, _ = View._daos()
        categoria = Categoria(id=categoria_id, descricao=descricao.strip())
        return categoria_dao.atualizar(categoria)

    @staticmethod
    def categoria_excluir(categoria_id: int) -> bool:
        _, categoria_dao, produto_dao, _, _ = View._daos()
        for prod in produto_dao.listar():
            if prod.id_categoria == categoria_id:
                prod.id_categoria = None
                produto_dao.atualizar(prod)
        return categoria_dao.excluir(categoria_id)

    @staticmethod
    def produto_listar() -> List[Produto]:
        _, _, produto_dao, _, _ = View._daos()
        return produto_dao.listar()

    @staticmethod
    def produto_listar_por_id(produto_id: int) -> Optional[Produto]:
        _, _, produto_dao, _, _ = View._daos()
        return produto_dao.listar_por_id(produto_id)

    @staticmethod
    def produto_inserir(
        descricao: str, preco: float, estoque: int, id_categoria: Optional[int]
    ) -> Produto:
        _, _, produto_dao, _, _ = View._daos()
        produto = Produto(
            id=0,
            descricao=descricao.strip(),
            preco=float(preco),
            estoque=int(estoque),
            id_categoria=id_categoria,
        )
        return produto_dao.inserir(produto)

    @staticmethod
    def produto_atualizar(
        produto_id: int,
        descricao: str,
        preco: float,
        estoque: int,
        id_categoria: Optional[int],
    ) -> bool:
        _, _, produto_dao, _, _ = View._daos()
        produto = Produto(
            id=produto_id,
            descricao=descricao.strip(),
            preco=float(preco),
            estoque=int(estoque),
            id_categoria=id_categoria,
        )
        return produto_dao.atualizar(produto)

    @staticmethod
    def produto_excluir(produto_id: int) -> bool:
        _, _, produto_dao, _, _ = View._daos()
        return produto_dao.excluir(produto_id)

    @staticmethod
    def produto_reajustar(percentual: float, id_categoria: Optional[int] = None) -> int:
        _, _, produto_dao, _, _ = View._daos()
        fator = 1.0 + (percentual / 100.0)
        alterados = 0
        for produto in produto_dao.listar():
            if id_categoria is None or produto.id_categoria == id_categoria:
                novo_preco = round(max(0.0, produto.preco * fator), 2)
                produto.preco = novo_preco
                produto_dao.atualizar(produto)
                alterados += 1
        return alterados

    @staticmethod
    def venda_listar() -> List[Venda]:
        _, _, _, venda_dao, _ = View._daos()
        return venda_dao.listar()

    @staticmethod
    def venda_item_listar() -> List[VendaItem]:
        _, _, _, _, item_dao = View._daos()
        return item_dao.listar()
