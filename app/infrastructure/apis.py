from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def check_health():
    return {"status": "ok"}


# @router.get("/version")
# def get_version():
#     return ResponseBuilder(
#         {
#             "image_version": environ.get("IMAGE_VERSION"),
#             "release_version": environ.get("RELEASE_VERSION"),
#             "git_commit_id": environ.get("GIT_COMMIT_ID"),
#             "git_branch": environ.get("GIT_BRANCH"),
#         }
#     ).build_success()


# @router.get("/env")
# def get_env():
#     return ResponseBuilder(
#         {
#             "app_env": environ.get("APP_ENV"),
#             "config_hash": environ.get("CONFIG_HASH"),
#             "config_commit_id": environ.get("CONFIG_COMMIT_ID"),
#         }
#     ).build_success()
