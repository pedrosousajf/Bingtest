from playwright.sync_api import sync_playwright


def baixar_html_prova(email, senha, id_prova):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # ✅ Headless para Streamlit Cloud
        context = browser.new_context()
        page = context.new_page()

        # 🔐 Acessa página de login
        page.goto("https://conta.grancursosonline.com.br/entrar")

        # 🔑 Faz login
        page.locator('input[name="email"]').fill(email)
        page.locator('input[name="password"]').fill(senha)
        page.get_by_role("button", name="Entrar", exact=True).click()

        # 🔄 Aguarda redirecionamento para página de seleção de sistemas
        page.wait_for_url("**/inicio")

        # 🎯 Clica no card "Backoffice Questões - Web"
        page.get_by_role("heading", name="Backoffice Questões - Web").click()

        # 🔄 Aguarda redirecionamento para o sistema do backoffice
        page.wait_for_url("**backoffice-questoes.grancursosonline.com.br/**")

        # 🌐 Acessa a página da prova (gabarito)
        url_prova = f"https://backoffice-questoes.grancursosonline.com.br/insercao/cadastro/prova/provas/gabarito/form/{id_prova}"
        page.goto(url_prova)

        # 🔄 Aguarda o carregamento completo da página da prova
        page.wait_for_load_state("networkidle")

        # 📄 Captura o HTML da prova
        html_content = page.content()

        # 💾 Salva localmente o arquivo HTML
        with open(f"prova_{id_prova}.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        browser.close()

        return html_content
