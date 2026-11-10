import os
from aiohttp import web
from pyrogram import Client

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Servidor Proxy do Telegram Rodando com Sucesso!")

async def main():
    # Inicia o servidor web do Render
    web_app = web.Application()
    web_app.add_routes(routes)
    runner = web.AppRunner(web_app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web rodando na porta {port}")

    # Inicia o cliente do Telegram se as chaves existirem
    if API_ID and API_HASH and BOT_TOKEN:
        await app.start()
        print("Bot do Telegram conectado com sucesso!")
    
    # Mantém o servidor rodando direto
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())