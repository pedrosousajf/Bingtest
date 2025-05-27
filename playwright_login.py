from playwright.sync_api import sync_playwright


def baixar_html_prova(email, senha, id_prova):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # ✅ Headless obrigatório no Streamlit Cloud
        context = browser.new_context()
        page = context.new_page()

        # 🔐 Login
        page.goto("https://conta.grancursosonline.com.br/login")
        page.locator('input[name="email"]').fill(email)
        page.locator('input[name="password"]').fill(senha)

        # ✅ Clicar no botão correto (não no login via Microsoft/AD)
        page.get_by_role("button", name="Entrar", exact=True).click()

        # 🔄 Aguarda o redirecionamento
        page.wait_for_timeout(5000)  # Pode trocar por waits mais inteligentes depois

        # 🌐 Acessa a página da prova
        url_prova = f"https://backoffice-questoes.grancursosonline.com.br/insercao/cadastro/prova/provas/gabarito/form/{id_prova}"
        page.goto(url_prova)

        page.wait_for_load_state("networkidle")

        # 📄 Captura o HTML
        html_content = page.content()

        with open(f"prova_{id_prova}.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        browser.close()

        return html_content
