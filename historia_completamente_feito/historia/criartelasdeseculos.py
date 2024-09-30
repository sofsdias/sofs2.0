import os

# Diretório onde os templates serão criados
template_dir = 'templates'

# Cria o diretório 'templates' se ele não existir
if not os.path.exists(template_dir):
    os.makedirs(template_dir)

def gerar_conteudo_html(seculo):
    """Gera o conteúdo HTML para cada século usando o template base."""
    titulo = f"Artigos do século {seculo} {'a.C.' if seculo < 0 else 'd.C.'}"
    return f"""{{% extends 'base.html' %}}

{{% block title %}}{titulo}{{% endblock %}}

{{% block content %}}
<h2>{titulo}</h2>
<div class="articles-grid">
    {{% if artigos %}}
        {{% for artigo in artigos %}}
            <div class="article">
                {{% if artigo['imagem_base64'] %}}
                    <div class="article-image">
                        <img src="{{{{ artigo['imagem_base64'] }}}}" alt="Imagem do artigo">
                    </div>
                {{% endif %}}
                <div class="article-content">
                    <h3>
                        <a href="{{{{ url_for('mostrar_artigo', artigo_id=artigo['id']) }}}}" target="_blank">
                            {{{{ artigo['titulo'] }}}}
                        </a>
                    </h3>
                    <p>Autor: {{{{ artigo['nome_do_autor'] }}}}</p>
                    <p>Publicado em: {{{{ artigo['data_criacao'].strftime('%d/%m/%Y') }}}}</p>
                </div>
            </div>
        {{% endfor %}}
    {{% else %}}
        <p>Nenhum artigo encontrado para este século.</p>
    {{% endif %}}
</div>
{{% endblock %}}
"""

# Cria templates para os séculos de -30 a.C. até 19 d.C.
for seculo in range(-30, 20):
    nome_arquivo = f"seculo_{seculo}{'_ac' if seculo < 0 else '_dc'}.html"
    caminho_arquivo = os.path.join(template_dir, nome_arquivo)
    
    # Gera o conteúdo HTML para o template
    conteudo_html = gerar_conteudo_html(seculo)
    
    # Cria o arquivo HTML com o conteúdo gerado
    with open(caminho_arquivo, 'w', encoding='utf-8') as file:
        file.write(conteudo_html)

    print(f"Arquivo criado: {caminho_arquivo}")
