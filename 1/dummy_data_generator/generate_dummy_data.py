import yaml #필요한 라이브러리 가져오기
import random #구성파일 읽기용 랜덤 가져오기
from sqlalchemy import create_engine, MetaData, Table # DB 연결 및 반영을 위한 SQL 구성요소
from sqlalchemy.orm import sessionmaker # DB와의 세션 작성
from faker import Faker # 더미 데이터 생성용
from pathlib import Path # 파일 경로 처리용

# 데이터베이스 연결 문자열(실제 데이터베이스 자격 증명으로 대체)
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 데이터베이스 연결 문자열(실제 데이터베이스 자격 증명으로 대체)
DATABASE_URI = 'mysql+pymysql://username:password@localhost/dbname'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

#테이블 정보를 보유할 MetaData 개체
metadata = MetaData()
metadata.reflect(bind=engine)

# 더미 데이터를 생성하는 faker 인스턴스
fake = Faker()

#테이블의 모든 데이터를 지우는 기능
def clear_table(table):
    session.execute(table.delete())
    session.commit()

#더미 데이터를 생성하고 테이블에 삽입하는 기능
def generate_data(table, count):
    data = []
    for _ in range(count):
        row = {}
        for column in table.columns:
            if column.name == 'id':
                continue
        if column.type.python_type is int:
            row[column.name] = random.randint(1,100)
        elif column.type.python_type is str:
            row[column.name] = fake.text(max_nb_chars=20)
        elif column.type.python_type is float:
            row[column.name] = random.uniform(1.0, 100.0)
        elif column.type.python_type is bool:
            row[column.name] = random.choice(True, False)
        elif column.type.python_type is datetime.date:
            row[column.name] = fake.date()
            #필요에 따라 더 많은 데이터 유형 추가
        data.append(row)
    session.execute(table.insert(), data)
    session.commit()

#구성을 읽고 데이터를 생성하는 주요 기능
def main():
    settings = config['settings']
    delete_existing = settings['delete_existing']
    tables_config = settings['tables']

    for table_config in table_config:
        table_name = table_config['name']
        count = table_config['count']

        table = Table(table_name, metadata, autoload_with=engine)
        if delete_existing:
            clear_table(table)
        generate_data(table, count)
        print(f"Inserted {count} rows into {table_name}")
if __name__ == "__main__":
    main()

#필요한 라이브러리 가져오기
#yaml: 구성 파일을 읽는 데 사용됩니다.
#random: 임의의 값을 생성하는 데 사용됩니다.
#sqlalchemy: 데이터베이스와 상호작용합니다.
#Faker: 더미 데이터 생성용.
#pathlib: 파일 경로를 처리하기 위한 것입니다.
