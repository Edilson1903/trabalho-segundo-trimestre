from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# Inicializa o aplicativo Flask para gerenciar as rotas do servidor web
app = Flask(__name__)

# Ativa o CORS para que seu index.html converse com o Python sem bloqueios de segurança
CORS(app)

# Nome do arquivo de Banco de Dados que você possui na barra lateral do VS Code
DB_NAME = "lg_moda.db"

# =====================================================================
# CONFIGURAÇÃO INICIAL DO BANCO DE DADOS (DATABASE)
# =====================================================================
def inicializar_banco():
    """
    Função que conecta ao lg_moda.db e cria as tabelas de histórico de IMC 
    e Ficha de Academia caso elas ainda não existam no banco.
    """
    # Abre a conexão com o banco de dados
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    
    # Criação da tabela para salvar os cálculos de IMC
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
    
    # Criação da tabela para salvar os dados da anamnese/academia
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ficha_academia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cardiaco TEXT,
            alergias TEXT,
            doencas TEXT,
            tempo TEXT,
            dias TEXT,
            data_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Salva as alterações e fecha a conexão com segurança
    conexao.commit()
    conexao.close()

# Executa a inicialização do banco ao rodar o app.py
inicializar_banco()


# =====================================================================
# LÓGICA DE NEGÓCIO (CÁLCULOS E CLASSIFICAÇÕES)
# =====================================================================
def calcular_imc(peso, altura):
    """Calcula o IMC: peso dividido por altura ao quadrado."""
    return peso / (altura ** 2)

def classificar_imc(imc):
    """Retorna o texto de classificação e a classe de cor correspondente para o CSS."""
    if imc < 18.5:
        return {"texto": "Abaixo do peso", "classe": "alerta"}
    elif 18.5 <= imc < 25:
        return {"texto": "Peso normal (parabéns!)", "classe": "normal"}
    elif 25 <= imc < 30:
        return {"texto": "Sobrepeso", "classe": "alerta"}
    elif 30 <= imc < 35:
        return {"texto": "Obesidade Grau 1", "classe": "perigo"}
    elif 35 <= imc < 40:
        return {"texto": "Obesidade Grau 2", "classe": "perigo"}
    else:
        return {"texto": "Obesidade Grau 3 (mórbida)", "classe": "perigo"}


# =====================================================================
# ROTAS DA API QUE SALVAM DIRETAMENTE NO BANCO DE DADOS
# =====================================================================

@app.route('/api/imc', methods=['POST'])
def api_imc():
    """Recebe peso e altura, calcula o IMC, grava no Banco de Dados e retorna o valor."""
    try:
        dados = request.get_json()
        peso = float(dados.get('peso'))
        altura = float(dados.get('altura'))
        
        # Realiza os cálculos lógicos no Python
        resultado_imc = calcular_imc(peso, altura)
        classificacao = classificar_imc(resultado_imc)
        
        # --- OPERAÇÃO DE BANCO DE DADOS (INSERT) ---
        conexao = sqlite3.connect(DB_NAME)
        cursor = conexao.cursor()
        
        # Insere o registro na tabela 'historico_imc'
        cursor.execute("""
            INSERT INTO historico_imc (peso, altura, imc, classificacao)
            VALUES (?, ?, ?, ?)
        """, (peso, altura, round(resultado_imc, 2), classificacao["texto"]))
        
        conexao.commit()
        conexao.close()
        
        # O jsonify envia a resposta de volta confirmando que deu certo
        return jsonify({
            "status": "sucesso",
            "imc": round(resultado_imc, 2),
            "classificacao": classificacao["texto"],
            "classe_css": classificacao["classe"]
        })
    except (ValueError, TypeError):
        return jsonify({"status": "erro", "mensagem": "Dados de IMC inválidos."}), 400


@app.route('/api/ficha', methods=['POST'])
def api_ficha():
    """Recebe a anamnese da academia do HTML e grava diretamente no Banco de Dados."""
    try:
        dados = request.get_json()
        
        # Captura e higieniza as respostas do formulário
        cardiaco = dados.get('cardiaco', 'Não')
        alergias = dados.get('alergias', '').strip() or "Nenhuma informada"
        doencas = dados.get('doencas', '').strip() or "Nenhuma informada"
        tempo = dados.get('tempo', '')
        dias = dados.get('dias', '')
        
        # --- OPERAÇÃO DE BANCO DE DADOS (INSERT) ---
        conexao = sqlite3.connect(DB_NAME)
        cursor = conexao.cursor()
        
        # Insere as respostas na tabela 'ficha_academia'
        # CORRIGIDO: Variável 'alergias' mapeada corretamente sem erros de digitação
        cursor.execute("""
            INSERT INTO ficha_academia (cardiaco, allergies, doencas, tempo, dias)
            VALUES (?, ?, ?, ?, ?)
        """, (cardiaco, alergias, doencas, tempo, dias))
        
        conexao.commit()
        conexao.close()
        
        # Retorna o JSON de sucesso para o navegador renderizar a resposta na tela
        return jsonify({
            "status": "sucesso",
            "mensagem": "Ficha salva com sucesso no banco de dados lg_moda.db!",
            "resumo": {
                "cardiaco": cardiaco,
                "alergias":  alergias,
                "doencas": doencas,
                "tempo": tempo,
                "dias": dias
            }
        })
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": f"Erro interno: {str(e)}"}), 500


# Inicializa o servidor local
if __name__ == '__main__':
    print("\n" + "="*40)
    print("   SERVIDOR PYTHON ATIVO (COM DATABASE)")
    print("   Rodando em: http://127.0.0.1:5000")
    print("="*40 + "\n")
    
    app.run(port=5000, debug=True)