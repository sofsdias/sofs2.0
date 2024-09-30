from flask import Flask, render_template, request
import mysql.connector
import io
import base64
import mammoth
import traceback
from PIL import Image
import os

app = Flask(__name__, template_folder='templates')

# Configuração do banco de dados
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'historia'
}

# Funções definidas antes das rotas

def detect_image_type(image_data):
    """Detecta o tipo de imagem usando Pillow."""
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            return img.format.lower()
    except Exception as e:
        print(f"Erro ao detectar o tipo de imagem: {e}")
        return None

def busca_artigos(pesquisa=None, seculo=None):
    """Busca artigos no banco de dados, opcionalmente filtrando por pesquisa ou século."""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT id, nome_do_autor, titulo, seculo, imagem, artigo, data_criacao FROM artigos"
    conditions = []
    params = []

    if pesquisa:
        conditions.append("(titulo LIKE %s OR nome_do_autor LIKE %s)")
        params.extend(['%' + pesquisa + '%', '%' + pesquisa + '%'])

    if seculo is not None:
        conditions.append("seculo = %s")
        params.append(seculo)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    cursor.execute(query, params)
    resultados = cursor.fetchall()

    # Converte a imagem BLOB para base64 para cada artigo
    for artigo in resultados:
        if artigo.get('imagem'):
            mime_type = detect_image_type(artigo['imagem'])
            if mime_type:
                artigo['imagem_base64'] = f"data:image/{mime_type};base64," + base64.b64encode(artigo['imagem']).decode('utf-8')
            else:
                artigo['imagem_base64'] = None
        else:
            artigo['imagem_base64'] = None

    cursor.close()
    conn.close()
    return resultados

def busca_artigo_por_id(artigo_id):
    """Busca um artigo específico por ID no banco de dados."""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM artigos WHERE id = %s"
    cursor.execute(query, (artigo_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    # Verifica e converte a imagem BLOB para base64 se houver
    if resultado and resultado.get('imagem'):
        mime_type = detect_image_type(resultado['imagem'])
        if mime_type:
            resultado['imagem_base64'] = f"data:image/{mime_type};base64," + base64.b64encode(resultado['imagem']).decode('utf-8')
        else:
            resultado['imagem_base64'] = None
    else:
        resultado['imagem_base64'] = None
    
    return resultado

def docx_para_html(conteudo_binario):
    """Converte o conteúdo do arquivo DOCX para HTML usando Mammoth."""
    try:
        file_stream = io.BytesIO(conteudo_binario)
        result = mammoth.convert_to_html(file_stream)
        html = result.value  # HTML resultante da conversão
        
        return html
    except Exception as e:
        return f"<p>Erro ao processar o arquivo DOCX: {traceback.format_exc()}</p>"

# Definição das rotas do Flask

@app.route('/', methods=['GET', 'POST'])
def index():
    pesquisa = request.form.get('pesquisa')
    artigos = busca_artigos(pesquisa)
    return render_template('index.html', artigos=artigos, titulo="Página Geral")

@app.route('/seculo/<seculo>', methods=['GET'])
def artigos_por_seculo(seculo):
    """Rota para exibir artigos de um determinado século."""
    try:
        # Converte o parâmetro da URL para um número inteiro
        seculo = int(seculo)

        # Busca os artigos filtrados pelo século
        artigos = busca_artigos(seculo=seculo)
        nome_template = f"seculo_{seculo}{'_ac' if seculo < 0 else '_dc'}.html"
        
        # Caminho completo do template
        caminho_template = os.path.join(app.template_folder, nome_template)

        # Verifica se o template existe
        if os.path.exists(caminho_template):
            return render_template(nome_template, artigos=artigos, seculo=seculo)
        else:
            print(f"Template não encontrado: {caminho_template}")
            return render_template('404.html', mensagem=f"Página do século {seculo} não encontrada."), 404
    except ValueError:
        # Trata o caso em que a conversão de string para int falha
        return render_template('404.html', mensagem="Século inválido fornecido."), 404
    except Exception as e:
        print(f"Erro ao processar o século: {e}")
        return f"Erro ao processar o século: {e}", 500

@app.route('/artigo/<int:artigo_id>')
def mostrar_artigo(artigo_id):
    """Rota para exibir o conteúdo de um artigo específico."""
    artigo = busca_artigo_por_id(artigo_id)
    if artigo:
        if artigo['artigo']:
            html_content = docx_para_html(artigo['artigo'])
        else:
            html_content = "<p>Conteúdo do arquivo não encontrado.</p>"

        return render_template('artigo.html', artigo=artigo, html_content=html_content)
    else:
        return "Artigo não encontrado ou arquivo indisponível."

if __name__ == '__main__':
    app.run(debug=True)
