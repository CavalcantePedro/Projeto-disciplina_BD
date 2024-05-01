import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

#Classe estoque
class Estoque:
    #método construtor
    def __init__(self, nome, quantidade, valor, categoria, fab_mari):
        # Inicialização da classe Estoque com atributos específicos
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
        self.categoria = categoria
        self.fab_mari = fab_mari

#Classe cliente 
class Cliente:
    #metodo construtor
    def __init__(self, nome, email, telefone, endereco, username, senha):
        # Inicialização da classe Cliente com atributos específicos
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.username = username
        self.senha = senha

#Classe vendedor
class Vendedor:
    #método construtor
    def __init__(self, nome, email, telefone, username, senha):
        # Inicialização da classe Vendedor com atributos específicos
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.username = username
        self.senha = senha

#Classe venda
class Venda:
    #método construtor
    def __init__(self, cliente, valor, data, descricao, vendedor, item, tipo_pagamento):
        # Inicialização da classe Venda com atributos específicos
        self.item = item
        self.cliente = cliente
        self.vendedor = vendedor
        self.valor = valor
        self.data = data
        self.descricao = descricao
        self.tipo_pagamento = tipo_pagamento

#Classe GerenciadorCRUD
class GerenciadorCRUD:
    #Método construtor
    def __init__(self, db_name = 'bancoDeDados.db'):
        #Conexão com o banco de dados
        self.conn = sqlite3.connect('bancoDeDados.db')
            
        #Criação do cursor
        self.cursor = self.conn.cursor()
    
        #Criação da tabela estoque
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS estoque (
                        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        quantidade INTEGER NOT NULL,
                        valor REAL NOT NULL,
                        categoria TEXT NOT NULL,
                        fab_mari TEXT NOT NULL
                        )
                        """)

        #Criação da tabela cliente
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS cliente (
                        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT UNIQUE,
                        telefone TEXT NOT NULL,
                        endereco TEXT NOT NULL,
                        username TEXT NOT NULL,
                        senha TEXT NOT NULL
                    )
                        """)

        #Criação da tabela vendedor
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS vendedor (
                        id_vendedor INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT UNIQUE,
                        telefone TEXT NOT NULL,
                        username TEXT NOT NULL,
                        senha TEXT NOT NULL
                        )
                        """)
                        
        #Criação da tabela venda
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS venda (
                        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER NOT NULL,
                        id_item INTEGER NOT NULL,
                        id_vendedor INTEGER NOT NULL,
                        valor REAL NOT NULL,    
                        data DATE NOT NULL,
                        descricao TEXT,
                        tipo_pagamento TEXT,
                        FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente),
                        FOREIGN KEY (id_vendedor) REFERENCES vendedor (id_vendedor),
                        FOREIGN KEY (id_item) REFERENCES estoque (id_produto)
                        )
                        """)
        # O ForeignKey é uma chave estrangeira que faz referência a chave primária da tabela cliente

    #Método para inserir um novo cliente na tabela de clientes
    def inserir_cliente(self, nome, email, telefone, endereco, username, senha):
        # Método para inserir um novo cliente na tabela de clientes
        try:
            if nome == '' or telefone == '' or endereco == '':
                print('Nome, telefone e endereço são campos obrigatórios.')
            else:
                cliente = Cliente(nome, email, telefone, endereco, username, senha)
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
                print("\033c")
                print(f'ID: {cliente[0]}, Nome: {cliente[1]}, Email: {cliente[2]}, Telefone: {cliente[3]}, Endereço: {cliente[4]}')
        except sqlite3.Error as e:
            print('Erro ao listar clientes')
    
    # Método para inserir uma nova venda na tabela
    def inserir_venda(self, username_cliente, data, descricao, tipo_pagamento, nome_produto, username_vendedor, senha_vendedor):
        # Método para inserir uma nova venda na tabela
        try:
            #pegar o id do cliente
            id_cliente = self.buscar_cliente_por_username(username_cliente)
            cliente_existente = self.buscar_cliente(id_cliente)    
            valor = self.buscar_valor_produto(nome_produto)
            id_item = self.buscar_produto_por_nome(nome_produto)
            data = data.replace('/', '-')
            data = datetime.strptime(data, '%d-%m-%Y').strftime('%Y-%m-%d')
            verificar_login_vendedor = self.verificar_login_vendedor(username_vendedor, senha_vendedor)
            if verificar_login_vendedor:
                id_vendedor = self.buscar_vendedor_por_username(username_vendedor)
            else:
                print('Vendedor não encontrado')
                return
            
            
            if cliente_existente:
                self.cursor.execute("""
                    INSERT INTO venda (id_cliente, id_item, id_vendedor, valor, data, descricao, tipo_pagamento)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (id_cliente, id_item, id_vendedor, valor, data, descricao, tipo_pagamento))
                self.conn.commit()
                print(f'Venda cadastrada com sucesso!')
                self.diminuir_quantidade_produto(id_item)
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
                    print("\033c")
                    print(f'Valor: {compra[1]}, Data: {compra[2]}, Descrição: {compra[3]}')
                    valor = sum(compra[1] for compra in compras)
            else:
                print("\033c")
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
                print("\033c")
                print(f'Clientes encontrados com o nome contendo "{nome}":')
                for cliente in clientes_encontrados:
                    print(f'ID: {cliente[0]}, Nome: {cliente[1]}, Email: {cliente[2]}, Telefone: {cliente[3]}, Endereço: {cliente[4]}')
            else:
                print("\033c")
                print(f'Nenhum cliente encontrado com o nome contendo "{nome}".')

        except sqlite3.Error as e:
            print(f'Erro ao pesquisar clientes por nome: {e}')

    # Método para fechar a conexão com o banco de dados
    def fechar_conexao(self):
        print('Fechando conexão com o banco de dados...')
        self.conn.close()

    #metodo para verificar login do cliente
    def verificar_login_cliente(self, username, senha):
        try:
            self.cursor.execute("""
                SELECT * FROM cliente
                WHERE username = ? AND senha = ?
            """, (username, senha))
            cliente = self.cursor.fetchone()
            if cliente:
                print(f'\n\nBem-vindo, {cliente[1]}!')
                return True
            else:
                return False
        except sqlite3.Error as e:
            print('Erro ao verificar login do cliente')

    #Metodo para verificar login do vendedor
    def verificar_login_vendedor(self, username, senha):
        try:
            self.cursor.execute("""
                SELECT * FROM vendedor
                WHERE username = ? AND senha = ?
            """, (username, senha))
            vendedor = self.cursor.fetchone()
            if vendedor:
                print(f'\n\nBem-vindo, {vendedor[1]}!')
                return True
            else:
                return False
        except sqlite3.Error as e:
            print('Erro ao verificar login do vendedor')
    
    # Método para vizualizar o estoque
    def visualizar_estoque(self):
        try:
            self.cursor.execute("""
                SELECT * FROM estoque
            """)
            produtos = self.cursor.fetchall()
            print('\nEstoque:')
            for produto in produtos:
                print(f'Nome: {produto[1]}, Quantidade: {produto[2]}, Valor: R${produto[3]}, Categoria: {produto[4]}, Fabricante: {"Sem fabricante" if produto[5] == "não" else "Feito por Mari"}')
        except sqlite3.Error as e:
            print('Erro ao visualizar estoque')
        
    #Metodo para  buscar os itens  fabricados por Mari
    def buscar_item_fab_mari(self):
        try:
            self.cursor.execute("""
                CREATE VIEW IF NOT EXISTS produtos_fabricados AS
                SELECT * FROM estoque
                WHERE fab_mari = 'sim'
            """)
            self.cursor.execute("""
                SELECT * FROM produtos_fabricados
            """)
            produtos = self.cursor.fetchall()
            print('\nProdutos fabricados por Mari:')
            for produto in produtos:
                print(f'Nome: {produto[1]}, Quantidade: {produto[2]}, Valor: R${produto[3]}, Categoria: {produto[4]}')
        except sqlite3.Error as e:
            print('Erro ao buscar itens fabricados por Mari')
    
    #Método para buscar produtos por categoria
    def buscar_item_categoria(self, categoria):
        try:
            self.cursor.execute("""
                SELECT * FROM estoque
                WHERE categoria = ?
            """, (categoria,))
            produtos = self.cursor.fetchall()
            print(f'\nProdutos da categoria {categoria}:')
            for produto in produtos:
                print(f'Nome: {produto[1]}, Quantidade: {produto[2]}, Valor: R${produto[3]}, Fabricante: {"Sem fabricante" if produto[5] == "não" else "Feito por Mari"}')
        except sqlite3.Error as e:
            print('Erro ao buscar produtos por categoria')
    
    #Método para buscar produtos por preço
    def buscar_item_preco(self, preco):
        try:
            self.cursor.execute("""
                SELECT * FROM estoque
                WHERE valor <= ?
            """, (preco,))
            produtos = self.cursor.fetchall()
            print(f'\nProdutos com preço menor que R${preco}:')
            for produto in produtos:
                print(f'Nome: {produto[1]}, Quantidade: {produto[2]}, Valor: R${produto[3]}, Categoria: {produto[4]}, Fabricante: {"Sem fabricante" if produto[5] == "não" else "Feito por Mari"}')
        except sqlite3.Error as e:
            print('Erro ao buscar produtos por preço')

    #Método para buscar produtos por nome
    def buscar_item_nome(self, nome):
        try:
            self.cursor.execute("""
                SELECT * FROM estoque
                WHERE nome LIKE '%' || ? || '%'
            """, (nome,))
            produtos = self.cursor.fetchall()
            print(f'\nProdutos com nome contendo "{nome}":')
            for produto in produtos:
                print(f'Nome: {produto[1]}, Quantidade: {produto[2]}, Valor: R${produto[3]}, Categoria: {produto[4]}, Fabricante: {"Sem fabricante" if produto[5] == "não" else "Feito por Mari"}')
        except sqlite3.Error as e:
            print('Erro ao buscar produtos por nome')

    #Metodo para verificar se tem o produto no estoque
    def verificar_produto(self, id_produto):
        try:
            self.cursor.execute("""
                SELECT * FROM estoque
                WHERE id_produto = ? AND quantidade > 0
            """, (id_produto,))
            produto = self.cursor.fetchone()
            if produto:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print('Erro ao verificar produto')
            return False
    
    #Metodo para buscar cliente por username e retornar o id
    def buscar_cliente_por_username(self, username):
        try:
            self.cursor.execute("""
                SELECT id_cliente FROM cliente
                WHERE username = ?
            """, (username,))
            cliente = self.cursor.fetchone()
            if cliente:
                return cliente[0]
            else:
                return None
        except sqlite3.Error as e:
            print('Erro ao buscar cliente por username')
            return None

    #Metodo para retornar o valor do produto partindo do nome
    def buscar_valor_produto(self, nome):
        try:
            self.cursor.execute("""
                SELECT valor FROM estoque
                WHERE nome = ?
            """, (nome,))
            produto = self.cursor.fetchone()
            if produto:
                return produto[0]
            else:
                return None
        except sqlite3.Error as e:
            print('Erro ao buscar valor do produto')
            return None

    #Método para buscar produto por nome e retornar o id
    def buscar_produto_por_nome(self, nome):
        try:
            self.cursor.execute("""
                SELECT id_produto FROM estoque
                WHERE nome = ?
            """, (nome,))
            produto = self.cursor.fetchone()
            if produto:
                return produto[0]
            else:
                return None
        except sqlite3.Error as e:
            print('Erro ao buscar produto por nome')
            return None
    
    #Metodo para bucar id do vendedor por username
    def buscar_vendedor_por_username(self, username):
        try:
            self.cursor.execute("""
                SELECT id_vendedor FROM vendedor
                WHERE username = ?
            """, (username,))
            vendedor = self.cursor.fetchone()
            if vendedor:
                return vendedor[0]
            else:
                return None
        except sqlite3.Error as e:
            print('Erro ao buscar vendedor por username')
            return None
    
    #metodo para dimunuir a quantidade do produto
    def diminuir_quantidade_produto(self, id_produto):
        try:
            self.cursor.execute("""
                UPDATE estoque
                SET quantidade = quantidade - 1
                WHERE id_produto = ?
            """, (id_produto,))
            self.conn.commit()
        except sqlite3.Error as e:
            print('Erro ao diminuir quantidade do produto')