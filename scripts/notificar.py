import os, datetime, urllib.request, zoneinfo
tz = zoneinfo.ZoneInfo("America/Sao_Paulo")
hoje = datetime.datetime.now(tz).date()
inicio = datetime.date(2026, 11, 9)
n = (hoje - inicio).days + 1
noite = os.environ.get("EVENT_SCHEDULE", "") == "30 23 * * *"
dow = hoje.weekday()  # 0 = segunda
quests = {0: "dia de luta", 1: "Superior A na academia", 2: "dia de luta", 3: "Inferior + core na academia",
          4: "Superior B na academia", 5: "desafio em casa (e refeição livre)", 6: "treino em casa"}
especiais = {datetime.date(2026, 11, 10): "aula experimental de jiu-jitsu",
             datetime.date(2026, 11, 11): "Superior A na academia"}
quest = especiais.get(hoje, quests[dow])
if n < 1:
    titulo, msg = "Físico dos Deuses", "A campanha ainda não começou."
elif n > 180:
    titulo, msg = "Campanha concluída", "Os 180 dias acabaram. Abra o app para ver sua retrospectiva e começar a próxima temporada."
elif noite:
    titulo, msg = "Sistema", f"Dia {n} de 180. Já registrou o dia? Conte ao Sistema o que treinou e comeu antes de dormir."
else:
    chefe = " Hoje é dia de CHEFÃO." if n % 30 == 0 else ""
    titulo, msg = "Bom dia, Vitor", f"Dia {n} de 180: {quest}.{chefe} Abra o app e faça o check-in."
req = urllib.request.Request("https://ntfy.sh/" + os.environ["NTFY_TOPIC"], data=msg.encode("utf-8"), method="POST",
                             headers={"Title": "=?UTF-8?B?" + __import__("base64").b64encode(titulo.encode()).decode() + "?=",
                                      "Click": os.environ["APP_URL"], "Tags": "crossed_swords"})
urllib.request.urlopen(req, timeout=20)
print("enviado:", titulo, "|", msg)
