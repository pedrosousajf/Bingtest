from playwright.sync_api import sync_playwright


def baixar_html_prova(email, senha, id_prova):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # ✅ Streamlit precisa ser headless
        context = browser.new_context()
        page = context.new_page()

        # 🔐 Acessa página de login
        page.goto("https://conta.grancursosonline.com.br/login")

        # 🔑 Faz login
        page.locator('input[name="email"]').fill(email)
        page.locator('input[name="password"]').fill(senha)
        page.get_by_role("button", name="Entrar", exact=True).click()

        # 🔄 Aguarda redirecionamento para página de escolha de sistemas
        page.wait_for_url("**/inicio")

        # 🎯 Clica no card "Backoffice Questões - Web"
        page.get_by_role("heading", name="Backoffice Questões - Web").click()

        # 🔄 Aguarda entrada no sistema do backoffice
        page.wait_for_url("**backoffice-questoes.grancursosonline.com.br/**")

        # 🌐 Vai para a página da prova
        url_prova = f"https://backoffice-questoes.grancursosonline.com.br/insercao/cadastro/prova/provas/gabarito/form/{id_prova}"
        page.goto(url_prova)

        page.wait_for_load_state("networkidle")

        # 📄 Captura o HTML
        html_content = page.content()

        with open(f"prova_{id_prova}.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        browser.close()

        return html_content
