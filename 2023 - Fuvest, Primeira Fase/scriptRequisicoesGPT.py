import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

# --- Carrega a chave do .env ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

BASE_DIR = "./Questoes"
OUT_DIR = "./RespostasGPT"
os.makedirs(OUT_DIR, exist_ok=True)

def encode_image(image_path):
    """Converte imagem para base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

for x in range(1, 91):
    num = f"{x:02d}"
    folder = os.path.join(BASE_DIR, f"Questao{num}")
    txt_path = os.path.join(folder, f"Questao{num}.txt")
    out_path = os.path.join(OUT_DIR, f"RespostaGPTQuestao{num}.txt")

    if not os.path.exists(txt_path):
        print(f"❌ Arquivo não encontrado: {txt_path}")
        continue

    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- Prepara blocos de conteúdo ---
    content_blocks = []
    img_index = 1

    for chunk in content.split("{imagem}"):
        # bloco de texto
        if chunk.strip():
            content_blocks.append({"type": "input_text", "text": chunk})

        # bloco de imagem
        img_path = os.path.join(folder, f"Questao{num}-{img_index}.png")
        if not os.path.exists(img_path) and img_index == 1:
            img_path = os.path.join(folder, f"Questao{num}.png")

        if os.path.exists(img_path):
            img_b64 = encode_image(img_path)
            content_blocks.append({
                "type": "input_file",
                "image_url": f"data:image/png;base64,{img_b64}"
            })

        img_index += 1

    if not content_blocks:
        print(f"⚠️ Questao{num} está vazia, pulando...")
        continue

    try:
        # --- Chamada correta da API ---
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{"role": "user", "content": content_blocks}]
        )

        reply = response.output_text or ""
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(reply)

        print(f"✅ Resposta salva em {out_path}")

    except Exception as e:
        print(f"⚠️ Erro ao processar Questao{num}: {e}")
