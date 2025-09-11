import re
import os

def separar_questoes_em_arquivos(arquivo_entrada):
    # Lê o conteúdo do arquivo com todas as questões
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Expressão regular atualizada para capturar números com zero à esquerda
    padrao = r'(Questão\s+(\d{1,3}):.*?)(?=Questão\s+\d{1,3}:|$)'  # captura texto e número
    questoes = re.findall(padrao, conteudo, re.DOTALL)

    # Cria diretório para armazenar os arquivos, se não existir
    os.makedirs('Questoes', exist_ok=True)

    # Processa e salva cada questão
    for questao_texto, numero in questoes:
        numero_formatado = numero.zfill(2)  # garante dois dígitos, ex: '01', '09', '10'
        print(numero_formatado)
        nome_arquivo = f'Questoes/Questao{numero_formatado}/Questao{numero_formatado}.txt'
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(questao_texto.strip())

# Chamada da função
separar_questoes_em_arquivos('QuestoesFUVEST.txt')

