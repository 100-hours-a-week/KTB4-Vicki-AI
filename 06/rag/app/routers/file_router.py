from fastapi import APIRouter, UploadFile, File, Request, HTTPException

from app.services.file_storage_service import FileStorageService
from app.services.document_loader import DocumentLoader

router = APIRouter(prefix="/api/v1", tags=["File"])

service = FileStorageService()
loader = DocumentLoader()


@router.get("/files")
def get_files():
    files = service.list_files()

    return {"count": len(files), "files": files}


@router.post("/files")
async def upload_file(request: Request, file: UploadFile = File(...)):

    try:
        save_path = service.save_file(file)
        loaded_file = loader.load_document(str(save_path))
        vector_store = request.app.state.vector_store
        vector_store.index_document(loaded_file)

    except Exception as e:
        if save_path.exists():
            save_path.unlink()

        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "파일 업로드 성공", "filename": save_path.name}


@router.post("/files/index")
def index_all_files(request: Request):
    vector_store = request.app.state.vector_store
    files = service.list_files()

    success = 0
    failed = []

    for filename in files:
        try:
            file_path = service.get_file(filename)
            document = loader.load_document(str(file_path))
            vector_store.index_document(document)
            success += 1
        except Exception as e:
            failed.append({"file": filename, "error": str(e)})

    return {"indexed": success, "failed": failed}


@router.delete("/files/{filename}")
def delete_file(filename: str, request: Request):
    file_path = service.get_file(filename)
    vector_store = request.app.state.vector_store
    vector_store.delete_documents(str(file_path))
    service.delete_file(filename)

    return {"message": "삭제 완료"}


@router.delete("/reset")
def reset_collection(request: Request):
    vector_store = request.app.state.vector_store
    vector_store.reset_collection()

    # files = service.list_files()

    # for file in files:
    #    service.delete_file(file)

    return {"message": "초기화 완료"}
