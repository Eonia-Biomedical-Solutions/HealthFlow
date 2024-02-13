from sqlalchemy import create_engine, Table, Column, String, MetaData, inspect
from sqlalchemy_utils import database_exists, create_database


class Db:
    def __init__(self, dbfile:str):
        self.engine = create_engine(f'sqlite:///{dbfile}', echo=False)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        self.metadata = MetaData()

    def build_table(self, column_names:list, version:str):
        """se encarga de construir una tabla a partir de una lista de variables"""

        columns = [Column(name, String) for name in column_names]
        self.table = Table(
            f'V{version}',
            self.metadata,
            *columns
        )
        
        inspector = inspect(self.engine)
        if not inspector.has_table(f'V{version}'):
            self.metadata.create_all(self.engine)

    def add(self, data:dict):
        """Agrega los datos enviados por el parametro data,
        {columna:valor, columna2:valor}
        """
        try:
            with self.engine.connect() as connection:
                insert_statement = self.table.insert().values(**data)
                connection.execute(insert_statement)
                connection.commit()
                return True
        except:
            return False


if __name__ =='__main__':
    file = 'example.sqlite'
    db = Db(file)
    db.build_table(column_names=['a', 'b'], version=1.0)
    jeje = {
        'a':1, 'b':18
    }
    db.add(jeje)
