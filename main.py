from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from bs4 import BeautifulSoup
import requests

USER_AGENT = [
    "Mozilla/5.0 (Linux; Android 9; SM-G955F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; ANE-LX1 Build/HUAWEIANE-L01; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1Go; 8227L_demo) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; M2010J19SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.6.1.151 Yowser/2.5 Yptp/1.23 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1; Turkcell_T_Tablet Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.91 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1.0; Nexus 10 Build/LMY49F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/600.1.4",
    "Mozilla/5.0 (Linux; Android 10; Redmi Note 9S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 OPR/62.2.3146.57547",
    "Mozilla/5.0 (Linux; Android 10; SM-N975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36"
]

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/convert", response_class=HTMLResponse)
async def submit_form(request: Request):
    form_data = await request.form()

    text1 = form_data["form1"]
    text2 = form_data["form2"]
    text3 = form_data["form3"]

    HEADERS = {}
    for agent in USER_AGENT:
        HEADERS["User-Agent"] = agent

    link = f"https://www.forbes.com/advisor/money-transfer/currency-converter/{text2.lower()}-{text3.lower()}/?amount={text1.lower()}"

    r = requests.get(link, headers=HEADERS)

    soup = BeautifulSoup(r.text, "lxml")
    get_res = soup.find("h2", class_='result-box-conversion')

    get_span = get_res.find("span", class_="amount").text

    result = f"{text1} {text2} = {get_span} {text3}".upper()

    return templates.TemplateResponse("index.html", {"request": request, "text1": result})
