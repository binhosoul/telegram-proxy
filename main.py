import os
from aiohttp import web
from pyrogram import Client

# Configurações que vamos pegar no Telegram
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Servidor Proxy do Telegram Rodando com Sucesso!")

async def start_web():
    web_app = web.Application()
    web_app.add_routes(routes)
    runner = web.AppRunner(web_app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web rodando na porta {port}")

if __name__ == "__main__":
    app.start()
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_web())
    import idle
    idle()