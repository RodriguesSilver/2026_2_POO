from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Cliente:
    id: int
    nome: str
    email: str
    fone: str
    senha: str = "1234"

    def __str__(self) -> str:
        return f"{self.id} - {self.nome} ({self.email} | {self.fone})"


@dataclass
class Categoria:
    id: int
    descricao: str

    def __str__(self) -> str:
        return f"{self.id} - {self.descricao}"


@dataclass
class Produto:
    id: int
    descricao: str
    preco: float
    estoque: int
    id_categoria: Optional[int] = None

    def __str__(self) -> str:
        return (
            f"{self.id} - {self.descricao} | R$ {self.preco:.2f} "
            f"| Estoque: {self.estoque} | Cat: {self.id_categoria}"
        )


@dataclass
class VendaItem:
    id: int
    id_venda: int
    id_produto: int
    qtd: int
    preco: float

    @property
    def subtotal(self) -> float:
        return self.qtd * self.preco


@dataclass
class Venda:
    id: int
    data: datetime = field(default_factory=datetime.now)
    carrinho: bool = True
    total: float = 0.0
    id_cliente: Optional[int] = None


class _BaseDAO:
    def __init__(self, store: Dict[int, object]):
        self._store = store

    def _proximo_id(self) -> int:
        return (max(self._store.keys()) + 1) if self._store else 1

    def inserir(self, obj: object) -> object:
        novo_id = self._proximo_id()
        obj.id = novo_id
        self._store[novo_id] = obj
        return obj

    def listar(self) -> List[object]:
        return list(self._store.values())

    def listar_por_id(self, obj_id: int) -> Optional[object]:
        return self._store.get(obj_id)

    def atualizar(self, obj: object) -> bool:
        obj_id = getattr(obj, "id", None)
        if obj_id is not None and obj_id in self._store:
            self._store[obj_id] = obj
            return True
        return False

    def excluir(self, obj_id: int) -> bool:
        if obj_id in self._store:
            del self._store[obj_id]
            return True
        return False


class ClienteDAO(_BaseDAO):
    def listar(self) -> List[Cliente]:
        return super().listar()

    def listar_por_id(self, obj_id: int) -> Optional[Cliente]:
        return super().listar_por_id(obj_id)


class CategoriaDAO(_BaseDAO):
    def listar(self) -> List[Categoria]:
        return super().listar()

    def listar_por_id(self, obj_id: int) -> Optional[Categoria]:
        return super().listar_por_id(obj_id)


class ProdutoDAO(_BaseDAO):
    def listar(self) -> List[Produto]:
        return super().listar()

    def listar_por_id(self, obj_id: int) -> Optional[Produto]:
        return super().listar_por_id(obj_id)


class VendaDAO(_BaseDAO):
    def listar(self) -> List[Venda]:
        return super().listar()

    def listar_por_id(self, obj_id: int) -> Optional[Venda]:
        return super().listar_por_id(obj_id)


class VendaItemDAO(_BaseDAO):
    def listar(self) -> List[VendaItem]:
        return super().listar()

    def listar_por_id(self, obj_id: int) -> Optional[VendaItem]:
        return super().listar_por_id(obj_id)
