from fastapi import APIRouter
from social_network.routers.AuthRouter import router as authRouter
from social_network.routers.FacebookRouter import router as facebookRouter
from social_network.routers.MessengerRouter import router as messengerRouter
from social_network.routers.PostRouter import router as postRouter

router = APIRouter()

router.include_router(authRouter)
router.include_router(facebookRouter)
router.include_router(messengerRouter)
router.include_router(postRouter)
