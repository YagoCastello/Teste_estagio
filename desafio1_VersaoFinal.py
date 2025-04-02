import os
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup
import re

def download_pdfs_and_zip():
    # Configurações
    base_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("Acessando o site...")
        response = requests.get(base_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print("Analisando o conteúdo...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # URLs diretos dos anexos (obtidos manualmente)
        pdf_links = [
            ('Anexo_I.pdf', 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf'),
            ('Anexo_II.pdf', 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf')
        ]
        
        # Alternativa: Buscar os links automaticamente (caso os URLs mudem)
        if not pdf_links:
            for link in soup.find_all('a', href=True):
                href = link['href']
                if 'Anexo_I' in href or 'Anexo_II' in href:
                    # Remover o prefixo do visualizador de PDF se existir
                    clean_url = re.sub(r'^chrome-extension://[^/]+/', '', href)
                    if 'Anexo_I' in clean_url:
                        pdf_links.append(('Anexo_I.pdf', clean_url))
                    elif 'Anexo_II' in clean_url:
                        pdf_links.append(('Anexo_II.pdf', clean_url))
        
        if not pdf_links:
            print("Não foram encontrados links para os anexos.")
            return
        
        print(f"Encontrados {len(pdf_links)} anexos:")
        for filename, url in pdf_links:
            print(f"- {filename}: {url}")
        
        # Criar diretório temporário
        temp_dir = 'temp_anexos'
        os.makedirs(temp_dir, exist_ok=True)
        downloaded_files = []
        
        # Baixar os PDFs
        for filename, pdf_url in pdf_links:
            try:
                print(f"\nBaixando {filename}...")
                pdf_response = requests.get(pdf_url, headers=headers, stream=True, timeout=60)
                pdf_response.raise_for_status()
                
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'wb') as f:
                    for chunk in pdf_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                if os.path.exists(filepath):
                    downloaded_files.append(filepath)
                    print(f"Download concluído: {filename} ({os.path.getsize(filepath)/1024:.2f} KB)")
                else:
                    print(f"Erro: Arquivo {filename} não foi salvo corretamente.")
                
            except Exception as e:
                print(f"Erro ao baixar {filename}: {str(e)}")
                continue
        
        # Compactar os arquivos baixados
        if downloaded_files:
            zip_filename = 'Anexos_ROI_Procedimentos.zip'
            try:
                with ZipFile(zip_filename, 'w') as zipf:
                    for file in downloaded_files:
                        zipf.write(file, os.path.basename(file))
                
                print(f"\nCompactação concluída! Arquivo criado: {zip_filename}")
                print(f"Tamanho do arquivo ZIP: {os.path.getsize(zip_filename)/1024:.2f} KB")
                
            except Exception as e:
                print(f"Erro ao criar arquivo ZIP: {str(e)}")
        
        # Limpar arquivos temporários
        for file in downloaded_files:
            try:
                os.remove(file)
            except:
                pass
        
        try:
            os.rmdir(temp_dir)
        except:
            pass
        
    except Exception as e:
        print(f"\nOcorreu um erro durante a execução: {str(e)}")

if __name__ == "__main__":
    download_pdfs_and_zip()
    print("\nProcesso concluído.")