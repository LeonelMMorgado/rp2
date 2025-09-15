import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

# grok
# https://platform.openai.com/docs/guides/images-vision?api-mode=responses&format=base64-encoded#analyze-images
# gemini
# https://ai.google.dev/gemini-api/docs/image-understanding?hl=pt-br

# --- Carrega a chave do .env ---
load_dotenv()
gpt_key = os.getenv("OPENAI_API_KEY")
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
xai_api_key = os.getenv("XAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

gpt_client = OpenAI(api_key=gpt_key)
deepseek_client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
xai_client = OpenAI(api_key=xai_api_key, base_url="https://api.x.ai/v1")
gemini_client= OpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

clients = {
    "GPT": gpt_client,
    "DEEPSEEK": deepseek_client,
    "XAI": xai_client,
    "GEMINI": gemini_client,
}

def encode_image(image_path):
    """Converte imagem para base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

dir_base = '.'

for ai in clients:
    model = ""
    if ai == "GPT": model = 'gpt-4.1-mini'
    elif ai == "DEEPSEEK": model = 'deepseek-reasoner'
    elif ai == "XAI": model = 'grok-4'
    elif ai == "GEMINI": model = 'gemini-2.5-flash'
    
    for fuvest_ano in os.listdir(dir_base):
        ano_path = os.path.join(dir_base, fuvest_ano)
        questoes_ano_path = os.path.join(ano_path, 'Questoes')

        for i, questao in enumerate(os.listdir(questoes_ano_path)):
            num = f"{i:02d}"
            questao_path = os.path.join(questoes_ano_path, questao)
            out_path = os.path.join(questao_path, f'Resposta{ai}Questao{num}.txt')
            cont_path = os.path.join(questao_path, f'Questao{num}.txt')
            quest_cont = ''
            with open(cont_path, 'r') as file_handle:
                quest_cont = file_handle.read()
        
            content_blocks = []
            img_index = 1

            for chunk in quest_cont.split("{imagem}"):
                if chunk.strip():
                    content_blocks.append({"type": "input_text", "text": chunk})

                img_path = os.path.join(questao_path, f"Questao{num}-{img_index}.png")
                if not os.path.exists(img_path) and img_index == 1:
                    img_path = os.path.join(questao_path, f"Questao{num}.png")

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

            #o chatgpt só aceita client.responses.create()
            #os outros aceitam client.chat.completions.create()

            try:
                response = clients[ai].responses.create(
                    model=model,
                    input=[{"role": "user", "content": content_blocks}]
                )

                reply = response.output_text or ""
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(reply)

                print(f"✅ Resposta salva em {out_path}")

            except Exception as e:
                print(f"⚠️ Erro ao processar Questao{num}: {e}")