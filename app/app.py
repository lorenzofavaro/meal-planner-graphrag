import chainlit as cl
from logic.authCallback import execute as authCallback
from logic.onChatStart import execute as onChatStart
from logic.onMessage import execute as onMessage
from logic.onStarters import execute as onStarters


@cl.set_starters
async def set_starters():
    return await onStarters()


@cl.on_chat_start
async def start():
    await onChatStart()


@cl.on_message
async def on_message(message: cl.Message):
    await onMessage(message)


@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    return await authCallback(username, password)


if __name__ == "__main__":
    from chainlit.cli import run_chainlit

    run_chainlit(__file__)
