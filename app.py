import sqlite3  # Importa a biblioteca padrão do Python para gerenciamento de bancos de dados SQLite

DB_NAME = "lg_moda.db"  # Define em uma constante global o nome do arquivo físico de banco de dados que será gerenciado


def inicializar_banco():  # Cria a função responsável por criar as tabelas estruturais internas
    """Garante a criação apenas da tabela de histórico de IMC dentro do banco de dados lg_moda.db."""
    conexao = sqlite3.connect(
        DB_NAME
    )  # Abre uma conexão direta com o arquivo lg_moda.db (ele é criado automaticamente se não existir)
    cursor = (
        conexao.cursor()
    )  # Cria o objeto cursor, necessário para trafegar e executar comandos SQL no banco

    # Executa o comando SQL para criar a tabela de IMC, caso ela ainda não tenha sido mapeada no banco de dados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_imc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            peso REAL,
            altura REAL,
            imc REAL,
            classificacao TEXT,
            data_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.commit()  # Confirma a gravação permanente da estrutura da tabela no arquivo de banco de dados
    conexao.close()  # Fecha a conexão para liberar o arquivo e não travar a memória do sistema


def calcular_imc(peso, altura):  # Cria a função pura para o cálculo matemático
    """Realiza a fórmula matemática clássica do IMC."""
    return peso / (
        altura**2
    )  # Retorna o resultado da divisão do peso pelo quadrado da altura (altura multiplicada por ela mesma)


def classificar_imc(imc):  # Cria a função pura para rotular o IMC por escrito
    """Retorna a classificação oficial do IMC com base nas faixas da OMS."""
    if imc < 18.5:  # Condição para nota abaixo do recomendado
        return "Abaixo do peso"  # Retorna o diagnóstico por extenso
    elif 18.5 <= imc < 25:  # Condição para faixa perfeita de peso ideal
        return "Peso normal"  # Retorna o diagnóstico por extenso
    elif 25 <= imc < 30:  # Condição para sobrepeso inicial
        return "Sobrepeso"  # Retorna o diagnóstico por extenso
    elif 30 <= imc < 35:  # Condição para início de obesidade crônica
        return "Obesidade Grau 1"  # Retorna o diagnóstico por extenso
    elif 35 <= imc < 40:  # Condição para obesidade severa de segundo nível
        return "Obesidade Grau 2"  # Retorna o diagnóstico por extenso
    else:  # Caso o número extrapole todas as barreiras anteriores
        return (
            "Obesidade Grau 3 (Mórbida)"  # Retorna o diagnóstico de risco alto
        )


def salvar_imc_no_banco(
    peso, altura
):  # Cria a função que junta os cálculos e faz o registro no arquivo .db
    """Calcula o IMC, classifica e grava o registro definitivo no banco de dados."""
    try:  # Abre um bloco de monitoramento contra erros inesperados
        imc_calculado = calcular_imc(
            peso, altura
        )  # Aciona a função de cálculo matemático enviando os parâmetros digitados
        status_imc = classificar_imc(
            imc_calculado
        )  # Aciona a função classificatória para descobrir o texto do status
        imc_arredondado = round(
            imc_calculado, 2
        )  # Arredonda o valor decimal do IMC em apenas duas casas de precisão

        conexao = sqlite3.connect(
            DB_NAME
        )  # Conecta no banco de dados local para iniciar a transação de dados
        cursor = (
            conexao.cursor()
        )  # Instancia o controlador de escrita sql do banco de dados

        # Executa o comando de inserção protegendo as variáveis usando interrogações contra ataques ou erros de aspas
        cursor.execute(
            """
            INSERT INTO historico_imc (peso, altura, imc, classificacao)
            VALUES (?, ?, ?, ?)
        """,
            (peso, altura, imc_arredondado, status_imc),
        )

        conexao.commit()  # Valida a gravação da nova linha na tabela do arquivo de forma definitiva
        conexao.close()  # Desliga do banco de dados de maneira limpa e segura

        print(
            f"\n[SUCESSO] IMC de {imc_arredondado} ({status_imc}) salvo no banco!"
        )  # Emite mensagem verde de sucesso no terminal informando os valores gerados

    except (
        Exception
    ) as e:  # Caso ocorra alguma queda de permissão ou falha no disco durante a gravação
        print(
            f"\n[ERRO] Não foi possível salvar no banco: {e}"
        )  # Avisa o desenvolvedor exibindo o código de erro do sistema operacional


