## ==============================
# 🔧 Instalação de pacotes
# ==============================
!apt update -y
!apt install -y tesseract-ocr poppler-utils
!pip install --upgrade pytesseract Pillow pdf2image PyMuPDF easyocr gspread oauth2client \
    google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 \
    gspread-formatting opencv-python-headless numpy

# ==============================
# 📂 Montar Google Drive
# ==============================
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

# ==============================
# 📦 Importações
# ==============================
import os
import re
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import pytesseract
import easyocr
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pdf2image import convert_from_path
from gspread_formatting import set_row_height, set_column_width, format_cell_range, CellFormat, TextFormat, set_frozen

# ==============================
# 🔐 Autenticação Google
# ==============================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

json_path = '/content/drive/MyDrive/Colab Notebooks/caetanodecampos-0e106bb10513.json'
if not os.path.exists(json_path):
    raise FileNotFoundError(f"Arquivo JSON não encontrado: {json_path}")

creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)

spreadsheet_id = '1nysE4mZ8xzFzEE5IibUaU65qaG3z6ftlSYJtWuijVOg'
spreadsheet = client.open_by_key(spreadsheet_id)
sheet = spreadsheet.worksheet('sheet1')

# ==============================
# 🖼️ Pasta de arquivos
# ==============================
image_folder = '/content/drive/MyDrive/Colab Notebooks/contracapas'

# ==============================
# 🧠 Função OCR + Extração de Dados
# ==============================
reader = easyocr.Reader(['pt'], gpu=True)

def extrair_dados(texto):
    """Extrai título, autor, ano e editora do texto OCR"""
    titulo = autor = ano = editora = "Não encontrado"
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]

    # -------------------
    # TÍTULO → primeira linha longa "limpa"
    # -------------------
    for linha in linhas:
        if len(linha.split()) > 3 and not linha.isupper():
            titulo = linha
            break

    # -------------------
    # AUTOR → procura padrão "Sobrenome, Nome"
    # -------------------
    padrao_autor = r"([A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+,\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+.*)"
    match_autor = re.search(padrao_autor, texto)
    if match_autor:
        autor = match_autor.group(1).strip()

    # -------------------
    # ANO → primeira ocorrência de 4 dígitos plausível
    # -------------------
    padrao_ano = r"(19\d{2}|20\d{2}|202\d|203\d)"
    match_ano = re.search(padrao_ano, texto)
    if match_ano:
        ano = match_ano.group(1)

    # -------------------
    # EDITORA → palavras-chave
    # -------------------
    padrao_editora = r"(?i)(Editora\s+[^\n,]+|Publicado por\s+[^\n,]+|FTD|Ática|Moderna|Companhia das Letras|Saraiva)"
    match_editora = re.search(padrao_editora, texto)
    if match_editora:
        editora = match_editora.group(1).strip()

    return titulo, autor, ano, editora

# ==============================
# 🔁 Processar arquivos (com tratamento de erros)
# ==============================
def arquivos_ordenados(pasta):
    """Ordena arquivos numericamente"""
    return sorted(os.listdir(pasta), key=lambda x: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', x)])

arquivos = arquivos_ordenados(image_folder)

# Verificar duplicatas na planilha
dados_existentes = [row[4] for row in sheet.get_all_values()[1:]]

for file_name in arquivos:
    try:
        if file_name in dados_existentes:
            print(f"⚠️ Pulando {file_name} (já existe na planilha)")
            continue

        file_path = os.path.join(image_folder, file_name)
        texto_extraido = ""

        # PDF
        if file_name.lower().endswith('.pdf'):
            try:
                pages = convert_from_path(file_path)
                for page in pages:
                    texto_extraido += ' ' + ' '.join([line[1] for line in reader.readtext(np.array(page))])
            except Exception as e:
                print(f"❌ Erro ao processar PDF {file_name}: {e}")
                texto_extraido = ""

        # Imagem
        elif file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(file_path)
                texto_extraido = ' '.join([line[1] for line in reader.readtext(np.array(img))])
            except Exception as e:
                print(f"❌ Erro ao processar imagem {file_name}: {e}")
                texto_extraido = ""

        else:
            print(f"⚠️ Formato não suportado: {file_name}")
            continue

        # Se não conseguiu extrair nada
        if not texto_extraido.strip():
            titulo, autor, ano, editora = ["Não encontrado"] * 4
        else:
            titulo, autor, ano, editora = extrair_dados(texto_extraido)

        print(f"📚 {file_name} -> {titulo} | {autor} | {ano} | {editora}")

        try:
            sheet.append_row([titulo, autor, ano, editora, file_name])
        except Exception as e:
            print(f"❌ Erro ao salvar {file_name} na planilha: {e}")

    except Exception as e:
        print(f"❌ Erro inesperado no arquivo {file_name}: {e}")

# ==============================
# 🎨 Formatação da planilha
# ==============================
# Congelar primeira linha
set_frozen(sheet, rows=1)

# Largura das colunas
set_column_width(sheet, 'A', 300)
set_column_width(sheet, 'B', 200)
set_column_width(sheet, 'C', 100)
set_column_width(sheet, 'D', 200)
set_column_width(sheet, 'E', 150)

# Altura da primeira linha
set_row_height(sheet, '1:1', 30)

# Cabeçalho negrito e centralizado
header_format = CellFormat(
    textFormat=TextFormat(bold=True),
    horizontalAlignment='CENTER'
)
format_cell_range(sheet, 'A1:E1', header_format)
