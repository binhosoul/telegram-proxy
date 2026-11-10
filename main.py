import os
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Servidor Proxy do Telegram Rodando com Sucesso!")

async def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web_app = asyncio.run(init_app())
    web.run_app(web_app, host="0.0.0.0", port=port)