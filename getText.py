from fasthtml.common import *

app, rt = fast_app(exts='ws')

# Input field that gets reset after sending
def mk_input(): 
    return Input(id='msg', placeholder="Type your message", value="", hx_swap_oob="true")

@rt('/')
def index():
    return Div(
            Form(mk_input(), ws_send=True),
            hx_ext='ws', ws_connect='/ws'
        )

@app.ws('/ws')
async def ws(msg: str, send):
    # Print the message to terminal
    print(msg)
    
    # Reset the input field
    await send(mk_input())
    
serve()