import sqlite3

#Classe cliente
class Cliente:
    #metodo construtor
    def __init__(self, nome, email, telefone, endereco):
        # Inicialização da classe Cliente com atributos específicos
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

#Classe venda
class Venda:
    #método construtor
    def __init__(self, cliente, valor, data):
        # Inicialização da classe Venda com atributos específicos
        self.cliente = cliente
        self.valor = valor
        self.data = data

#Classe GerenciadorCRUD
class GerenciadorCRUD:
    #Método construtor
    def __init__(self, db_name = 'bancoDeDados.db'):
        #Conexão com o banco de dados
        self.conn = sqlite3.connect('bancoDeDados.db')
            
        #Criação do cursor
        self.cursor = self.conn.cursor()
    
        #Criação da tabela cliente
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS cliente (
                        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT UNIQUE,
                        telefone TEXT NOT NULL,
                        endereco TEXT NOT NULL
                    )
                        """)

        #Criação da tabela venda
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS venda (
                        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER NOT NULL,
                        valor REAL NOT NULL,    
                        data DATE NOT NULL,
                        FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
                        )
                        """)
        # O ForeignKey é uma chave estrangeira que faz referência a chave primária da tabela cliente

    #Método para inserir um novo cliente na tabela de clientes
    def inserir_cliente(self, nome, email, telefone, endereco):
        # Método para inserir um novo cliente na tabela de clientes
        try:
            if nome == '' or telefone == '' or endereco == '':
                print('Nome, telefone e endereço são campos obrigatórios.')
            else:
                cliente = Cliente(nome, email, telefone, endereco)
                self.cursor.execute("""
                    INSERT INTO cliente (nome, email, telefone, endereco)
                    VALUES (?,?,?,?)
                    """, (cliente.nome, cliente.email, cliente.telefone, cliente.endereco))
                self.conn.commit()
                print(f'\n\nCliente {cliente.nome} cadastrado com sucesso!')
        except sqlite3.Error as e:
            print('\n\nErro ao inserir cliente')

    #Método para alterar informações de um cliente existente na tabela
    def alterar_cliente(self, id_cliente ,novo_nome, novo_email, novo_telefone, novo_endereco):
        # Método para alterar informações de um cliente existente na tabela
        try: 
            self.cursor.execute("""
                UPDATE cliente
                SET nome = ?, email = ?, telefone = ?, endereco = ?
                WHERE id_cliente = ?
                """, (novo_nome, novo_email, novo_telefone, novo_endereco, id_cliente))
            self.conn.commit()
            print(f'Cliente {novo_nome} alterado com sucesso!')
        except sqlite3.Error as e:
            print('Erro ao alterar cliente')
    
    #Método para buscar um cliente na tabela por id
    def buscar_cliente(self, id_cliente):
        # Método para buscar um cliente na tabela por id
        try:
            self.cursor.execute("""
                SELECT * FROM cliente
                WHERE id_cliente = ?
                """, (id_cliente,))
            cliente = self.cursor.fetchone()
            if cliente:
                return cliente
            else:
                return None
        except sqlite3.Error as e:
            print('Erro ao buscar cliente')
            return None
        return None

    #Método para remover um cliente da tabela por id
    def remover_cliente(self, id_cliente):
        try:
            self.cursor.execute("""
                DELETE FROM cliente
                WHERE id_cliente = ?
                """, (id_cliente,))
            self.conn.commit()
            print(f'Cliente removido com sucesso!')
        except sqlite3.Error as e:
            print('Erro ao remover cliente')

    #Método para listar todos os clientes na tabela
    def listar_todos_clientes(self):
        # Método para listar todos os clientes na tabela
        try:
            self.cursor.execute("""
                SELECT * FROM cliente
                """)
            clientes = self.cursor.fetchall()
            print('\nLista de Clientes:')
            for cliente in clientes:
                print(f'ID: {cliente[0]}, Nome: {cliente[1]}, Email: {cliente[2]}, Telefone: {cliente[3]}, Endereço: {cliente[4]}')
        except sqlite3.Error as e:
            print('Erro ao listar clientes')
    
    # Método para inserir uma nova venda na tabela
    def inserir_venda(self, id_cliente, valor, data):
        # Método para inserir uma nova venda na tabela
        try:
            # Verificar se o id_cliente existe na tabela cliente
            cliente_existente = self.buscar_cliente(id_cliente)
            
            # Substituir vírgula por ponto para valores decimais    
            valor = float(valor.replace(',', '.'))
            
            if cliente_existente:
                self.cursor.execute("""
                    INSERT INTO venda (id_cliente, valor, data)
                    VALUES (?, ?, ?)
                """, (id_cliente, valor, data))
                self.conn.commit()
                print(f'Venda cadastrada com sucesso!')
            else:
                print(f'Cliente com ID {id_cliente} não encontrado. Venda não cadastrada.')
        except sqlite3.Error as e:
            print(f'Erro ao cadastrar venda: {e}')


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

    def fechar_conexao(self):
        print('Fechando conexão com o banco de dados...')
        self.conn.close()

