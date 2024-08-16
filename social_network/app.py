from fastapi import APIRouter
from social_network.routers.AuthRouter import router as authRouter
from social_network.routers.FacebookRouter import router as facebookRouter
from social_network.routers.MessageRouter import router as messengerRouter
from social_network.routers.PostRouter import router as postRouter
from social_network.routers.CommonRouter import router as commonRouter
from social_network.routers.CommentRouter import router as commentRouter

router = APIRouter()

router.include_router(authRouter)
router.include_router(facebookRouter)
router.include_router(messengerRouter)
router.include_router(postRouter)
router.include_router(commonRouter)
router.include_router(commentRouter)
