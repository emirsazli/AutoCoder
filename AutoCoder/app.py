from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    title = ""
    code = ""

    if request.method == "POST":
        prompt = request.form["prompt"]
        result = get_code_and_title(prompt)
        title, code = result

    return render_template("index.html", title=title, code=code)

def get_code_and_title(prompt):
    system_text = "Kullanıcının verdiği açıklamaya göre önce başlık, sonra Python kodu üret.\nFormat:\nBaşlık: <buraya başlığı yaz>\nKod:\n```python\n<python kodu>\n```"


    cevap = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Veya kullandığın model ismi
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": prompt}
        ]
    )

    yanit = cevap.choices[0].message['content']

    try:
        satirlar = yanit.split("Kod:\n```python\n")
        if len(satirlar) == 2:
            title = satirlar[0].replace("Başlık:", "").strip()
            code = satirlar[1].replace("```", "").strip()
        else:
            title = "Başlık ayıklanamadı"
            code = "Kod bulunamadı"
    except Exception as e:
        title = "Başlık ayıklanamadı"
        code = f"Bir hata oluştu: {str(e)}"

    return title, code

if __name__ == "__main__":
    app.run(debug=True)
