# Função para calcular o IMC e retornar a classificação
def calcular_imc(peso, altura):
    # A fórmula do IMC é: peso dividido pela altura ao quadrado
    imc = peso / (altura ** 2)
    return imc

def classificar_imc(imc):
    # Avalia o resultado do IMC com base nas faixas da OMS
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 25:
        return "Peso normal (parabéns!)"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    elif 30 <= imc < 35:
        return "Obesidade Grau 1"
    elif 35 <= imc < 40:
        return "Obesidade Grau 2"
    else:
        return "Obesidade Grau 3 (mórbida)"

# --- Fluxo Principal do Programa ---
print("--- CALCULADORA DE IMC ---")

try:
    # Solicitando os dados do usuário
    # Usamos 'float' para permitir números com casas decimais
    peso = float(input("Digite seu peso em kg (ex: 70.5): "))
    altura = float(input("Digite sua altura em metros (ex: 1.75): "))

    # Executa a função de cálculo
    resultado_imc = calcular_imc(peso, altura)
    
    # Executa a função de classificação
    classificacao = classificar_imc(resultado_imc)

    # Exibe os resultados formatados
    # O ':.2f' serve para arredondar o IMC para duas casas decimais
    print("\n--- RESULTADO ---")
    print(f"Seu IMC é: {resultado_imc:.2f}")
    print(f"Classificação: {classificacao}")

except ValueError:
    # Caso o usuário digite texto em vez de números ou use vírgula ao invés de ponto
    print("\nErro: Por favor, digite números válidos. Use ponto (.) para casas decimais.")