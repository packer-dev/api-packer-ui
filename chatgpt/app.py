from openai import OpenAI
from typing import List
from fastapi import APIRouter
from chatgpt.models import Role, ChatGPT
from firebase_admin import db

router = APIRouter()

client = OpenAI(
    api_key="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",
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


@router.post("api/chat-gpt/history/save")
async def saveHistory(param: ChatGPT):
    ref = db.reference("chatGPT")
    data = ref.get()

    param = param.model_dump()
    if data is None:
        data = {}
    data[param["userId"]] = param["list"]
    ref.set(data)
