from playwright.sync_api import sync_playwright
import os
import json


SESSAO_DIR = "sessions"
os.makedirs(SESSAO_DIR, exist_ok=True)


def salvar_cookies(context, nome_arquivo):
    cookies = context.storage_state()
    with open(os.path.join(SESSAO_DIR, nome_arquivo), "w") as f:
        json.dump(cookies, f)


def carregar_cookies(browser, nome_arquivo):
    caminho = os.path.join(SESSAO_DIR, nome_arquivo)
    if os.path.exists(caminho):
        return browser.new_context(storage_state=caminho)
    else:
        return browser.new_context()


def baixar_html_prova(email, senha, id_prova, nome_sessao="sessao_gran.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = carregar_cookies(browser, nome_sessao)
        page = context.new_page()

        # Testa se já tá logado
        page.goto("https://backoffice-questoes.grancursosonline.com.br/")
        if "Entrar" in page.content():
            # Se não tá logado, faz login
            page.goto("https://conta.grancursosonline.com.br/login")

            page.fill('input[name="email"]', email)
            page.fill('input[name="password"]', senha)
            page.click('button:has-text("Entrar")')

            page.wait_for_timeout(5000)

            salvar_cookies(context, nome_sessao)

        # Acessa a prova
        url_prova = f"https://backoffice-questoes.grancursosonline.com.br/insercao/cadastro/prova/provas/gabarito/form/{id_prova}"
        page.goto(url_prova)

        page.wait_for_load_state("networkidle")

        html_content = page.content()

        browser.close()
        return html_content
