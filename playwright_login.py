from playwright.sync_api import sync_playwright


def baixar_html_prova(email, senha, id_prova):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://conta.grancursosonline.com.br/login")

        page.locator('input[name="email"]').fill(email)
        page.locator('input[name="password"]').fill(senha)
        page.get_by_role("button", name="Entrar", exact=True).click()

        # 🔥 Aguarda até cair no backoffice
        page.wait_for_url("**/backoffice-questoes.grancursosonline.com.br/**")

        url_prova = f"https://backoffice-questoes.grancursosonline.com.br/insercao/cadastro/prova/provas/gabarito/form/{id_prova}"
        page.goto(url_prova)

        page.wait_for_load_state("networkidle")

        html_content = page.content()

        with open(f"prova_{id_prova}.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        browser.close()

        return html_content
