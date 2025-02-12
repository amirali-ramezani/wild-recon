from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess
import os

app = FastAPI()


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def run_bash_script(script: str, domain: str) -> str:
    try:
        result = subprocess.run(['bash', script, domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running {script}: {e}")

def save_to_file(filename: str, data: str):
    with open(filename, 'w') as f:
        f.write(data)

def remove_duplicates(filename: str):
    if not os.path.exists(filename):
        return
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    unique_lines = sorted(set(line.strip() for line in lines))
    
    with open(filename, 'w') as f:
        for line in unique_lines:
            f.write(f"{line}\n")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "subdomains": None})

@app.post("/recon")
def run_recon(request: Request, domain: str = Form(...)):
    output1 = run_bash_script('amass-brute-sub.sh', domain)
    output2 = run_bash_script('amass-sub-enum.sh', domain)
    output3 = run_bash_script('subfinder-automate.sh', domain)
    
    combined_output = output1 + output2 + output3
    save_to_file('subdomains.txt', combined_output)
    remove_duplicates('subdomains.txt')
    
    subprocess.run(['bash', 'httpx.sh', 'subdomains.txt'])
    
    with open('subdomains.txt', 'r') as f:
        subdomains = f.readlines()
    
    return templates.TemplateResponse("index.html", {"request": request, "subdomains": subdomains})
