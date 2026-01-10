from fastapi import FastAPI, APIRouter,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController,ProjectController,ProcessController
import aiofiles
import logging
from models import ResponsFiles
from .schemes.data import ProcesseRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel    

from models.db_schema import Data_chunk    
from models.AssetModel import AssetModel
from models.db_schema import Asset
from models.enums.AssetTypeEnum  import AssetTypeEnum

from bson.objectid import ObjectId


logger=logging.getLogger("uploadfile.uncorn")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)
@data_router.post("/upload/{project_id}")
async def upolad_data(request :Request,project_id: str,file :UploadFile,app_settings : Settings=Depends(get_settings)):
    #print(request.app.dbclient)
    projectModel=await ProjectModel.create_instance(dbclient=request.app.dbclient)

    prject= await projectModel.get_project_or_createone(project_id=project_id)
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
   # print (prject)
    assetModel=await AssetModel.create_instance(dbclient=request.app.dbclient)
    asset_record=Asset(
        asset_project_id=ObjectId(prject.id) if isinstance(prject.id,str) else prject.id,
        asset_type=AssetTypeEnum.file.value ,
        asset_name=new_fiel_key,
        asset_size=os.path.getsize(file_path) 
    )
    print("asset_record",asset_record)

    added_asset_record = await assetModel.create_asset(asset=asset_record)   


    return JSONResponse(
            content={
                "Result": ResponsFiles.File_upload_sucess.value,
                "new_file_key":new_fiel_key ,
                "added_asset_record":str(added_asset_record.id)     
             
                  
            }
        )
#staring the new end point here
@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str,process_request:ProcesseRequest):
            file_id = process_request.file_id
            chunk_size = process_request.chunk_size
            overlap_size = process_request.overlap_size
            do_reset=process_request.do_reset
            
            projectModel=await ProjectModel.create_instance(dbclient=request.app.dbclient)

            prject= await projectModel.get_project_or_createone(project_id=project_id)
             

             #get all project files if file_id is None or file_id.strip()=="":
             #or get specific file
            assetModel=await AssetModel.create_instance(dbclient=request.app.dbclient)
            
            project_file_ids={}
            if (process_request.file_id is not None) and (process_request.file_id.strip()!=""):
                #project_file_ids.append(process_request.file_id)
                project_assets= await assetModel.get_project_assets_byname(
                    asset_project_id=prject.id,
                    asset_name=process_request.file_id
                )
                if project_assets is None:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            "signal": ResponsFiles.error_file_not_found.value
                        }
                        )

                project_file_ids = { project_assets.id: project_assets.asset_name
                }

            else:
                #get all project files
                
                project_assets= await assetModel.get_project_assets(
                    asset_project_id=prject.id,
                    asset_type=AssetTypeEnum.file.value 
                )
                project_file_ids = {
                    asset.id: asset.asset_name
                for asset in project_assets
                }

 
           

        
            if len( project_file_ids)==0:
                 return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponsFiles.no_files_to_process.value
            }
            )



            chunkModel=await  ChunkModel.create_instance(dbclient=request.app.dbclient)    
            # deletecCout=0
            if (do_reset==1):
                    deletecCout= await chunkModel.delete_project_chunks(project_id=prject.id)


            process_controller = ProcessController(project_id=project_id)
            file_chunks_all=0
            numberofadded_all=0
            number_file_count=0



            for  asset_id,file_id in project_file_ids.items():
                
                file_content = process_controller.get_file_content(file_id=file_id)
                if file_content is None:
                    logger.error(f"file content is None for file id :{file_id}")
                    continue    


                file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )
                file_chunks_all += len(file_chunks) 

              
                


                file_chunk_records=[
                    Data_chunk(
                        chunk_text =chunk.page_content
                        ,check_metdadata=chunk.metadata
                        ,chunk_order=index +1
                        ,chunk_project_id=ObjectId(prject.id)
                        ,chunk_asset_id=asset_id
                        ) for index,chunk in enumerate(file_chunks)

                ]
              
                numberofadded =await chunkModel.create_multiple_chunks_bsize_v3(
                    chunks=file_chunk_records)
                numberofadded_all += numberofadded
                number_file_count+=1

            if file_chunks_all== 0:
                    return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponsFiles.PROCESSING_FAILED.value
                }
            )
            return JSONResponse(    
            content={
                 "signal": ResponsFiles.PROCESSING_SUCESS.value,
                 "deletecCout":deletecCout if do_reset==1 else 0,

                "number_of_added_chunks":   numberofadded_all,
                "total_files_processed":number_file_count,

            }
            )
