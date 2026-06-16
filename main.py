import os
from bot import create_bot
from config import TOKEN
if __name__ == "__main__":
    

    if not TOKEN:
        print("❌ DISCORD_TOKEN bulunamadı!")
        print("PowerShell:")
        print('$env:DISCORD_TOKEN="TOKENIN"')
        exit()

    bot = create_bot()
    print(" Bot başlatılıyor...")
    bot.run(TOKEN)