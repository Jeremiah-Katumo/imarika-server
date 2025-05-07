
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import org_models
from .routes import (
    auth_routes, contact_routes, faqs_routes, org_routes, 
    branches_routes, tenders_routes)
from .routes.careers_routes import team_routes, departments_routes
from .routes.newscentre_routes import gallery_routes, latestnews_routes, statementspressrelease_routes
from .routes.vacancies_routes import vacancies_routes
from .routes.vacancies_routes.applications_routes import vacancyapplicationfile_routes
from .routes.downloads_routes import downloadfiles_routes
from .routes.product_routes import mainproducts_routes
from .database import engine


app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

org_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Welcome to Imarika Foundation"}   


app.include_router(auth_routes.router)
app.include_router(contact_routes.router)
app.include_router(faqs_routes.router)
app.include_router(org_routes.router)
# Branches
app.include_router(branches_routes.router)
# Careers
app.include_router(team_routes.router)
app.include_router(departments_routes.router)
# News centre
app.include_router(gallery_routes.router)
app.include_router(latestnews_routes.router)
app.include_router(statementspressrelease_routes.router)
# Vacancies
app.include_router(vacancies_routes.router)
app.include_router(vacancyapplicationfile_routes.router)
# Downloads
app.include_router(downloadfiles_routes.router)
# Products
app.include_router(mainproducts_routes.router)
# Tenders
app.include_router(tenders_routes.router)
