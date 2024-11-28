import discord
from discord import app_commands
import os
import requests

TOKEN = os.getenv("DISCORD_TOKEN")  # Hole das Token aus den Umgebungsvariablen

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"Angemeldet als {client.user}")
    await tree.sync()

@tree.command(name="prompt", description="Frag den Sauxomat was!")
@app_commands.describe(prompt="Ich bin ganz Ohr! Frag mich was")
async def prompt(interaction: discord.Interaction, prompt: str):
    try:
        # URL und Anfrage
        url = "https://gemini.einfachniemmand-project.workers.dev"
        headers = {"Content-Type": "application/json"}
        payload = {"content": prompt}

        # POST-Anfrage senden
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Fehler bei schlechter Antwort auslösen

        # Antwort verarbeiten
        data = response.json()
        result = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Ergebnis senden
        await interaction.response.send_message(f"Antwort: {result}")
    except Exception as e:
        await interaction.response.send_message(f"Fehler: {e}")

# Starte den Bot
def handler(request):
    client.run(TOKEN)
    return "Bot is running", 200
