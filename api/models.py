from pydantic import BaseModel, BaseSettings, Field
import datetime


class Question(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime.datetime
    category_id: int
    value: int | None = 0
    created_rec: datetime.datetime


class Category(BaseModel):
    id: int
    title: str

class PostgresDsn(BaseSettings):
    dbname: str = Field(..., env="DB_NAME")
    user: str = Field(..., env="DB_USER")
    password: str = Field(..., env="DB_PASSWORD")
    host: str = Field(..., env="DB_HOST")
    port: int = Field(..., env="DB_PORT")
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

POSTGRES_DSN = PostgresDsn().dict()
