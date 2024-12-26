from starlette.responses import JSONResponse


class Response:
    @staticmethod
    def response(message:str,status:str,error_code:str=None,data:any=None):
        response = {"status":status,"message":message}
        if error_code:
            response.update({"error_code":error_code})
        if data:
            response.update({"data":data})
        return response

class CustomErrorResponse:
    @staticmethod
    def error_response(response:dict,http_code:int):
        return JSONResponse(status_code=http_code,content=response)