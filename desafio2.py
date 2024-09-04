import textwrap

def exibir_menu():
    """
    Exibe o menu de opções do sistema.
    """
    menu = """\n
    =============== MENU ================
    [d]\t Depositar
    [s]\t Sacar
    [e]\t Extrato
    [nc]\t Nova conta
    [lc]\t Listar contas
    [nu]\t Novo usuário
    [lu]\t Listar usuários
    [q]\t Sair
    => """
    return input(textwrap.dedent(menu))

def validar_cpf(cpf):
    """
    Valida se o CPF possui exatamente 11 números.
    """
    if len(cpf) != 11 or not cpf.isdigit():
        print("CPF inválido! O CPF deve conter exatamente 11 números.")
        return False
    return True

def depositar(saldo, valor, extrato, /):
    """
    Realiza o depósito em uma conta, adicionando o valor ao saldo e registrando no extrato.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R${valor:.2f}\n"
        print("\nDepósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza um saque de uma conta, verificando saldo, limite e número de saques permitidos.
    """
    excede_saldo = valor > saldo
    excede_limite = valor > limite
    excede_saques = numero_saques >= limite_saques

    if excede_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excede_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excede_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    """
    Cria um novo usuário (cliente) no sistema, validando o CPF e obrigando a inserção do nome.
    """
    cpf = input("Informe o CPF (somente o número): ")
    if not validar_cpf(cpf):
        return

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ").strip()
    if not nome:
        print("O nome é obrigatório!")
        return

    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    """
    Filtra a lista de usuários para encontrar um cliente com o CPF fornecido.
    """
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios, contas):
    """
    Cria uma nova conta corrente para um usuário existente no sistema, vinculando ao CPF.
    """
    cpf = input("Informe o CPF do usuário: ")
    if not validar_cpf(cpf):
        return None

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\nConta criada com sucesso!")
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": "", "numero_saques": 0}
        contas.append(conta)
        return conta

    print("Usuário não encontrado, fluxo de criação de conta encerrado!")
    return None

def encontrar_conta(cpf, contas):
    """
    Encontra uma conta associada ao CPF fornecido.
    """
    for conta in contas:
        if conta['usuario']['cpf'] == cpf:
            return conta
    return None

def listar_contas(contas):
    """
    Lista todas as contas cadastradas no sistema.
    """
    if not contas:
        print("\nNão há contas cadastradas.")
    else:
        for conta in contas:
            linha = f"""\
                        Agência:\t{conta['agencia']}
                        C/C:\t\t{conta['numero_conta']}
                        Titular:\t{conta['usuario']['nome']}
                    """
            print("=" * 100)
            print(textwrap.dedent(linha))

def listar_usuarios(usuarios):
    """
    Lista todos os usuários cadastrados no sistema.
    """
    if not usuarios:
        print("\nNão há usuários cadastrados.")
    else:
        for usuario in usuarios:
            linha = f"""\
                    CPF:\t{usuario['cpf']}
                    Nome:\t\t{usuario['nome']}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

def main():
    """
    Função principal que gerencia o fluxo do sistema bancário, com opções de depósito, saque, extrato e gerenciamento de contas e usuários.
    """
    limite_saques = 3
    agencia_padrao = "0001"

    usuarios = []
    contas = []
    numero_conta = 1
    saudacao_exibida = False  # Para controlar a exibição da saudação

    while True:
        if not saudacao_exibida:
            print("\nBem-vindo ao sistema bancário!")
            saudacao_exibida = True

        opcao = exibir_menu()

        if opcao == "d":
            cpf = input("Informe o CPF para depósito: ")
            if validar_cpf(cpf):
                conta = encontrar_conta(cpf, contas)
                if conta:
                    valor = float(input("Informe o valor do depósito: "))
                    conta['saldo'], conta['extrato'] = depositar(conta['saldo'], valor, conta['extrato'])
                else:
                    print("Conta não encontrada. Crie uma conta primeiro.")

        elif opcao == "s":
            cpf = input("Informe o CPF para saque: ")
            if validar_cpf(cpf):
                conta = encontrar_conta(cpf, contas)
                if conta:
                    valor = float(input("Informe o valor do saque: "))
                    conta['saldo'], conta['extrato'], conta['numero_saques'] = sacar(
                        saldo=conta['saldo'],
                        valor=valor,
                        extrato=conta['extrato'],
                        limite=500,
                        numero_saques=conta['numero_saques'],
                        limite_saques=limite_saques,
                    )
                else:
                    print("Conta não encontrada. Crie uma conta primeiro.")

        elif opcao == "e":
            cpf = input("Informe o CPF para consultar o extrato: ")
            if validar_cpf(cpf):
                conta = encontrar_conta(cpf, contas)
                if conta:
                    exibir_extrato(conta['saldo'], extrato=conta['extrato'])
                else:
                    print("Conta não encontrada. Crie uma conta primeiro.")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(agencia_padrao, numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "q":
            print("\nObrigado por utilizar nossos serviços! Até logo.")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
