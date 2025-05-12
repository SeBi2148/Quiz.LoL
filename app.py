from flask import Flask, render_template, request, session, redirect, url_for
import random
import requests

app = Flask(__name__)
app.secret_key = "ceva_secret"


static_questions = [
    {
        "question": "Ce rol are campionul Thresh?",
        "options": ["ADC", "Junglă", "Suport", "Top"],
        "answer": "Suport"
    },
    {
        "question": "Cum se numește abilitatea pasivă a lui Yasuo?",
        "options": ["Conqueror", "Steel Tempest", "Way of the Wanderer", "Last Breath"],
        "answer": "Way of the Wanderer"
    },
    {
        "question": "Ce campion este cunoscut ca The Darkin Blade?",
        "options": ["Aatrox", "Lux", "Teemo", "Ahri"],
        "answer": "Aatrox"
    },
    {
        "question": "Ce campion este cunoscut ca The Unforgiven?",
        "options": ["Yone", "Zed", "Yasuo", "Tryndamere"],
        "answer": "Yasuo"
    },
    {
        "question": "Care este ultimata lui Lux?",
        "options": ["Prismatic Barrier", "Lucent Singularity", "Final Spark", "Light Binding"],
        "answer": "Final Spark"
    },
    {
        "question": "Ce campion se transformă într-un dragon?",
        "options": ["Aurelion Sol", "Shyvana", "Sion", "Kennen"],
        "answer": "Shyvana"
    },
    {
        "question": "Ce tip de energie folosește Zed?",
        "options": ["Mana", "Furie", "Umbră", "Energi"],
        "answer": "Energi"
    },
    {
        "question": "Ce campion are abilitatea ‘Bouncing Bomb’?",
        "options": ["Ziggs", "Zilean", "Zoe", "Zed"],
        "answer": "Ziggs"
    },
    {
        "question": "Ce rol principal are campionul Janna?",
        "options": ["Suport", "Junglă", "Top", "Mid"],
        "answer": "Suport"
    },
    {
        "question": "Care este pasiva lui Teemo?",
        "options": ["Camuflaj", "Blinding Dart", "Toxic Shot", "Noxious Trap"],
        "answer": "Camuflaj"
    },
    {
        "question": "Cum se numește orașul de origine al lui Jinx?",
        "options": ["Noxus", "Demacia", "Zaun", "Ionia"],
        "answer": "Zaun"
    },
    {
        "question": "Ce campion are abilitatea ‘Decimate’?",
        "options": ["Garen", "Darius", "Draven", "Renekton"],
        "answer": "Darius"
    },
    {
        "question": "Care campion are un urs numit Tibbers?",
        "options": ["Annie", "Amumu", "Lulu", "Nunu"],
        "answer": "Annie"
    },
    {
        "question": "Cine este cunoscut ca The Curious Chameleon?",
        "options": ["Neeko", "Teemo", "Yuumi", "Rakan"],
        "answer": "Neeko"
    },
    {
        "question": "Ce abilitate este folosită pentru a face ‘Flash’?",
        "options": ["Summoner Spell", "Passive", "Ultimate", "Item"],
        "answer": "Summoner Spell"
    }
]

def get_champions():
    RIOT_API_URL = "https://ddragon.leagueoflegends.com/cdn/14.5.1/data/en_US/champion.json"
    try:
        response = requests.get(RIOT_API_URL)
        if response.status_code == 200:
            data = response.json()["data"]
            champions = [{
                "name": champ,
                "image": f"https://ddragon.leagueoflegends.com/cdn/14.5.1/img/champion/{data[champ]['image']['full']}",
            } for champ in data.keys()]
            return champions
    except:
        return []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["username"] = request.form.get("username")
        session["score"] = 0
        session["wrong"] = 0
        session["questions_answered"] = 0
        return redirect(url_for("quiz"))
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if session.get("questions_answered", 0) >= 10:
        return redirect(url_for("final"))

    all_champions = get_champions()
    champion_options = random.sample(all_champions, 4)
    champ = random.choice(champion_options)
    question = random.choice(static_questions)

    result_1 = ""
    result_2 = ""

    if request.method == "POST":
        user_answer_1 = request.form.get("answer_1")
        user_answer_2 = request.form.get("answer_2")

        correct_answer_1 = request.form.get("correct_answer_1")
        correct_answer_2 = request.form.get("correct_answer_2")

        if user_answer_1 == correct_answer_1:
            session["score"] += 1
            result_1 = "Corect la întrebarea 1!"
        else:
            session["wrong"] += 1
            result_1 = f"Greșit la întrebarea 1! Răspunsul corect era {correct_answer_1}"

        if user_answer_2 == correct_answer_2:
            session["score"] += 1
            result_2 = "Corect la întrebarea 2!"
        else:
            session["wrong"] += 1
            result_2 = f"Greșit la întrebarea 2! Răspunsul corect era {correct_answer_2}"

        session["questions_answered"] += 1

    return render_template("quiz.html", question=question, champions=champion_options, champ=champ,
                           result_1=result_1, result_2=result_2)

@app.route("/final")
def final():
    return render_template("final.html", score=session.get("score", 0), wrong=session.get("wrong_answers", 0))

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
