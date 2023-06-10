from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from quiz import get_question, get_random_question_from_api

app = FastAPI(title="Victorina")

class InputData(BaseModel):
    questions_num: int = Field(title='Quantity of questions')

@app.post("/quiz")
async def get_questions(item: InputData):
    prev_quest = get_question(item.questions_num)
    #prev_quest = get_random_question_from_api(1)

    return prev_quest


if __name__ == '__main__':
    print("start app :::::::::::::::::::::::::::::::::::::::::::::::::::: 2")
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
