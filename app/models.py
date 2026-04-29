from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Product(Base):
    __tablename__ = "products"

    product_id          = Column(Integer, primary_key=True, autoincrement=True)
    product_name        = Column(String(120), nullable=False)
    product_description = Column(Text, nullable=True)
    product_category    = Column(String(80), nullable=True)
    product_price       = Column(Numeric(10, 2), nullable=False)
    product_stock       = Column(Integer, default=0, nullable=True)
    product_image       = Column(String(500), nullable=True)

    def to_dict(self):
        return {
            "product_id":          self.product_id,
            "product_name":        self.product_name,
            "product_description": self.product_description or "",
            "product_category":    self.product_category or "",
            "product_price":       str(self.product_price),
            "product_stock":       self.product_stock or 0,
            "product_image":       self.product_image or "",
        }

    def __repr__(self):
        return f"<Product id={self.product_id} name={self.product_name!r}>"


class User(Base):
    __tablename__ = "users"

    user_id    = Column(Integer, primary_key=True, autoincrement=True)
    username   = Column(String(80),  unique=True, nullable=False)
    email      = Column(String(120), unique=True, nullable=False)
    password   = Column(String(256), nullable=False)
    role       = Column(String(20),  nullable=False, default="customer")  # 'customer' | 'admin'
    created_at = Column(DateTime, server_default=func.now())

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User id={self.user_id} username={self.username!r} role={self.role!r}>"


class Order(Base):
    __tablename__ = "orders"

    order_id   = Column(Integer, primary_key=True, autoincrement=True)
    user_id    = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    total      = Column(Numeric(10, 2), nullable=False)
    status     = Column(String(30), nullable=False, default="pending")
    created_at = Column(DateTime, server_default=func.now())

    items = relationship("OrderItem", back_populates="order")
    user  = relationship("User")

    def __repr__(self):
        return f"<Order id={self.order_id} total={self.total} status={self.status!r}>"


class OrderItem(Base):
    __tablename__ = "order_items"

    item_id       = Column(Integer, primary_key=True, autoincrement=True)
    order_id      = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id    = Column(Integer, ForeignKey("products.product_id"), nullable=True)
    product_name  = Column(String(120), nullable=False)
    product_price = Column(Numeric(10, 2), nullable=False)
    quantity      = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")

    def __repr__(self):
        return f"<OrderItem order={self.order_id} product={self.product_name!r} qty={self.quantity}>"
