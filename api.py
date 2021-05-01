from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from functions import *
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates/")


@app.get("/recommandation")
def form_post(request: Request):
    result = ""
    return templates.TemplateResponse('recommandation.html', context={'request': request, 'result': result})


@app.post('/recommandation', response_class=HTMLResponse)
def form_post(request: Request, user_id: int = Form(None), category: str = Form(None), checkboxcategory: bool = Form(False)):
    if get_html(user_id, category, checkboxcategory) == str(user_id):
        result = f'User id {user_id} not in database'
        return templates.TemplateResponse('recommandation.html', context={'request': request, 'result': result})
    html = get_html(user_id, category, checkboxcategory)
    return html
