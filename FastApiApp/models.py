from pydantic import BaseModel
from typing import Optional, List

# Ürün modelleri
class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True

# Satış modelleri
class SaleBase(BaseModel):
    product_id: int
    quantity: int
    sale_date: str
    total_price: float

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    
    class Config:
        from_attributes = True

# Satış istatistikleri
class SaleStats(BaseModel):
    total_sales: float
    total_quantity: int
    avg_sale_price: float

# API yanıt modelleri
class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
