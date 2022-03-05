from app.dbconn import engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.automap import automap_base

Base = automap_base()

class Products(Base):
    __tablename__ = 'products'

    id= Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    it_sale = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))

Base.prepare(engine, reflect=True)



















# products = Base.classes.products
# metadata = MetaData()

# metadata.reflect(engine)

# # @event.listens_for(Base.metadata, "column_reflect")
# # def column_relect(inspector, table, column_info):
# #     column_info['key'] = "attr_%s" % column_info['name'].lower()

# # Base.prepare(engine, reflect=True)

# Table('products', metadata, Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')))

# Base = automap_base(metadata=metadata)

# Base.prepare()

# products = Base.classes.products