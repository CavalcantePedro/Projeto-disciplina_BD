import sisCrud

#Interface do vendedor 
def interface_vendedor(GerenciadorCRUD):
    gerenciador = GerenciadorCRUD
    while True:
        # Exibição do menu de opções para o usuário
        print("\n===== Cliente =====")
        print("1. Inserir Cliente")
        print("2. Alterar Cliente")
        print("3. Remover Cliente")
        print("4. Listar Todos os Clientes")
        print("5. Listar clientes e seus ids por nome")
        print("\n===== Venda =====")
        print("7. Exibir Vendas por Cliente")
        print("8. Gerar Relatório de Vendas do Mês atual")
        print("9. Gerar Relatório Vendas do Ano atual")
        print("10. Gerar Relatório de Vendas do dia atual")
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

def interface_cliente(GerenciadorCRUD):
    gerenciador = GerenciadorCRUD
    while True:
        # Exibição do menu de opções para o usuário
        print("\n======= Seja bem vindo ao NAUTICO's shop =======")
        print("1. Ver estoque de todos produtos")
        print("2. Ver produtos por categoria")
        print("3. Ver produtos por preço")
        print("4. Ver produtos frabricados por Mari")
        print("5. Ver produtos por nome")
        print("6. Realizar compra")
        print("7. Alterar cadastro")
        print("\n===== Voltar =====")
        print("0. Voltar")

        # Solicitação da escolha do usuário
        escolha = input("\nEscolha uma opção: \n")
        if escolha == "0":
            print("\033c")
            break
        elif escolha == "1":
            print("\033c")
            gerenciador.visualizar_estoque()
        elif escolha == "2":
            print("\033c")
            print("Categorias disponíveis:")
            print("1. Perecíveis")
            print("2. Não Perecíveis")
            input_categoria = input("Escolha uma categoria: ")
            gerenciador.buscar_item_categoria('per' if input_categoria == "1" else "n_per")
        elif escolha == "3":
            print("\033c")
            print("Deseja ver produtos menores que qual valor?")
            input_preco = input("Digite o valor: ")
            input_preco = input_preco.replace(",", ".")
            input_preco = float(input_preco)
            gerenciador.buscar_item_preco(input_preco)
        elif escolha == "4":
            print("\033c")
            gerenciador.buscar_item_fab_mari()
        elif escolha == "5":
            print("\033c")
            print("Digite o nome do produto:")
            input_nome = input("Nome: ")
            gerenciador.buscar_item_nome(input_nome)
        elif escolha == "6":
            print("\033c")
            # Inserir Venda:
            username = input("Digite seu username : ")
            data = input("Data da venda (formato DD/MM/AAAA): ")
            descricao = input("Descrição da venda: ")            
            print("1. Cartão de Crédito")
            print("2. Cartão de Débito")
            print("3. Dinheiro/Pix")
            input_pagamento = input("Escollha o metodo de pagamento:")
            if input_pagamento == "1":
                input_pagamento = "Credito"
            elif input_pagamento == "2":
                input_pagamento = "Debito"
            else:
                input_pagamento = "Dinheiro/Pix"
            nome_do_produto = input("Digite o nome do produto: ")
            print("\033c")
            print("Para confirmar a compra, insira seu username e senha de vendedor.")
            username_vendedor = input("Username: ")
            senha_vendedor = input("Senha: ")
            print("\033c")
            gerenciador.inserir_venda(username, data, descricao, input_pagamento, nome_do_produto, username_vendedor, senha_vendedor)
            
def interface_menu(GerenciadorCRUD):
    gerenciador = GerenciadorCRUD
    while True:
        # Exibição do menu de opções para o usuário
        print("\n======= Entrar como: =======")
        print("1. Vendedor")
        print("2. Cliente")
        print("3. Visitante")
        print("Ps: O visitante pode apenas visualizar os produtos e não pode realizar compras.")
        print("\n===== Sair =====")
        print("0. Sair")

        # Solicitação da escolha do usuário
        escolha = input("\nEscolha uma opção: \n")
        if escolha == "0":
            break
        elif escolha == "1":
            # limpar a saída do console
            print("\033c")
            username = input("Username: ")
            senha = input("Senha: ")
            print("\033c")
            if gerenciador.verificar_login_vendedor(username, senha):
                interface_vendedor(gerenciador)
            else:
                print("\033c")
                print("Usuário ou senha incorretos.")
        elif escolha == "2":
            # limpar a saída do console
            print("\033c")
            username = input("Username: ")
            senha = input("Senha: ")
            print("\033c")
            if gerenciador.verificar_login_cliente(username, senha):
                interface_cliente(gerenciador)
            else:
                print("\033c")
                print("Usuário ou senha incorretos.")
        elif escolha == "3":
            # limpar a saída do console
            print("\033c")
            gerenciador.visualizar_estoque()
# Função principal para interação com o usuário via terminal
def main():
    # Criação de uma instância do GerenciadorCRUD
    gerenciador = sisCrud.GerenciadorCRUD()
    # Interface do menu
    interface_menu(gerenciador)
    gerenciador.fechar_conexao()
# Verifica se o script está sendo executado diretamente (não importado como um módulo)
if __name__ == "__main__":
    # Chama a função principal para iniciar a interação com o usuário
    main()