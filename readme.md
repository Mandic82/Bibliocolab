⚙️ Instalação e Execução
Abra o notebook notebook.ipynbno Google Colab .
Monte o Google Drive para acessar uma pasta de imagens/PDFs.
Verifique se o caminho do arquivo JSON está correto no código.
Execute todas as células do notebook.
O código será instalado automaticamente todas as dependências necessárias, incluindo OCR e bibliotecas de processamento de imagens.

🧠 Funcionalidades
OCR robusto em português com EasyOCR.
Suporte a imagens ( .jpg, .png, .jpeg) e PDFs .
Pré-processamento das imagens para aumentar a precisão do OCR (cinza, contraste, equalização).
Pareamento automático de capas e contracapas.
Pós-processamento de texto , incluindo correção de palavras quebradas e remoção de caracteres inválidos.
Evita duplicidade na planilha, gravando apenas novos arquivos.
Registro dos seguintes campos na planilha:
Título
Autor
Ano
Editora
Nome do arquivo
📝 Observações
A pasta de imagens/PDFs deve ser organizada e numerada, seguindo o padrão 1.1.capa, 1.1.contrapara manter o pareamento correto.
O OCR funciona melhor em imagens nítidas e legíveis . PDFs digitalizados de baixa qualidade podem precisar de ajuste manual.
É usar GPU recomendada no Colab para acelerar o processamento, especialmente se houver muitas imagens ou PDFs grandes. -
💡 Sugestões de melhoria futura
OCR paralelo em múltiplas GPUs ou threads.
Reconstrução automática de limites espalhados em várias linhas.
Integração com banco de dados externos para consultas e buscas avançadas.
🛠 Tecnologias utilizadas
Python 3.x
Google Colab
EasyOCR
Travesseiro
pdf2image
OpenCV
gspread
OAuth2Client
Oliveira AR: 09/2025