def exibir_historico():  # Cria a função responsável por ler e mostrar os dados cadastrados
    """Busca e lista no terminal todos os recordes de IMC salvos até o momento."""
    conexao = sqlite3.connect(
        DB_NAME
    )  # Abre conexão de leitura com o banco de dados lg_moda.db
    cursor = conexao.cursor()  # Prepara o leitor sql

    print(
        "\n" + "=" * 50
    )  # Imprime uma linha de caracteres de igual para fazer uma divisória elegante no console
    print(
        "           HISTÓRICO DE IMC NO BANCO"
    )  # Imprime o cabeçalho do relatório impresso em tela
    print(
        "=" * 50
    )  # Imprime a linha inferior de fechamento do cabeçalho do relatório

    cursor.execute(
        "SELECT id, peso, altura, imc, classificacao, data_registro FROM historico_imc"
    )  # Dispara comando sql buscando todas as colunas ordenadas da tabela
    registros = (
        cursor.fetchall()
    )  # Captura todas as linhas encontradas no banco e armazena em formato de lista na variável

    if (
        not registros
    ):  # Caso a lista tenha vindo totalmente vazia (banco recém criado)
        print(
            "Nenhum registro encontrado."
        )  # Escreve o aviso de banco zerado na tela
    else:  # Caso existam registros cadastrados anteriores
        for linha in registros:  # Inicia um laço de repetição para varrer e imprimir uma linha por vez
            print(
                f"ID: {linha[0]} | Peso: {linha[1]}kg | Altura: {linha[2]}m | IMC: {linha[3]} | Status: {linha[4]} | Data: {linha[5]}"
            )  # Imprime os campos formatados separando-os com barras verticais

    print(
        "=" * 50 + "\n"
    )  # Imprime a linha divisória final de encerramento do relatório no terminal
    conexao.close()  # Fecha a conexão de leitura com o banco liberando o arquivo


# BLOCO PRINCIPAL DE ENTRADA DO ARQUIVO PYTHON (MENU INTERATIVO)
if (
    __name__ == "__main__"
):  # Verifica se o script está sendo executado diretamente pelo terminal do usuário
    inicializar_banco()  # Executa a função inicial para garantir que a tabela esteja de pé e pronta no arquivo .db

    while (
        True
    ):  # Inicia um laço de repetição infinito para manter o menu do terminal rodando sem fechar sozinho
        print("--- MENU DE IMC (lg_moda.db) ---")  # Título principal do menu
        print(
            "1. Calcular Novo IMC e Salvar no Banco"
        )  # Opção para executar cálculo e salvar no .db
        print(
            "2. Ver Histórico de IMC"
        )  # Opção para puxar relatório das linhas existentes
        print("3. Sair")  # Opção para interromper o terminal e fechar o programa

        opcao = (
            input("Escolha uma opção (1/2/3): ").strip()
        )  # Recebe a resposta digitada pelo usuário e limpa espaços extras nas pontas

        if (
            opcao == "1"
        ):  # Se a escolha digitada no console foi correspondente ao item 1
            try:  # Abre bloco contra erros de digitação de letras em campos numéricos
                p = float(
                    input("Digite o peso em kg (Ex: 75.4): ")
                )  # Recebe o peso digitado pelo terminal e converte para número de ponto flutuante
                a = float(
                    input("Digite a altura em metros (Ex: 1.75): ")
                )  # Recebe a altura digitada pelo terminal e converte para número de ponto flutuante
                if (
                    p > 0 and a > 0
                ):  # Validação de segurança para impedir a entrada de números negativos ou zero
                    salvar_imc_no_banco(
                        p, a
                    )  # Envia os dados numéricos válidos obtidos para a função de cálculo e gravação
                else:  # Caso o usuário tenha digitado um peso ou altura menor ou igual a zero
                    print(
                        "\n[ERRO] Os valores precisam ser maiores que zero.\n"
                    )  # Exibe notificação de erro matemático no console
            except (
                ValueError
            ):  # Captura erro caso o usuário tente digitar letras ou usar vírgulas em vez de pontos nos inputs decimais
                print(
                    "\n[ERRO] Por favor, digite números válidos usando ponto para decimais.\n"
                )  # Orienta a digitação correta no terminal

        elif (
            opcao == "2"
        ):  # Se a escolha digitada no console foi correspondente ao item 2
            exibir_historico()  # Executa o leitor interno sql que lista o banco na tela

        elif (
            opcao == "3"
        ):  # Se a escolha digitada no console foi correspondente ao item 3
            print(
                "\nSaindo do programa..."
            )  # Mostra um aviso informando o desligamento planejado
            break  # Quebra o laço de repetição infinito (While True), finalizando a execução do script Python
        else:  # Caso o usuário digite qualquer caractere diferente de 1, 2 ou 3
            print(
                "\nOpção inválida. Tente novamente.\n"
            )  # Informa o erro de seleção de menu para o usuário tentar novamente