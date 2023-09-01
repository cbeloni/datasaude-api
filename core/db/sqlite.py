from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BaseSqlite = declarative_base()

class Tabela1(BaseSqlite):
    __tablename__ = 'tabela3'
    id = Column(Integer, primary_key=True)
    nome = Column(String)

db1_url = 'sqlite:///db1.sqlite'
engineSqlite = create_engine(db1_url)
SessionSqlite = sessionmaker(bind=engineSqlite)
sessionSqlite = SessionSqlite()

BaseSqlite.metadata.create_all(engineSqlite)


if __name__ == '__main__':
    tabela1_item = Tabela1(nome=f'Exemplo 3')
    sessionSqlite.add(tabela1_item)
    sessionSqlite.commit()

    result1 = sessionSqlite.query(Tabela1).all()
    print('Dados da tabela1:')
    for item in result1:
        print(item.id, item.nome)