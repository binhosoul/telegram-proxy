import os
import asyncio
from aiohttp import web
from pyrogram import Client

# Pega as chaves configuradas no Render
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Inicializa o cliente do Pyrogram (Telegram)
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Servidor Proxy do Telegram para Bob Player Rodando com Sucesso!")

@routes.get("/video/{chat_id}/{message_id}")
async def stream_video(request):
    chat_id = request.match_info.get("chat_id")
    message_id = int(request.match_info.get("message_id"))
    
    try:
        # Converte o chat_id corretamente se for número inteiro
        target_chat = int(chat_id) if (chat_id.startswith("-") or chat_id.isdigit()) else chat_id
        
        # Busca a mensagem no Telegram
        msg = await app.get_messages(target_chat, message_id)
        
        media = msg.video or msg.document
        if not media:
            return web.Response(text="Nenhum arquivo de vídeo encontrado nesta mensagem.", status=404)
        
        file_size = media.file_size
        
        async def file_sender():
            async for chunk in app.stream_media(msg):
                yield chunk

        response = web.StreamResponse(
            status=200,
            reason='OK',
            headers={
                'Content-Type': 'video/mp4',
                'Content-Length': str(file_size),
                'Accept-Ranges': 'bytes',
            }
        )
        await response.prepare(request)
        async for chunk in file_sender():
            await response.write(chunk)
        await response.write_eof()
        return response
    except Exception as e:
        return web.Response(text=f"Erro ao transmitir vídeo: {str(e)}", status=500)

async def init_web():
    web_app = web.Application()
    web_app.add_routes(routes)
    runner = web.AppRunner(web_app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web rodando na porta {port}")

async def main():
    if API_ID and API_HASH and BOT_TOKEN:
        await app.start()
        print("Bot do Telegram conectado com sucesso!")
    else:
        print("Aviso: Credenciais do Telegram não informadas.")
    
    await init_web()
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())