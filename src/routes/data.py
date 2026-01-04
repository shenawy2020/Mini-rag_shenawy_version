from fastapi import FastAPI, APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController,ProjectController,ProcessController
import aiofiles
import logging
from models import ResponsFiles
from .schemes.data import ProcesseRequest


logger=logging.getLogger("uploadfile.uncorn")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)
@data_router.post("/upload/{project_id}")
async def upolad_data(project_id: str,file :UploadFile,app_settings : Settings=Depends(get_settings)):
    
    is_valid,result_Smg=DataController().validate_uploaded_file(file=file)
    
    if not is_valid:
         return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Result": result_Smg          
            }
                      
         )
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    new_file_name,new_fiel_key=DataController().generate_file_name(origin_filename=file.filename,projectid=project_id)

    file_path=os.path.join(
         project_dir_path,new_file_name
         
    )
         
    try:
         async with aiofiles.open(file_path, 'wb') as f:
             while chunk:=await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
              await f.write(chunk)    

    except Exception as e:
        logging.log(f"error while uploading files {file.filename} :{e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Result": ResponsFiles.File_upload_Field          
            }
                      
         )
    

    return JSONResponse(
            content={
                "Result": ResponsFiles.File_upload_sucess.value,
                "new_file_key":new_fiel_key                
            }
        )
#staring the new end point here
@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request:ProcesseRequest):
            file_id = process_request.file_id
            chunk_size = process_request.chunk_size
            overlap_size = process_request.overlap_size

            process_controller = ProcessController(project_id=project_id)

            file_content = process_controller.get_file_content(file_id=file_id)

            file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )
            

            if file_chunks is None or len(file_chunks) == 0:
                return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponsFiles.PROCESSING_FAILED.value
            }
        )

            return file_chunks