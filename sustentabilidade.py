import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fraccaroli3",
    database="projeto_integrador"
)
cursor = conexao.cursor()

opcao = ""

while opcao != "2":
    print("\n=== Sistema de Monitoramento de Sustentabilidade Pessoal ===")
    print("1 - Ver dados e calcular médias")
    print("2 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cursor.execute("""
            SELECT consumo_agua, consumo_energia, residuos_nao_reciclaveis, residuos_reciclados, transporte_usado 
            FROM Monitoramento_Sustentabilidade
        """)
        dados = cursor.fetchall()

        qtd = 0
        total_agua = 0
        total_energia = 0
        total_residuos_nao_reciclaveis = 0
        total_residuos_reciclados = 0
        transportes = {}

        for registro in dados:
            total_agua += registro[0]
            total_energia += registro[1]
            total_residuos_nao_reciclaveis += registro[2]
            total_residuos_reciclados += registro[3]

            transporte = registro[4]
            if transporte not in transportes:
                transportes[transporte] = 1
            else:
                transportes[transporte] += 1

            qtd = qtd + 1

        if qtd == 0:
            print("\nNenhum dado encontrado.")
        else:
            media_agua = total_agua / qtd
            media_energia = total_energia / qtd
            media_residuos = total_residuos_nao_reciclaveis / qtd
            total_residuos = total_residuos_nao_reciclaveis + total_residuos_reciclados

            if total_residuos == 0:
                percentual_reciclados = 0
            else:
                percentual_reciclados = (total_residuos_reciclados / total_residuos) * 100

            transporte_mais_usado = ""
            maior = 0

            for transporte in transportes:
                if transportes[transporte] > maior:
                    maior = transportes[transporte]
                    transporte_mais_usado = transporte

            if media_agua < 150 and media_energia < 100 and percentual_reciclados > 50:
                classificacao = "Excelente"
            elif media_agua < 200 and media_energia < 150 and percentual_reciclados > 30:
                classificacao = "Bom"
            else:
                classificacao = "Precisa Melhorar"

            print("\n--- Relatório de Sustentabilidade ---")
            print(f"Média de Consumo de Água (L): {media_agua:.2f}")
            print(f"Média de Consumo de Energia (kWh): {media_energia:.2f}")
            print(f"Média de Resíduos Não Recicláveis (Kg): {media_residuos:.2f}")
            print(f"Percentual de Reciclados (%): {percentual_reciclados:.2f}")
            print(f"Transporte mais utilizado (ID): {transporte_mais_usado}")
            print(f"Classificação de Sustentabilidade: {classificacao}")

    elif opcao == "2":
        print("saindo do sistema.")
    else:
        print("Opção inválida.")

cursor.close()
conexao.close()