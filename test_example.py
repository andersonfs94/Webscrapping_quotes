## https://playwright.dev/python/docs/intro ##

from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape(): #Inicio da função
    try:        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            try:
                page.goto("https://quotes.toscrape.com/") # Tentando carregar a página
            except Exception as e:
                print(f"Erro ao carregar a página: {e}")
                return

            all_quotes =[]
            all_authors = []
            all_tags = []
            page_number = 1 # Contador de páginas

            print("Iniciando a raspsagem de dados...\n")

            while True:
                print(f"Coletando dados da página {page_number}...")

                quotes = page.locator(".quote .text").all_text_contents()
                authors = page.locator(".quote .author").all_text_contents()

                tags_list = []
                for quote in page.locator(".quote").all():
                    tags = quote.locator(".tags a").all_text_contents()
                    tags_list.append(", ".join(tags))

                # Adiciona os dados da página atual às listas principais
                all_quotes.extend(quotes)
                all_authors.extend(authors)
                all_tags.extend(tags_list)

                print(f"Página {page_number} coletada: {len(quotes)} citações encontradas.")
                
                # Verifica se o botão "Next" existe e clica para ir à próxima página
                next_button = page.locator(".pager .next a")
                if next_button.count() > 0:
                    next_button.click()
                    time.sleep(1) # Pausa de 1 segundo entre o clique e o carregamento da próxima página
                    page.wait_for_load_state("domcontentloaded")  # Aguarda a próxima página carregar
                    page_number += 1 #Atualiza o contador de páginas.
                else:
                    print("\n Nenhuma página restante. Finalizando a coleta...")
                    break  # Sai do loop quando não houver mais "Next"
        
        # Tentando salvar o arquivo
        try:
            sheet = "quotes_all_pages.xlsx"
            df = pd.DataFrame({
                "Quote": all_quotes, 
                "Author": all_authors,
                "Tags": all_tags
            })
            df.to_excel(sheet, index=False)
            print(f"Data saved on {sheet} with {len(all_quotes)} citations.")
            print("Raspagem concluída com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")
            return

   
    except KeyboardInterrupt:
        print("\n Execução interrompida pelo usuário.")    
    except Exception as e:
        print(f"Ocorreu um erro inesperado {e}")

scrape() # Onde a função é chamada


# “Many that live deserve death. And some that die deserve life. 
# Can you give it to them? Then do not be too eager to deal out death in judgement. 
# For even the very wise cannot see all ends.” - Gandalf