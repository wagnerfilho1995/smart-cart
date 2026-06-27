from fastapi import APIRouter

from schema.comparison_schema import ProductComparisonIN, ProductComparisonOUT
from service.comparison_service import compare_products

comparison_controller = APIRouter()


@comparison_controller.post(
    "/compare",
    description="Compara dois produtos e identifica qual possui melhor custo-benefício por unidade base.",
    response_model=ProductComparisonOUT,
    status_code=200,
)
def compare_product_prices(payload: ProductComparisonIN) -> ProductComparisonOUT:
    return compare_products(payload)
