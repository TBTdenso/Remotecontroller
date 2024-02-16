from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = FastAPI()

# 環境変数設定
ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN", "QBP3QwVxDteJgcF83pgs/owHqwzEY1zC94OXgGjZLnbblQOC9CCAybNSaLTNumcyljaFZ7lCLcglQAKLJuYU3g+DkQbYDDdzKixmLfveh2ZYDviVMHDUEivrbmrqKCRpu61jeVX71wUpctUa41P9XQdB04t89/1O/w1cDnyilFU=")
SECRET = os.getenv("LINE_SECRET", "7fc0d703d5cc1412e6c1d0373fdb855b")

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookParser(SECRET)

@app.post("/")
async def callback(request: Request):
    # ヘッダー
    signature = request.headers.get('X-Line-Signature', '')
    
    # リクエストボディ
    body = await request.body()
    body_str = body.decode('utf-8')
    print(body_str)
    
    try: 
        events = handler.parse(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        
        text = event.message.text
        line_user_id = event.source.user_id
        global a
        if text in AirOnWords:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=AirOn))
            a = 1
        elif text in AirOffWords:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=AirOff))
            a = 2
        elif text in TempupWords:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=Tempup))
            a = 3
        elif text in TempdownWords:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=Tempdown))
            a = 4
        elif text in ChangeDriveWords:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=ChangeDrive))
            a = 5
        elif text in HightPowerWords:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=HightPower))
            a = 6
        elif text in AirVelocityWords:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=AirVelocity))
            a = 7
        elif text in AirWindWords:
            line_bot_api.push_message(line_user_id, TextSendMessage(text=Airwind))
            a = 8
    
    return JSONResponse(content={"status": "OK"})

# フラグ用グローバル変数
a = 0

@app.get("/")
async def handle_get_request():
    global a
    b = a
    a = 0
    print("accept_" + str(b))
    # GETリクエスト時のパラメータをbot経由で通知
    # line_bot_api.push_message("Ufc2f9581f7270b02bdf52f7ae30c337f", TextSendMessage(text="accept_" + str(b)))
    return {"message": f"%%%{b}%%%"}

AirOn = 'エアコンをオンにしました。'
AirOff = 'エアコンをオフにしました'
Tempup = '温度を1度上げました'
Tempdown = '温度を1度下げました'
ChangeDrive = '運転切り替えしました'
HightPower = 'ハイパワーにしました'
AirVelocity = '風速を切り替えました'
Airwind = '風当てを切り替えました'
AirOnWords = ['エアコンの電源入れて','エアコンの電源を入れて','エアコンオン']
AirOffWords = ['エアコン消して','エアコンの電源を消して','エアコンオフ']
TempupWords = ['エアコンの温度を上げて','エアコン温度上昇','エアコンの温度上げて']
TempdownWords = ['エアコンの温度を下げて','エアコンの温度下げて']
ChangeDriveWords = ['運転切り替え','運転切替','運転切り替えして','運転切替して','運転を切り替えて']
HightPowerWords = ['ハイパワー','ハイパワーにして','ハイパワーに切り替えて']
AirVelocityWords = ['風速切替','風速を変えて','風速切り替え','風速を切り替えて']
AirWindWords = ['風当て','風当てして']
