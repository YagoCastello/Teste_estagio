import os
import zipfile
import pandas as pd
import pdfplumber
import re

def extrair_dados_pdf(nome_arquivo_pdf):
    """
    Extrai os dados da tabela do PDF do Anexo I
    """
    dados = []
    cabecalho = None
    legenda_od_amb = {}
    
    with pdfplumber.open(nome_arquivo_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            
            # Extrair legenda do rodapé (se existir)
            if "OD =" in texto and "AMB =" in texto:
                legenda_match = re.search(r"OD\s*=\s*(.*?)\s*AMB\s*=\s*(.*?)(?:\n|$)", texto)
                if legenda_match:
                    legenda_od_amb['OD'] = legenda_match.group(1).strip()
                    legenda_od_amb['AMB'] = legenda_match.group(2).strip()
            
            # Extrair tabela
            tabela = pagina.extract_table()
            if tabela:
                if not cabecalho:
                    cabecalho = tabela[0]
                    dados.extend(tabela[1:])
                else:
                    dados.extend(tabela)
    
    return cabecalho, dados, legenda_od_amb

def processar_dados(cabecalho, dados, legenda):
    """
    Processa os dados extraídos e substitui as abreviações
    """
    # Criar DataFrame
    df = pd.DataFrame(dados, columns=cabecalho)
    
    # Limpar dados
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Substituir abreviações
    if 'OD' in df.columns and 'OD' in legenda:
        df['OD'] = df['OD'].replace({'OD': legenda['OD'], '': ''})
    
    if 'AMB' in df.columns and 'AMB' in legenda:
        df['AMB'] = df['AMB'].replace({'AMB': legenda['AMB'], '': ''})
    
    return df

def executar_teste_transformacao(nome_arquivo_pdf, seu_nome):
    try:
        print("Iniciando extração de dados do PDF...")
        cabecalho, dados, legenda = extrair_dados_pdf(nome_arquivo_pdf)
        
        if not cabecalho or not dados:
            raise ValueError("Não foi possível extrair dados da tabela do PDF")
        
        print("Processando dados extraídos...")
        df = processar_dados(cabecalho, dados, legenda)
        
        # Nome do arquivo CSV
        nome_csv = f"Rol_Procedimentos_{seu_nome}.csv"
        df.to_csv(nome_csv, index=False, encoding='utf-8-sig')
        print(f"Dados salvos em {nome_csv}")
        
        # Compactar
        nome_zip = f"Teste_{seu_nome}.zip"
        with zipfile.ZipFile(nome_zip, 'w') as zipf:
            zipf.write(nome_csv)
            print(f"Arquivo compactado criado: {nome_zip}")
        
        # Remover CSV temporário
        os.remove(nome_csv)
        
        print("Processo concluído com sucesso!")
        return nome_zip
    
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        return None

if __name__ == "__main__":
    
    ARQUIVO_PDF = "Anexo_I.pdf"  # Ou o caminho completo para o arquivo
    SEU_NOME = "Yago_Saloman"  
    
    executar_teste_transformacao(ARQUIVO_PDF, SEU_NOME)