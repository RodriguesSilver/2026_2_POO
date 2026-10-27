import json


class Cliente:

  def __init__(self, id: int, nome: str, email: str, fone: str):
    self.__id = id
    self.__nome = nome
    self.__email = email
    self.__fone = fone

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, valor):
    self.__id = valor

  @property
  def nome(self):
    return self.__nome

  @nome.setter
  def nome(self, valor):
    self.__nome = valor

  @property
  def email(self):
    return self.__email

  @email.setter
  def email(self, valor):
    self.__email = valor

  @property
  def fone(self):
    return self.__fone

  @fone.setter
  def fone(self, valor):
    self.__fone = valor

  def __str__(self):
    return f"ID: {self.__id} | Nome: {self.__nome} | Email: {self.__email} | Fone: {self.__fone}"

  def to_dict(self):
    return {
        "id": self.id,
        "nome": self.nome,
        "email": self.email,
        "fone": self.fone,
    }

  @classmethod
  def from_dict(cls, dados):
    return cls(dados["id"], dados["nome"], dados["email"], dados["fone"])


class ClienteDAO:
  objetos = []

  @classmethod
  def inserir(cls, cliente):
    cls.objetos.append(cliente)

  @classmethod
  def listar(cls):
    return cls.objetos

  @classmethod
  def listar_id(cls, id):
    for obj in cls.objetos:
      if obj.id == id:
        return obj
    return None

  @classmethod
  def atualizar(cls, cliente):
    existente = cls.listar_id(cliente.id)
    if existente:
      existente.nome = cliente.nome
      existente.email = cliente.email
      existente.fone = cliente.fone

  @classmethod
  def excluir(cls, cliente):
    cls.objetos.remove(cliente)

  @classmethod
  def salvar(cls):
    with open("clientes.json", "w", encoding="utf-8") as f:
      dados = [c.to_dict() for c in cls.objetos]
      json.dump(dados, f, indent=4, ensure_ascii=False)

  @classmethod
  def abrir(cls):
    cls.objetos = []
    try:
      with open("clientes.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
        for d in dados:
          cls.objetos.append(Cliente.from_dict(d))
    except FileNotFoundError:
      pass


class UI:

  @staticmethod
  def menu():
    print("\n=== SISTEMA DE GESTÃO DE CLIENTES ===")
    print("1 - Listar Clientes")
    print("2 - Inserir Cliente")
    print("3 - Atualizar Cliente")
    print("4 - Excluir Cliente")
    print("0 - Sair")
    return input("Escolha uma opção: ")

  @staticmethod
  def main():
    ClienteDAO.abrir()

    op = ""
    while op != "0":
      op = UI.menu()
      if op == "1":
        UI.cliente_listar()
      elif op == "2":
        UI.cliente_inserir()
      elif op == "3":
        UI.cliente_atualizar()
      elif op == "4":
        UI.cliente_excluir()
      elif op == "0":
        ClienteDAO.salvar()
        print("\nDados salvos com sucesso. Encerrando o programa!")
      else:
        print("\nOpção inválida! Tente novamente.")

  @staticmethod
  def cliente_listar():
    clientes = ClienteDAO.listar()
    if len(clientes) == 0:
      print("\nNenhum cliente cadastrado.")
    else:
      print("\n--- LISTA DE CLIENTES ---")
      for c in clientes:
        print(c)

  @staticmethod
  def cliente_inserir():
    print("\n--- NOVO CLIENTE ---")
    id = int(input("ID: "))
    nome = input("Nome: ")
    email = input("Email: ")
    fone = input("Telefone: ")

    novo_cliente = Cliente(id, nome, email, fone)
    ClienteDAO.inserir(novo_cliente)
    print("Cliente cadastrado com sucesso!")

  @staticmethod
  def cliente_atualizar():
    print("\n--- ATUALIZAR CLIENTE ---")
    id = int(input("Informe o ID do cliente que deseja alterar: "))
    cliente = ClienteDAO.listar_id(id)

    if cliente is None:
      print("Cliente não encontrado!")
    else:
      print(f"Dados atuais -> {cliente}")
      novo_nome = input("Novo Nome: ")
      novo_email = input("Novo Email: ")
      novo_fone = input("Novo Telefone: ")

      cliente_atualizado = Cliente(id, novo_nome, novo_email, novo_fone)
      ClienteDAO.atualizar(cliente_atualizado)
      print("Cliente atualizado com sucesso!")

  @staticmethod
  def cliente_excluir():
    print("\n--- EXCLUIR CLIENTE ---")
    id = int(input("Informe o ID do cliente que deseja excluir: "))
    cliente = ClienteDAO.listar_id(id)

    if cliente is None:
      print("Cliente não encontrado!")
    else:
      ClienteDAO.excluir(cliente)
      print("Cliente excluído com sucesso!")


if __name__ == "__main__":
  UI.main()
    

    
    



    
    