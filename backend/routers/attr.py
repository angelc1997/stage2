from typing import List
from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel
from ..models.Attraction import AttractionModel
attr = APIRouter()


class Attraction(BaseModel):
    id: int = 1
    name: str = "新北投溫泉區"
    category: str = "養生溫泉"
    description: str = "北投溫泉從日據時代便有盛名，深受喜愛泡湯的日人自然不會錯過"
    address: str = "臺北市  北投區中山路、光明路沿線"
    transport: str = "216、218、223、230、266、602、小6、小7、小9、、小22、小25、小26至新北投站下車"
    mrt: str = "新北投"
    lat: float = 25.137077
    lng: float = 121.508447
    images: List[str] = ["https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000848.jpg"]


class AttrResponse(BaseModel):
    data: List[Attraction]

class AttrListResponse(BaseModel):
    nextPage: int = 1
    data: List[Attraction]
    
class ErrorResponse(BaseModel):
    error: bool = True
    message: str = "請按照情境提供對應的錯誤訊息"



@attr.get("/attractions",
          summary = "取得景點資料列表",
          description = "取得不同分頁的旅遊景點列表資料，也可以根據標題關鍵字、或捷運站名稱篩選",
          responses = {
              200: {"model": AttrListResponse, "description": "正常運作"},
              500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}})

async def get_attractions(
    page: int= Query(..., ge=0, description="要取得的分頁，每頁 12 筆資料"), 
    keyword: str = Query(None, description="用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選")):
    
    try:
        all_data = AttractionModel.get_attr_list(page, keyword)
        attractions = [
            {"id": i[0], 
            "name": i[1],
            "category": i[3],
            "description": i[9],
            "address": i[4],
            "transport": i[8],
            "mrt": i[5],
            "lat": i[7],
            "lng": i[6],
            "images":(i[-1].split(","))} 
            for i in all_data[:12]]

        # Check data size
        if len(all_data) == 0:
            return {"nextPage": None, "data": None}

        if len(all_data) < 13:
            return {"nextPage": None, "data": attractions}
        
        else:
            return {"nextPage": page + 1, "data": attractions}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail= {"error": True, "message": "伺服器內部錯誤"})



@attr.get("/attraction/{attractionId}",    
          
          summary = "根據景點編號取得景點資料", responses={
              200: {"model": AttrResponse, "description": "景點資料"},
              400: {"model": ErrorResponse,"description": "景點編號不正確"},
              500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}})

async def get_attraction(attractionId: int = Path(..., description="景點編號")):


    try:
        data = AttractionModel.get_attr_detail(attractionId)

        if data is None:
            return {"data": None}

      
        return {"data": {"id": data[0], "name": data[1], "category": data[3], "description": data[9], "address": data[4], "transport": data[8], "mrt": data[5], "lat": data[7], "lng": data[6], "images": data[-1]}}
        

    except Exception as e:    

        raise HTTPException(status_code=500, detail={"error": True, "message": "伺服器內部錯誤"})
    


