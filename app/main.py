from fastapi import FastAPI

from .routers import auth, livres, utilisateurs

app = FastAPI(
	title="App Gestion Maison d Edition",
	version="0.1.0",
)


@app.get("/health", tags=["Système"])
def health_check():
	return {"status": "ok"}


app.include_router(utilisateurs.router)
app.include_router(livres.router)
app.include_router(auth.router)
