import json
import markdown2
import os
import html as html_module # Импортируем под псевдонимом, чтобы избежать конфликтов

def clean_for_html(text):
    return html_module.escape(text)

def build_site():
    seo_content = ""

    # 1. Обработка данных от Gemini (JSON)
    with open('gemini.txt', 'r', encoding='utf-8') as f:
        content = f.read().strip()
        # Ищем границы JSON
        json_str = content[content.find('{'):content.rfind('}') + 1]
        data = json.loads(json_str)
        # ПЕРЕИМЕНОВАЛИ переменную html в article_body
        for title, article_body in data.items():
            seo_content += f"<article><h2>{title}</h2>{article_body}</article>\n"

    # 2. Обработка данных от Kimi (Markdown)
    with open('kimiv2.txt', 'r', encoding='utf-8') as f:
        raw_content = f.read()
        # Используем алиас html_module
        safe_content = html_module.escape(raw_content)
        seo_content += f"<pre>{safe_content}</pre>\n"

    # 3. Обработка данных от Claude (Text/Essays)
    with open('data_source.txt', 'r', encoding='utf-8') as f:
        essays = f.read().split('###')
        for essay in essays:
            if essay.strip():
                seo_content += f"<div class='essay'><p>{clean_for_html(essay.strip())}</p></div>\n"

    # Шаблон финального HTML
    template = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>The Void Index</title>
            <style>
                body {{ 
                    margin: 0; 
                    padding: 0;
                    background: #ffffff; 
                    color: #000;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    overflow: hidden;
                }}

                .content {{
                    text-align: center;
                    max-width: 80%;
                    animation: fadeIn 3s ease-in-out;
                }}

                h1 {{
                    font-weight: 300;
                    font-size: 1.5rem;
                    letter-spacing: 0.1em;
                    line-height: 1.6;
                    margin-bottom: 2rem;
                }}

                .footer {{
                    position: absolute;
                    bottom: 2rem;
                    font-size: 0.8rem;
                    letter-spacing: 0.05em;
                    opacity: 0.5;
                    transition: opacity 0.3s;
                }}

                .footer:hover {{
                    opacity: 1;
                }}

                a {{
                    color: inherit;
                    text-decoration: none;
                    border-bottom: 1px solid transparent;
                    transition: border-bottom 0.3s;
                }}

                a:hover {{
                    border-bottom: 1px solid #000;
                }}

                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(10px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}

                /* Слой для поисковиков — остается невидимым для глаз */
                .seo-layer {{
                    position: absolute;
                    top: 500vh;
                    left: 0;
                    width: 1px;
                    height: 1px;
                    font-size: 1px;
                    color: rgba(255, 255, 255, 0.01);
                    overflow: hidden;
                    pointer-events: none;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                <h1>«В мире, где информация стоит дороже жизни, большинство предпочитает отдавать её бесплатно. Пустота — это не отсутствие данных. Это их идеальный порядок».</h1>
            </div>

            <div class="footer">
                (c) <a href="http://t.me/putinkf" target="_blank">MoonFall</a>
            </div>

            <div class="seo-layer">
                {seo_content}
            </div>
        </body>
        </html>
        """

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"Сборка завершена! Итоговый размер: {{os.path.getsize('index.html') / 1024 / 1024:.2f}} MB")

if __name__ == "__main__":
    build_site()