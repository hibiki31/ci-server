from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn
import datetime
import json
import yaml
import subprocess

from module_ssh import send_json, run_cmd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/gh/{name}")
def gh_name(json_body: dict, name: str, request: Request):
    event = request.headers["X-GitHub-Event"]
    sender_id = json_body["sender"]["login"]
    
    dt_jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')
    dt_now = datetime.datetime.now(dt_jst)
    dt_now_str = dt_now.strftime('%Y-%m%d-%H%M%S')
    dump_file_name = f'dump/{dt_now_str}_{event}_{sender_id}.json'

    # dump
    with open(dump_file_name, 'w') as f:
        json.dump(json_body, f, indent=2)
    
    with open(f'config/{name}.yaml', 'r') as f:
        config = yaml.safe_load(f)
        
    if not sender_id in config["trust_users"]:
        return {"message": "Bad World"}
        
    send_json(
        local_path=dump_file_name,
        remote_path=f"/tmp/ci.json",
        hostname=config["host"],
        user=config["user"]
    )
    
    if event == "push":
        run_cmd(
            hostname=config["host"],
            user=config["user"],
            cmd=config["push_script"]
        )
    
    return {"message": "Hello World"}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)