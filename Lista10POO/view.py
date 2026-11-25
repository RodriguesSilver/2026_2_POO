from datetime import datetime
from typing import Dict, List, Optional, Tuple
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
    """Classe estática de serviço/fachada com controle de sessão e operações."""

    @staticmethod
    def _garantir_estado() -> Dict[str, object]:
        if "db_ecommerce_l10" not in st.session_state:
            st.session_state["db_ecommerce_l10"] = {
                "clientes": {},
                "categorias": {},
                "produtos": {},
                "vendas": {},
                "venda_itens": {},
                "usuario_logado": None,
                "perfil": "Visitante",
            }
            # Admin padrão com e-mail "admin" conforme enunciado
            View.cliente_inserir("Administrador", "admin", "(84) 90000-0000", "admin")
            View.cliente_inserir("Ana Silva", "ana@email.com", "(84) 99999-1111", "1234")
            View.cliente_inserir("Bruno Costa", "bruno@email.com", "(84) 98888-2222", "1234")

            cat_elec = View.categoria_inserir("Eletrônicos")
            cat_livros = View.categoria_inserir("Livros")

            View.produto_inserir("Mouse Sem Fio", 79.90, 15, cat_elec.id)
            View.produto_inserir("Teclado Mecânico", 249.00, 8, cat_elec.id)
            View.produto_inserir("Python Fluente", 120.00, 12, cat_livros.id)

        return st.session_state["db_ecommerce_l10"]

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

    # ---------------- SESSÃO / AUTENTICAÇÃO ----------------
    @staticmethod
    def get_usuario_logado() -> Optional[Cliente]:
        db = View._garantir_estado()
        return db["usuario_logado"]

    @staticmethod
    def get_perfil() -> str:
        db = View._garantir_estado()
        return db["perfil"]

    @staticmethod
    def entrar(email: str, senha: str = "") -> Tuple[bool, str]:
        email_limpo = email.strip().lower()
        if not email_limpo:
            return False, "Informe o e-mail para entrar."

        for cli in View.cliente_listar():
            if cli.email.strip().lower() == email_limpo:
                # Admin entra com e-mail "admin"; clientes podem informar senha ou entrar pelo e-mail cadastrado
                if email_limpo == "admin" and senha and senha != cli.senha and senha != "admin":
                    return False, "Senha incorreta para o administrador."
                if email_limpo != "admin" and senha and senha != cli.senha:
                    return False, "Senha incorreta."

                db = View._garantir_estado()
                db["usuario_logado"] = cli
                db["perfil"] = "Admin" if cli.email.strip().lower() == "admin" else "Cliente"
                return True, f"Bem-vindo, {cli.nome} ({db['perfil']})!"

        return False, "Usuário não encontrado. Você pode abrir uma conta na opção 'Abrir conta'."

    @staticmethod
    def sair() -> None:
        db = View._garantir_estado()
        db["usuario_logado"] = None
        db["perfil"] = "Visitante"

    @staticmethod
    def abrir_conta(nome: str, email: str, fone: str, senha: str = "1234") -> Tuple[bool, str]:
        email_limpo = email.strip().lower()
        if not nome.strip() or not email_limpo:
            return False, "Nome e e-mail são obrigatórios."
        if email_limpo == "admin":
            return False, "O e-mail 'admin' é reservado."
        for cli in View.cliente_listar():
            if cli.email.strip().lower() == email_limpo:
                return False, "Já existe um cliente cadastrado com este e-mail."

        novo = View.cliente_inserir(nome, email_limpo, fone, senha or "1234")
        return True, f"Conta criada com sucesso! Seu ID é {novo.id}. Agora você já pode entrar no sistema."

    # ---------------- CLIENTES ----------------
    @staticmethod
    def cliente_listar() -> List[Cliente]:
        cliente_dao, _, _, _, _ = View._daos()
        return cliente_dao.listar()

    @staticmethod
    def cliente_listar_por_id(cliente_id: int) -> Optional[Cliente]:
        cliente_dao, _, _, _, _ = View._daos()
        return cliente_dao.listar_por_id(cliente_id)

    @staticmethod
    def cliente_inserir(nome: str, email: str, fone: str, senha: str = "1234") -> Cliente:
        cliente_dao, _, _, _, _ = View._daos()
        cliente = Cliente(
            id=0, nome=nome.strip(), email=email.strip(), fone=fone.strip(), senha=senha
        )
        return cliente_dao.inserir(cliente)

    @staticmethod
    def cliente_atualizar(
        cliente_id: int, nome: str, email: str, fone: str, senha: Optional[str] = None
    ) -> bool:
        cliente_dao, _, _, _, _ = View._daos()
        atual = cliente_dao.listar_por_id(cliente_id)
        senha_final = senha if senha is not None else (atual.senha if atual else "1234")
        cliente = Cliente(
            id=cliente_id,
            nome=nome.strip(),
            email=email.strip(),
            fone=fone.strip(),
            senha=senha_final,
        )
        return cliente_dao.atualizar(cliente)

    @staticmethod
    def cliente_excluir(cliente_id: int) -> bool:
        cliente_dao, _, _, _, _ = View._daos()
        return cliente_dao.excluir(cliente_id)

    # ---------------- CATEGORIAS ----------------
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

    # ---------------- PRODUTOS ----------------
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

    # ---------------- CARRINHO E VENDAS ----------------
    @staticmethod
    def _obter_ou_criar_carrinho(cliente_id: int) -> Venda:
        _, _, _, venda_dao, _ = View._daos()
        for venda in venda_dao.listar():
            if venda.id_cliente == cliente_id and venda.carrinho:
                return venda
        nova_venda = Venda(
            id=0, data=datetime.now(), carrinho=True, total=0.0, id_cliente=cliente_id
        )
        return venda_dao.inserir(nova_venda)

    @staticmethod
    def _recalcular_total_venda(venda_id: int) -> None:
        _, _, _, venda_dao, item_dao = View._daos()
        venda = venda_dao.listar_por_id(venda_id)
        if venda is None:
            return
        total = sum(
            item.qtd * item.preco for item in item_dao.listar() if item.id_venda == venda_id
        )
        venda.total = round(total, 2)
        venda_dao.atualizar(venda)

    @staticmethod
    def carrinho_inserir_produto(cliente_id: int, produto_id: int, qtd: int) -> Tuple[bool, str]:
        if qtd <= 0:
            return False, "A quantidade deve ser maior que zero."

        _, _, produto_dao, _, item_dao = View._daos()
        produto = produto_dao.listar_por_id(produto_id)
        if produto is None:
            return False, "Produto não encontrado."

        carrinho = View._obter_ou_criar_carrinho(cliente_id)
        item_existente: Optional[VendaItem] = None
        for item in item_dao.listar():
            if item.id_venda == carrinho.id and item.id_produto == produto.id:
                item_existente = item
                break

        qtd_total_desejada = qtd + (item_existente.qtd if item_existente else 0)
        if qtd_total_desejada > produto.estoque:
            return False, f"Estoque insuficiente. Disponível: {produto.estoque} unidade(s)."

        if item_existente is not None:
            item_existente.qtd = qtd_total_desejada
            item_existente.preco = produto.preco
            item_dao.atualizar(item_existente)
        else:
            novo_item = VendaItem(
                id=0,
                id_venda=carrinho.id,
                id_produto=produto.id,
                qtd=qtd,
                preco=produto.preco,
            )
            item_dao.inserir(novo_item)

        View._recalcular_total_venda(carrinho.id)
        return True, f"Adicionado {qtd}x '{produto.descricao}' ao carrinho!"

    @staticmethod
    def carrinho_itens(cliente_id: int) -> List[Tuple[VendaItem, Produto]]:
        _, _, produto_dao, venda_dao, item_dao = View._daos()
        carrinho: Optional[Venda] = None
        for venda in venda_dao.listar():
            if venda.id_cliente == cliente_id and venda.carrinho:
                carrinho = venda
                break
        if carrinho is None:
            return []

        resultado: List[Tuple[VendaItem, Produto]] = []
        for item in item_dao.listar():
            if item.id_venda == carrinho.id:
                prod = produto_dao.listar_por_id(item.id_produto)
                if prod is not None:
                    resultado.append((item, prod))
        return resultado

    @staticmethod
    def carrinho_limpar(cliente_id: int) -> None:
        _, _, _, venda_dao, item_dao = View._daos()
        for venda in venda_dao.listar():
            if venda.id_cliente == cliente_id and venda.carrinho:
                itens_remover = [i.id for i in item_dao.listar() if i.id_venda == venda.id]
                for item_id in itens_remover:
                    item_dao.excluir(item_id)
                venda.total = 0.0
                venda_dao.atualizar(venda)

    @staticmethod
    def carrinho_comprar(cliente_id: int) -> Tuple[bool, str]:
        _, _, produto_dao, venda_dao, item_dao = View._daos()
        carrinho: Optional[Venda] = None
        for venda in venda_dao.listar():
            if venda.id_cliente == cliente_id and venda.carrinho:
                carrinho = venda
                break

        if carrinho is None:
            return False, "Seu carrinho está vazio."

        itens = [i for i in item_dao.listar() if i.id_venda == carrinho.id]
        if not itens:
            return False, "Seu carrinho está vazio."

        # Verifica estoque de todos os itens antes de confirmar
        for item in itens:
            prod = produto_dao.listar_por_id(item.id_produto)
            if prod is None or item.qtd > prod.estoque:
                nome_prod = prod.descricao if prod else f"ID {item.id_produto}"
                disp = prod.estoque if prod else 0
                return False, f"Estoque insuficiente para '{nome_prod}' (disponível: {disp})."

        # Baixa no estoque e finaliza compra
        for item in itens:
            prod = produto_dao.listar_por_id(item.id_produto)
            if prod is not None:
                prod.estoque -= item.qtd
                produto_dao.atualizar(prod)

        carrinho.carrinho = False
        carrinho.data = datetime.now()
        View._recalcular_total_venda(carrinho.id)
        venda_dao.atualizar(carrinho)
        return True, f"Compra #{carrinho.id} finalizada com sucesso! Total: R$ {carrinho.total:.2f}"

    @staticmethod
    def venda_listar_compras_cliente(cliente_id: int) -> List[Venda]:
        _, _, _, venda_dao, _ = View._daos()
        return [
            v for v in venda_dao.listar() if v.id_cliente == cliente_id and not v.carrinho
        ]

    @staticmethod
    def venda_listar_todas() -> List[Venda]:
        _, _, _, venda_dao, _ = View._daos()
        return [v for v in venda_dao.listar() if not v.carrinho]

    @staticmethod
    def venda_itens_por_venda(venda_id: int) -> List[Tuple[VendaItem, Optional[Produto]]]:
        _, _, produto_dao, _, item_dao = View._daos()
        return [
            (item, produto_dao.listar_por_id(item.id_produto))
            for item in item_dao.listar()
            if item.id_venda == venda_id
        ]
