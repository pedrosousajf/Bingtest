from playwright.sync_api import sync_playwright
import time


def baixar_html_prova(email, senha, id_prova):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Coloca True se quiser rodar sem abrir o navegador
        context = browser.new_context()
        page = context.new_page()

        # Acessa a página de login
        page.goto("https://conta.grancursosonline.com.br/login")

        # Preenche e-mail
        page.locator('input[name="email"]').fill(email)

        # Preenche senha
        page.locator('input[name="password"]').fill(senha)

        # Clica no botão Entrar
        page.locator('button:has-text("Entrar")').click()

        # Aguarda o login completar
        page.wait_for_timeout(5000)  # Você pode ajustar ou melhorar isso com um wait mais inteligente

        # Vai pra página da prova no backoffice
        url_prova = f"https://backoffice-questoes.grancursosonline.com.br/insercao/cadastro/prova/provas/gabarito/form/{id_prova}"
        page.goto(url_prova)

        # Espera a página carregar completamente
        page.wait_for_load_state("networkidle")
        time.sleep(2)  # Margem extra de segurança

        # Captura o HTML
        html_content = page.content()

        # Salva localmente
        with open(f"prova_{id_prova}.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ HTML da prova {id_prova} baixado com sucesso!")

        browser.close()

        return html_content