# Função principal para interação com o usuário via terminal
def main():
    # Criação de uma instância do GerenciadorCRUD
    gerenciador = GerenciadorCRUD()

    while True:
        # Exibição do menu de opções para o usuário
        print("\n======= Menu =======")
        print("\n===== Cliente=====")
        print("1. Inserir Cliente")
        print("2. Alterar Cliente")
        print("3. Remover Cliente")
        print("4. Listar Todos os Clientes")
        print("\n===== Venda=====")
        print("5. Inserir Venda")
        print("6. Exibir Venda por Cliente")
        print("7. Gerar Relatório de Vendas")
        print("0. Sair")

        # Solicitação da escolha do usuário
        escolha = input("\nEscolha uma opção: \n")

        # Realização de operações com base na escolha do usuário
       
        # Inserir Cliente
        if escolha == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            gerenciador.inserir_cliente(nome, email, telefone, endereco)
        # Alterar Cliente
        elif escolha == "2":
            id_cliente = input("Id do cliente a ser alterado: ")
            if gerenciador.buscar_cliente(id_cliente):
                print("Digite os novos dados do cliente:")
                novo_nome = input("Novo Nome: ")
                novo_email = input("Novo Email: ")
                novo_telefone = input("Novo Telefone: ")
                novo_endereco = input("Novo Endereço: ")
                gerenciador.alterar_cliente(id_cliente,novo_nome, novo_email, novo_telefone, novo_endereco)
            else:
                print(f'Cliente {id_cliente} não encontrado.')
        # Remover Cliente
        elif escolha == "3":
            id_cliente = input("ID do cliente a ser removido: ")
            gerenciador.remover_cliente(id_cliente)
        # Listar Todos os Clientes
        elif escolha == "4":
            gerenciador.listar_todos_clientes()
        # Inserir Venda
        elif escolha == "5":
            id_cliente = input("Id do cliente que comprou : ")
            valor = input("Valor da venda: ")
            data = input("Data da venda (formato DD-MM-AAAA): ")
            gerenciador.inserir_venda(id_cliente, valor, data)
        # Exibir Venda por Cliente
        elif escolha == "6":
            cliente_nome = input("Nome do cliente para exibir a venda: ")
            gerenciador.exibir_venda(cliente_nome)
        # Gerar Relatório de Vendas
        elif escolha == "7":
            gerenciador.gerar_relatorio_vendas()
        # Sair
        elif escolha == "0":
            print("Saindo do programa.")
            break
        # Opção inválida
        else:
            print("Opção inválida. Tente novamente.")
    gerenciador.fechar_conexao()

# Verifica se o script está sendo executado diretamente (não importado como um módulo)
if __name__ == "__main__":
    # Chama a função principal para iniciar a interação com o usuário
    main()
