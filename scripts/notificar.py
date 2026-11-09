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

def h32(n):
    M = 0xffffffff
    x = ((n ^ 0x9e3779b9) & M) * 2654435761 & M
    x ^= x >> 15; x = x * 2246822519 & M; x ^= x >> 13; x = x * 3266489917 & M; x ^= x >> 16
    return x

def kick_sabado(k):
    d = inicio + datetime.timedelta(days=k - 1)
    return 6 <= k <= 179 and k % 30 != 0 and d.weekday() == 5 and h32(k * 3 + 1) % 3 == 0
if n < 1:
    titulo, msg = "Físico dos Deuses", "A campanha ainda não começou."
elif n > 180:
    titulo, msg = "Campanha concluída", "Os 180 dias acabaram. Abra o app para ver sua retrospectiva e começar a próxima temporada."
elif noite:
    titulo, msg = "Sistema", f"Dia {n} de 180. Já registrou o dia? Conte ao Sistema o que treinou e comeu antes de dormir."
    if kick_sabado(n + 1):
        msg = f"Dia {n} de 180. Sinal detectado para amanhã cedo. Conclua a quest de hoje no app para revelar o boss de sábado."
else:
    chefe = " Hoje é dia de CHEFÃO." if n % 30 == 0 else ""
    titulo, msg = "Bom dia, Vitor", f"Dia {n} de 180: {quest}.{chefe} Abra o app e faça o check-in."
req = urllib.request.Request("https://ntfy.sh/" + os.environ["NTFY_TOPIC"], data=msg.encode("utf-8"), method="POST",
                             headers={"Title": "=?UTF-8?B?" + __import__("base64").b64encode(titulo.encode()).decode() + "?=",
                                      "Click": os.environ["APP_URL"], "Tags": "crossed_swords"})
urllib.request.urlopen(req, timeout=20)
print("enviado:", titulo, "|", msg)
