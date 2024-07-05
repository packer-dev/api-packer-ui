from openai import OpenAI
from typing import List
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from chatgpt.models import Role, ChatGPT
from firebase_admin import db
from utils import find_index
import json
from asyncio import sleep
from utils import find_index

router = APIRouter()

client = OpenAI(
    api_key="sk-proj-TUafaX3bRK4ZmSSJxtSMT3BlbkFJTLCSSnIPwVnamhbZOq8W",
)


def get_chat_completion(messages, model="gpt-3.5-turbo"):

    newMessages = []
    for item in messages:
        newMessages.append({"role": item.role, "content": item.content})
    response = client.chat.completions.create(
        model=model, messages=newMessages, temperature=0, max_tokens=1000
    )

    # Returning the extracted response
    return response.choices[0].message.content


@router.post("/v4/chat-gpt")
async def get_chat_gpt_v4():
    return 'Xin lỗi về sự nhầm lẫn trước đó. Dưới đây là một ví dụ về code JavaScript để tính tổng của các số trong một mảng:\n\n```javascript\n// Mảng chứa các số cần tính tổng\nconst numbers = [1, 2, 3, 4, 5];\n\n// Khởi tạo biến sum để lưu tổng\nlet sum = 0;\n\n// Duyệt qua từng phần tử trong mảng và cộng vào tổng\nfor (let i = 0; i < numbers.length; i++) {\n    sum += numbers[i];\n}\n\n// In ra tổng\nconsole.log("Tổng của các số trong mảng là: " + sum);\n```\n\nTrong ví dụ trên, chúng ta khởi tạo một mảng `numbers` chứa các số cần tính tổng. Sau đó, chúng ta sử dụng một vòng lặp `for` để duyệt qua từng phần tử trong mảng và cộng vào biến `sum`. Cuối cùng, chúng ta in ra tổng của các số trong mảng.'


@router.post("/v3/chat-gpt")
async def get_chat_gpt_v3():
    return "Open this HTML file in a browser, and as you scroll through the page, the current vertical scroll position will be displayed in the browser's console. Adjust the height property in the CSS to add more or less content and observe the scroll position changes."


@router.post("/v2/chat-gpt")
async def get_chat_gpt_v2():
    return "Để tính tổng của một mảng số trong JavaScript, bạn có thể sử dụng một trong các cách sau:\n\n1. Sử dụng vòng lặp for:\n```javascript\nfunction tinhTong(arr) {\n  let tong = 0;\n  for (let i = 0; i < arr.length; i++) {\n    tong += arr[i];\n  }\n  return tong;\n}\n\nlet mangSo = [1, 2, 3, 4, 5];\nconsole.log(tinhTong(mangSo)); // Kết quả: 15\n```\n\n2. Sử dụng phương thức reduce:\n```javascript\nlet mangSo = [1, 2, 3, 4, 5];\nlet tong = mangSo.reduce((accumulator, currentValue) => accumulator + currentValue, 0);\nconsole.log(tong); // Kết quả: 15\n```\n\n3. Sử dụng vòng lặp forEach:\n```javascript\nlet mangSo = [1, 2, 3, 4, 5];\nlet tong = 0;\nmangSo.forEach((so) => {\n  tong += so;\n});\nconsole.log(tong); // Kết quả: 15\n```\n\nCác cách trên đều sẽ tính tổng của các phần tử trong mảng số và trả về kết quả. Bạn có thể chọn cách nào phù hợp với nhu cầu của mình."


@router.post("/v1/chat-gpt")
async def get_chat_gpt_v1(messages: List[Role]):
    return get_chat_completion(messages)


@router.post("/api/chat-gpt/history/save")
async def saveHistory(param: ChatGPT):
    ref = db.reference("chatGPT")
    data = ref.get()

    param = param.model_dump()
    if data is None:
        data = {}

    userId = param["userId"]
    history = param["history"]
    list = []
    if userId in data:
        list = data[userId]
    index = find_index(list, history["id"])
    if index == -1:
        list.append(history)
    else:
        list[index] = history
    data[userId] = list
    ref.set(data)
    return True


@router.put("/api/chat-gpt/history/list")
async def getHistory(userId: str):
    ref = db.reference("chatGPT")
    data = ref.get()
    if data is None:
        return None
    if userId in data:
        for index, obj in enumerate(data[userId]):
            data[userId][index]["isArchive"] = (
                True if obj["isArchive"] == False else True
            )
        ref.set(data)
        return True
    else:
        return None


@router.get("/api/chat-gpt/history/get")
async def getHistory(id: str):
    ref = db.reference("chatGPT")
    data = ref.get()
    if data is None:
        return []
    if id in data:
        return data[id]
    else:
        return []


@router.delete("/api/chat-gpt/history/delete")
async def deleteHistory(userId: str, historyId: str):
    ref = db.reference("chatGPT")
    data = ref.get()
    if data is None:
        return False
    if userId not in data:
        return False
    list = data[userId]
    list = [obj for obj in list if str(obj["id"]) != historyId]
    data[userId] = list
    ref.set(data)
    return True


@router.delete("/api/chat-gpt/history/delete/all")
async def deleteHistory(userId: str):
    ref = db.reference("chatGPT")
    data = ref.get()
    if data is None:
        return False
    if userId not in data:
        return False
    data[userId] = []
    ref.set(data)
    return True


@router.get("/api/chat-gpt/history")
async def getHistoryById(userId: str, historyId: str):
    ref = db.reference("chatGPT")
    data = ref.get()

    if data is None:
        return None
    if userId not in data:
        return None

    list = data[userId]
    list = [obj for obj in list if str(obj["id"]) == historyId]

    return list[0] if len(list) == 1 else None


@router.get("/api/chat-gpt/history/share")
async def getHistoryById(historyId: str):
    ref = db.reference("chatGPT")
    data = ref.get()

    if data is None:
        return None
    keys = data.keys()
    list = []
    for key in keys:
        list = list + data[key]

    index = find_index(list, historyId)

    if index == -1:
        return None
    else:
        return list[index]


async def waypoints_generator():
    for i in range(5):
        data = json.dumps({"lat": 22.09769, "lng": 87.24068})
        yield f"event: locationUpdate\ndata: {data}\n\n"
        await sleep(1)


@router.get("/api/steam")
async def testSSE():
    return StreamingResponse(waypoints_generator(), media_type="text/event-stream")
