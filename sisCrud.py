import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

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
    def __init__(self, cliente, valor, data, descricao):
        # Inicialização da classe Venda com atributos específicos
        self.cliente = cliente
        self.valor = valor
        self.data = data
        self.descricao = descricao

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
                        descricao TEXT,
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
    def inserir_venda(self, id_cliente, valor, data, descricao):
        # Método para inserir uma nova venda na tabela
        try:
            # Verificar se o id_cliente existe na tabela cliente
            cliente_existente = self.buscar_cliente(id_cliente)
            
            # Substituir vírgula por ponto para valores decimais    
            valor = float(valor.replace(',', '.'))
            data = data.replace('/', '-')
            # Converter a data para o formato YYYY-MM-DD
            data = datetime.strptime(data, '%d-%m-%Y').strftime('%Y-%m-%d')
            
            if cliente_existente:
                self.cursor.execute("""
                    INSERT INTO venda (id_cliente, valor, data, descricao)
                    VALUES (?, ?, ?, ?)
                """, (id_cliente, valor, data, descricao))
                self.conn.commit()
                print(f'Venda cadastrada com sucesso!')
            else:
                print(f'Cliente com ID {id_cliente} não encontrado. Venda não cadastrada.')
        except sqlite3.Error as e:
            print(f'Erro ao cadastrar venda: {e}')

    # Método para exibir todas as compras feitas por um cliente
    def exibir_venda(self, id_cliente):
         # Método para mostrar todas as compras feitas por um cliente
        try:
            self.cursor.execute("""
                SELECT v.id_venda, v.valor, v.data, v.descricao
                FROM venda v
                WHERE v.id_cliente = ?
            """, (id_cliente,))
            
            compras = self.cursor.fetchall()
            
            if compras:
                print(f'\nCompras do Cliente ID {id_cliente}:')
                for compra in compras:
                    print(f'Valor: {compra[1]}, Data: {compra[2]}, Descrição: {compra[3]}')
                    valor = sum(compra[1] for compra in compras)
            else:
                print(f'O cliente com ID {id_cliente} ainda não fez compras.')
            print(f'Valor Total gasto pelo cliente: R${valor:.2f}')
        except sqlite3.Error as e:
            print(f'Erro ao mostrar compras do cliente: {e}')

    # Método para gerar um relatório de vendas com informações como quantidade e valor total
    def gerar_relatorio_vendas(self):
        # Método para gerar um relatório de vendas com informações como quantidade e valor total
        try:
            # Obter o mês e o ano atuais
            data_atual = datetime.now()
            mes_atual = data_atual.month
            ano_atual = data_atual.year

            # Definir o nome do arquivo PDF
            nome_arquivo = f"Relatorio_Vendas_{mes_atual}_{ano_atual}.pdf"

            # Criar o arquivo PDF
            pdf = canvas.Canvas(nome_arquivo, pagesize=letter)

            # Configuração do cabeçalho
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(72, 780, "Relatório de Vendas Mensal")
            pdf.drawString(72, 760, f"Mês: {mes_atual}, Ano: {ano_atual}")

            # Recuperar todas as vendas do mês
            self.cursor.execute("""
                    SELECT c.nome, v."data" , v.valor, v.descricao
                    FROM venda v
                    JOIN cliente c ON v.id_cliente = c.id_cliente
                    WHERE STRFTIME('%m', v."data") = ? AND STRFTIME('%Y', v."data") = ?
            """, (str(mes_atual).zfill(2), str(ano_atual)))

            vendas_mensais = self.cursor.fetchall()

            # Configuração do corpo do relatório
            pdf.setFont("Helvetica", 12)
            y_position = 740

            for venda in vendas_mensais:
                nome_cliente, data_venda, valor_venda, descricao_venda = venda  
                # Converter a data para o formato DD/MM/YYYY
                data_venda = datetime.strptime(data_venda, '%Y-%m-%d').strftime('%d/%m/%Y')                
                pdf.drawString(72, y_position, f"> Cliente: {nome_cliente}, Data: {data_venda}, Valor: R${valor_venda:.2f}")
                pdf.drawString(72, y_position - 20, f"Descrição: {descricao_venda}") 
                y_position -= 40

            # Calcular o total faturado
            total_faturado = sum(venda[2] for venda in vendas_mensais)

            # Configuração do rodapé
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(72, y_position, f"Total Faturado: R${total_faturado:.2f}")

            pdf.save()

            print(f'Relatório gerado com sucesso: {nome_arquivo}')

        except sqlite3.Error as e:
            print(f'Erro ao gerar relatório de vendas mensal: {e}')
        
        except Exception as e:
            print(f'Erro inesperado: {e}')

    # Método para gerar um relatório de vendas anual com informações como quantidade e valor total
    def gerar_relatorio_vendas_ano(self):
        # Método para gerar um relatório de vendas anual com informações como quantidade e valor total
        try:
            # Obter o ano atual
            ano_atual = datetime.now().year

            # Definir o nome do arquivo PDF
            nome_arquivo = f"Relatorio_Vendas_{ano_atual}.pdf"

            # Criar o arquivo PDF
            pdf = canvas.Canvas(nome_arquivo, pagesize=letter)

            # Configuração do cabeçalho
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(72, 780, "Relatório de Vendas Anual")
            pdf.drawString(72, 760, f"Ano: {ano_atual}")

            # Recuperar todas as vendas do ano
            self.cursor.execute("""
                        SELECT c.nome, v."data" , v.valor, v.descricao
                        FROM venda v
                        JOIN cliente c ON v.id_cliente = c.id_cliente
                        WHERE STRFTIME('%Y', v."data") = ?
                """, (str(ano_atual),))

            vendas_anuais = self.cursor.fetchall()

            # Configuração do corpo do relatório
            pdf.setFont("Helvetica", 12)
            y_position = 740

            for venda in vendas_anuais:
                nome_cliente, data_venda, valor_venda, descricao_venda = venda  
                # Converter a data para o formato DD/MM/YYYY
                data_venda = datetime.strptime(data_venda, '%Y-%m-%d').strftime('%d/%m/%Y')                
                pdf.drawString(72, y_position, f"> Cliente: {nome_cliente}, Data: {data_venda}, Valor: R${valor_venda:.2f}")
                pdf.drawString(72, y_position - 20, f"Descrição: {descricao_venda}") 
                y_position -= 40

            # Calcular o total faturado
            total_faturado = sum(venda[2] for venda in vendas_anuais)

            # Configuração do rodapé
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(72, y_position, f"Total Faturado: R${total_faturado:.2f}")

            pdf.save()

            print(f'Relatório gerado com sucesso: {nome_arquivo}')

        except sqlite3.Error as e:
            print(f'Erro ao gerar relatório de vendas anual: {e}')
  
    #Método para gerar relatório de vendas do dia
    def gerar_relatorio_vendas_dia(self):
    # Método para gerar um relatório de vendas diário com informações como quantidade e valor total
        try: 
            # Obter dia atual 
            dia_atual = datetime.now().day
            mes_atual = datetime.now().month
            ano_atual = datetime.now().year

            #definir o nome do arquivo PDF
            nome_arquivo = f"Relatorio_Vendas_{dia_atual}-{mes_atual}-{ano_atual}.pdf"

            #criar o arquivo PDF
            pdf = canvas.Canvas(nome_arquivo, pagesize=letter)

             # Configuração do cabeçalho
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(72, 780, "Relatório de Vendas do Dia")
            pdf.drawString(72, 760, f"Dia: {dia_atual}, Mês: {mes_atual}, Ano: {ano_atual}")

            # Recuperar todas as vendas do dia
            self.cursor.execute("""
                    SELECT c.nome, v."data" , v.valor, v.descricao
                    FROM venda v
                    JOIN cliente c ON v.id_cliente = c.id_cliente
                    WHERE STRFTIME('%d', v."data") = ? AND STRFTIME('%m', v."data") = ? AND STRFTIME('%Y', v."data") = ?
            """, (str(dia_atual).zfill(2), str(mes_atual).zfill(2), str(ano_atual)))

            vendas_diarias = self.cursor.fetchall()

           # Configuração do corpo do relatório
            pdf.setFont("Helvetica", 12)
            y_position = 740

            for venda in vendas_diarias:
                nome_cliente, data_venda, valor_venda, descricao_venda = venda  
                # Converter a data para o formato DD/MM/YYYY
                data_venda = datetime.strptime(data_venda, '%Y-%m-%d').strftime('%d/%m/%Y')                
                pdf.drawString(72, y_position, f"> Cliente: {nome_cliente}, Data: {data_venda}, Valor: R${valor_venda:.2f}")
                pdf.drawString(72, y_position - 20, f"Descrição: {descricao_venda}") 
                y_position -= 40
            
            # Calcular o total faturado
            total_faturado = sum(venda[2] for venda in vendas_diarias)

            # Configuração do rodapé
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(72, y_position, f"Total Faturado: R${total_faturado:.2f}")

            pdf.save()

            print(f'Relatório gerado com sucesso: {nome_arquivo}')
        
        except sqlite3.Error as e:
            print(f'Erro ao gerar relatório de vendas anual: {e}')

    # Método para listar clientes por nome
    def listar_clientes_por_nome(self, nome):
         # Método para pesquisar clientes pelo nome parcial e exibir todas as correspondências
        try:
            self.cursor.execute("""
                SELECT *
                FROM cliente
                WHERE nome LIKE '%' || ? || '%'
            """, (nome,))

            clientes_encontrados = self.cursor.fetchall()

            if clientes_encontrados:
                print(f'Clientes encontrados com o nome contendo "{nome}":')
                for cliente in clientes_encontrados:
                    print(f'ID: {cliente[0]}, Nome: {cliente[1]}, Email: {cliente[2]}, Telefone: {cliente[3]}, Endereço: {cliente[4]}')
            else:
                print(f'Nenhum cliente encontrado com o nome contendo "{nome}".')

        except sqlite3.Error as e:
            print(f'Erro ao pesquisar clientes por nome: {e}')

    # Método para fechar a conexão com o banco de dados
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
        print("\n===== Cliente =====")
        print("1. Inserir Cliente")
        print("2. Alterar Cliente")
        print("3. Remover Cliente")
        print("4. Listar Todos os Clientes")
        print("5. Listar clientes e seus ids por nome")
        print("\n===== Venda =====")
        print("6. Inserir Venda")
        print("7. Exibir Venda por Cliente")
        print("8. Gerar Relatório de Vendas do Mês atual")
        print("9. Gerar Relatório Vendas do Ano atual")
        print("10. Gerar Relatório de Vendas do dia atual")
        print("11.Gerar Relatório de Vendas do mês do intervalo de datas")
        print("\n===== Sair =====")
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
        # Listar clientes e seus ids por nome
        elif escolha == "5":
            print("Pesquisar clientes pelo nome:")
            gerenciador.listar_clientes_por_nome(input("Nome do cliente: "))
        # Inserir Venda
        elif escolha == "6":
            id_cliente = input("Id do cliente que comprou : ")
            valor = input("Valor da venda: ")
            data = input("Data da venda (formato DD/MM/AAAA): ")
            descricao = input("Descrição da venda: ")
            gerenciador.inserir_venda(id_cliente, valor, data, descricao)
        # Exibir Venda por Cliente
        elif escolha == "7":
            id_cliente = input("Id do cliente para exibir a venda: ")
            gerenciador.exibir_venda(id_cliente)
        # Gerar Relatório de Vendas
        elif escolha == "8":
            gerenciador.gerar_relatorio_vendas()
        # Gerar Relatório Anual de Vendas
        elif escolha == "9":
            gerenciador.gerar_relatorio_vendas_ano()
        # Gerar Relatório de Vendas do dia
        elif escolha == "10":
            gerenciador.gerar_relatorio_vendas_dia()
        # Gerar Relatório de Vendas do mês do intervalo de datas
        elif escolha == "11":
            print("Opção em desenvolvimento.")
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