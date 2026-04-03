from pydantic_settings import BaseSettings
#fastapi에서 설정관리할때 자주 사용
#환경변수에서 값을 자동으로 불러올 수 있는 클래스

class Settings(BaseSettings):
    db_user:str="root"
    db_password:str="1234"
    db_host:str="localhost"
    db_port:str="3306"
    db_name:str="board"

class Config:
    env_file=".env"
    case_sensitive=True
    extra="allow"
    populate_by_name=True

@property
def tmp_db(self) -> str:
    return f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

@property
def db_url(self) -> str:
    return f"mysql+asyncmy://{self.tmp_db}"

@property
def sync_db_url(self) -> str:
    return f"mysql+pymysql://{self.tmp_db}"


settings=Settings()
