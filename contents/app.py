from firebase_admin import db
from fastapi import APIRouter
from contents.models import Content
from utils import find_index

router = APIRouter()


@router.post("/components/content-list")
async def update_content_list(idComponent: str, content: Content):
    ref = db.reference("components")
    components = ref.get()
    index = find_index(components, idComponent)
    content = content.model_dump()
    if index == -1:
        return index
    else:
        components[index]["contents"] = [content]
        if "list" in content and content["list"] is not None:
            if len(content["list"]) == 0:
                contents = [
                    x
                    for x in components[index]["contents"]
                    if str(x["id"]) != str(content["id"])
                ]
                components[index]["contents"] = contents
        ref.set(components)
        return index


@router.post("/components/content")
async def get_props_by_id_component(idComponent: str, content: Content):
    ref = db.reference("components")
    components = ref.get()
    index = find_index(components, idComponent)
    content = content.model_dump()
    if index == -1:
        return []
    else:
        if (
            "contents" in components[index]
            and components[index]["contents"] is not None
        ):
            contents = components[index]["contents"]
            indexContent = find_index(contents, content["id"])
            if indexContent != -1:
                contents[indexContent] = content
            else:
                contents.append(content)

            components[index]["contents"] = contents
        else:
            components[index]["contents"] = [content]

        ref.set(components)
        return []


@router.delete("/components/content")
async def delete_content_list(idComponent: str, idContent: str):
    ref = db.reference("components")
    components = ref.get()
    index = find_index(components, idComponent)
    if index == -1:
        return []
    else:
        if (
            "contents" in components[index]
            and components[index]["contents"] is not None
        ):
            contents = [
                x
                for x in components[index]["contents"]
                if str(x["id"]) != str(idContent)
            ]
            components[index]["contents"] = contents

        ref.set(components)
        return []
