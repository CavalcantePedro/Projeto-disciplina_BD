class Cliente:
    def __init__(self, nome, email, telefone, endereco):
        # Inicialização da classe Cliente com atributos específicos
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

class Venda:
    def __init__(self, cliente, valor, data):
        # Inicialização da classe Venda com atributos específicos
        self.cliente = cliente
        self.valor = valor
        self.data = data

class GerenciadorCRUD:
    def __init__(self):
        # Inicialização do GerenciadorCRUD com listas vazias para armazenar clientes e vendas
        self.clientes = []
        self.vendas = []

    def inserir_cliente(self, nome, email, telefone, endereco):
        # Método para inserir um novo cliente na lista de clientes
        cliente = Cliente(nome, email, telefone, endereco)
        self.clientes.append(cliente)
        print(f'Cliente {nome} cadastrado com sucesso!')

    def alterar_cliente(self, nome, novo_email, novo_telefone, novo_endereco):
        # Método para alterar informações de um cliente existente na lista
        cliente = self.buscar_cliente(nome)
        if cliente:
            cliente.email = novo_email
            cliente.telefone = novo_telefone
            cliente.endereco = novo_endereco
            print(f'Dados do cliente {nome} alterados com sucesso!')
        else:
            print(f'Cliente {nome} não encontrado.')

    def pesquisar_cliente_por_nome(self, nome):
        # Método para pesquisar um cliente por nome e exibir suas informações
        cliente = self.buscar_cliente(nome)
        if cliente:
            print(f'Nome: {cliente.nome}, Email: {cliente.email}, Telefone: {cliente.telefone}, Endereço: {cliente.endereco}')
        else:
            print(f'Cliente {nome} não encontrado.')

    def remover_cliente(self, nome):
        # Método para remover um cliente da lista
        cliente = self.buscar_cliente(nome)
        if cliente:
            self.clientes.remove(cliente)
            print(f'Cliente {nome} removido com sucesso!')
        else:
            print(f'Cliente {nome} não encontrado.')

    def listar_todos_clientes(self):
        # Método para listar todos os clientes na lista
        print('Lista de Clientes:')
        for cliente in self.clientes:
            print(f'Nome: {cliente.nome}, Email: {cliente.email}, Telefone: {cliente.telefone}, Endereço: {cliente.endereco}')

    def buscar_cliente(self, nome):
        # Método para buscar um cliente na lista por nome
        for cliente in self.clientes:
            if cliente.nome == nome:
                return cliente
        return None

    def inserir_venda(self, cliente_nome, valor, data):
        # Método para inserir uma nova venda na lista
        cliente = self.buscar_cliente(cliente_nome)
        if cliente:
            venda = Venda(cliente, valor, data)
            self.vendas.append(venda)
            print(f'Venda cadastrada com sucesso!')
        else:
            print(f'Cliente {cliente_nome} não encontrado. Venda não cadastrada.')

    def exibir_venda(self, cliente_nome):
        # Método para exibir informações de uma venda para um cliente específico
        for venda in self.vendas:
            if venda.cliente.nome == cliente_nome:
                print(f'Cliente: {venda.cliente.nome}, Valor: {venda.valor}, Data: {venda.data}')
                return
        print(f'Nenhuma venda encontrada para o cliente {cliente_nome}.')

    def gerar_relatorio_vendas(self):
        # Método para gerar um relatório de vendas com informações como quantidade e valor total
        quantidade_vendas = len(self.vendas)
        valor_total_vendas = sum(venda.valor for venda in self.vendas)

        print('\nRelatório de Vendas:')
        print(f'Quantidade de Vendas: {quantidade_vendas}')
        print(f'Valor Total de Vendas: R${valor_total_vendas:.2f}')
# Função principal para interação com o usuário via terminal
def main():
    # Criação de uma instância do GerenciadorCRUD
    gerenciador = GerenciadorCRUD()

    while True:
        # Exibição do menu de opções para o usuário
        print("\n======= Menu =======")
        print("1. Inserir Cliente")
        print("2. Alterar Cliente")
        print("3. Pesquisar Cliente por Nome")
        print("4. Remover Cliente")
        print("5. Listar Todos os Clientes")
        print("6. Inserir Venda")
        print("7. Exibir Venda por Cliente")
        print("8. Gerar Relatório de Vendas")
        print("0. Sair")

        # Solicitação da escolha do usuário
        escolha = input("Escolha uma opção: ")

        # Realização de operações com base na escolha do usuário
        if escolha == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            gerenciador.inserir_cliente(nome, email, telefone, endereco)
        elif escolha == "2":
            nome = input("Nome do cliente a ser alterado: ")
            novo_email = input("Novo Email: ")
            novo_telefone = input("Novo Telefone: ")
            novo_endereco = input("Novo Endereço: ")
            gerenciador.alterar_cliente(nome, novo_email, novo_telefone, novo_endereco)
        elif escolha == "3":
            nome = input("Nome do cliente a ser pesquisado: ")
            gerenciador.pesquisar_cliente_por_nome(nome)
        elif escolha == "4":
            nome = input("Nome do cliente a ser removido: ")
            gerenciador.remover_cliente(nome)
        elif escolha == "5":
            gerenciador.listar_todos_clientes()
        elif escolha == "6":
            cliente_nome = input("Nome do cliente para a venda: ")
            valor = float(input("Valor da venda: "))
            data = input("Data da venda (formato YYYY-MM-DD): ")
            gerenciador.inserir_venda(cliente_nome, valor, data)
        elif escolha == "7":
            cliente_nome = input("Nome do cliente para exibir a venda: ")
            gerenciador.exibir_venda(cliente_nome)
        elif escolha == "8":
            gerenciador.gerar_relatorio_vendas()
        elif escolha == "0":
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Verifica se o script está sendo executado diretamente (não importado como um módulo)
if __name__ == "__main__":
    # Chama a função principal para iniciar a interação com o usuário
    main()
