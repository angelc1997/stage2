from fastapi import *
from fastapi.responses import FileResponse
from routers import user, attr, mrt, book, order
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
app=FastAPI(
	swagger_ui_parameters={"syntaxHighlight": False}, # Disable Syntax Highlight
	title="APIs for Taipei Day Trip",
	summary="台北一日遊網站 API 規格：網站後端程式必須支援這個 API 的規格，網站前端則根據 API 和後端互動。"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://100.28.23.193:8000/", "http://127.0.0.1:8000/"],
    allow_methods=["*"],  
    allow_headers=["*"]
)




# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")



app.include_router(user.user,prefix="/api", tags = ["User"])
app.include_router(attr.attr,prefix="/api", tags = ["Attraction"])
app.include_router(mrt.mrt,prefix="/api", tags = ["MRT Station"])
app.include_router(user.book,prefix="/api", tags = ["Booking"])
app.include_router(order.order,prefix="/api", tags = ["Order"], deprecated=True)



