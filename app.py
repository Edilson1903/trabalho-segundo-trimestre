import sqlite3

DB_NAME = "lg_moda.db"

def inicializar_banco():
    """
    Garante a criação apenas da tabela de histórico de IMC 
    dentro do banco de dados lg_moda.db.
    """
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    
    # Cria a tabela de IMC caso ela não exista
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
    
    conexao.commit()
    conexao.close()


def calcular_imc(peso, altura):
    """Realiza a fórmula matemática do IMC."""
    return peso / (altura ** 2)


def classificar_imc(imc):
    """Retorna a classificação oficial do IMC com base nas faixas da OMS."""
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 25:
        return "Peso normal"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    elif 30 <= imc < 35:
        return "Obesidade Grau 1"
    elif 35 <= imc < 40:
        return "Obesidade Grau 2"
    else:
        return "Obesidade Grau 3 (Mórbida)"


def salvar_imc_no_banco(peso, altura):
    """Calcula o IMC, classifica e grava o registro no banco de dados."""
    try:
        imc_calculado = calcular_imc(peso, altura)
        status_imc = classificar_imc(imc_calculado)
        imc_arredondado = round(imc_calculado, 2)
        
        # Conecta e insere no banco de dados lg_moda.db
        conexao = sqlite3.connect(DB_NAME)
        cursor = conexao.cursor()
        
        cursor.execute("""
            INSERT INTO historico_imc (peso, altura, imc, classificacao)
            VALUES (?, ?, ?, ?)
        """, (peso, altura, imc_arredondado, status_imc))
        
        conexao.commit()
        conexao.close()
        
        print(f"\n[SUCESSO] IMC de {imc_arredondado} ({status_imc}) salvo no banco!")
        
    except Exception as e:
        print(f"\n[ERRO] Não foi possível salvar no banco: {e}")


def exibir_historico():
    """Busca e lista no terminal todos os recordes de IMC salvos."""
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    
    print("\n" + "="*50)
    print("           HISTÓRICO DE IMC NO BANCO")
    print("="*50)
    
    cursor.execute("SELECT id, peso, altura, imc, classificacao, data_registro FROM historico_imc")
    registros = cursor.fetchall()
    
    if not registros:
        print("Nenhum registro encontrado.")
    else:
        for linha in registros:
            print(f"ID: {linha[0]} | Peso: {linha[1]}kg | Altura: {linha[2]}m | IMC: {linha[3]} | Status: {linha[4]} | Data: {linha[5]}")
            
    print("="*50 + "\n")
    conexao.close()


# Execução do script interativo no terminal
if __name__ == '__main__':
    # Garante que a tabela exista
    inicializar_banco()
    
    while True:
        print("--- MENU DE IMC (lg_moda.db) ---")
        print("1. Calcular Novo IMC e Salvar no Banco")
        print("2. Ver Histórico de IMC")
        print("3. Sair")
        
        opcao = input("Escolha uma opção (1/2/3): ").strip()
        
        if opcao == "1":
            try:
                p = float(input("Digite o peso em kg (Ex: 75.4): "))
                a = float(input("Digite a altura em metros (Ex: 1.75): "))
                if p > 0 and a > 0:
                    salvar_imc_no_banco(p, a)
                else:
                    print("\n[ERRO] Os valores precisam ser maiores que zero.\n")
            except ValueError:
                print("\n[ERRO] Por favor, digite números válidos usando ponto para decimais.\n")
                
        elif opcao == "2":
            exibir_historico()
            
        elif opcao == "3":
            print("\nSaindo do programa...")
            break
        else:
            print("\nOpção inválida. Tente novamente.\n")