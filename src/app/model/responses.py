class Response:
    @staticmethod
    def response(message:str,status:str,error_code:str=None,data:any=None):
        response = {"status":status,"message":message}
        if error_code:
            response.update({"error_code":error_code})
        if data:
            response.update({"data":data})
        return response