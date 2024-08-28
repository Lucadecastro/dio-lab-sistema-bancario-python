"""
Este módulo implementa um simples sistema de operações bancárias, permitindo depósitos, saques,
visualização de extratos e uma opção para sair. Ele utiliza um menu interativo para que o
usuário escolha a operação desejada.
"""

MENU = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """


def depositar(saldo, extrato):
    """
    Realiza um depósito na conta.

    Args:
        saldo (float): Saldo atual da conta.
        extrato (str): Histórico das transações.

    Returns:
        tuple: Saldo atualizado e o extrato atualizado.
    """

    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def sacar(saldo, extrato, numero_saques, limite, limite_saques):
    """
    Realiza um saque na conta, respeitando limites de valor e número de saques.

    Args:
        saldo (float): Saldo atual da conta.
        extrato (str): Histórico das transações.
        numero_saques (int): Número de saques já realizados.
        limite (float): Limite de valor por saque.
        limite_saques (int): Limite máximo de saques permitidos.

    Returns:
        tuple: Saldo atualizado, extrato atualizado e o número de saques atualizados.
    """

    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não possui saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Você atingiu o limite de saques diários.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, extrato):
    """
    Exibe o extrato da conta, mostrando todas as transações realizadas.

    Args:
        saldo (float): Saldo atual da conta.
        extrato (str): Histórico das transações.
    """

    print("\n=========== EXTRATO ===========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("===============================")

def main():
    """
    Função principal que controla o fluxo do programa de operações bancárias.
    """

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    limite_saques = 3

    while True:
        opcao = input(MENU)

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(
                saldo, extrato, numero_saques, limite, limite_saques
            )
        elif opcao == "e":
            mostrar_extrato(saldo, extrato)
        elif opcao == "q":
            print("Obrigado por usar o nosso serviço. Tenha um ótimo dia!")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
