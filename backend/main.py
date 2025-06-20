from fastapi import FastAPI

app = FastAPI()

name = 'feed'
@app.get(f"/{name}")
async def root():
    return {'Hello': '123'}