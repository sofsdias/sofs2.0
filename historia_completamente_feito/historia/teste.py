import mysql.connector

def armazenar_arquivo(docx_path, image_path, titulo, autor, seculo):
    # Lê o conteúdo do arquivo DOCX como binário
    with open(docx_path, 'rb') as file:
        conteudo_binario = file.read()

    # Lê o conteúdo da imagem como binário
    with open(image_path, 'rb') as image_file:
        imagem_binaria = image_file.read()

    # Conecte-se ao banco de dados
    conn = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='historia'
    )
    cursor = conn.cursor()

    # Insere o conteúdo do arquivo DOCX e da imagem como BLOB
    query = """
    INSERT INTO artigos (titulo, nome_do_autor, seculo, artigo, imagem)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (titulo, autor, seculo, conteudo_binario, imagem_binaria))

    conn.commit()
    cursor.close()
    conn.close()

# Exemplo de uso com caminhos corretos
armazenar_arquivo(
    r"C:\Users\MMSOUZA\OneDrive - Auto Viação MM Souza Turismo Ltda\testando.docx", 
    r"C:\Users\MMSOUZA\OneDrive - Auto Viação MM Souza Turismo Ltda\Imagens\Capturas de tela\Captura de tela 2024-09-04 193111.png",
    'Titulo do Artigo', 
    'Nome do Autor', 
    '-20'
)
