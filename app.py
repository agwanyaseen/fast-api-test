from pydantic import BaseModel,Field,Requ
from fastapi import FastAPI,HTTPException,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler
from typing import List

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"errors": exc.errors(), "message": "Custom validation failed ❌"},
    )

class Tea(BaseModel):
    id: int
    name: str =  Field(...,min_length=4, max_length=10,name="name",title="name")
    is_available : bool


teas : List[Tea] =[]

@app.get("/tea")
def get_all_teas():
    print(f"Total Teams object is {teas}")
    return teas


@app.post("/tea")
def add_tea(tea: Tea):
    print(f"Tea object is {tea}")
    teas.append(tea)
    print(f"Total Tea object in  Get is {teas}")
    return tea.id

@app.get("/tea/{id}")
def get_tea_by_id(id:int):
    result= next((tea for tea in teas if tea.id==id),None)
    if not result:
        raise HTTPException(status_code=401,detail="Tea not found")
    return result


# if __name__ == "__main__":
#     app

