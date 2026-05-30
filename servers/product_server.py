from mcp.server.fastmcp import FastMCP

from shared.products import PRODUCTS
from shared.cart import CART
from shared.cart_store import (
    load_cart,
    save_cart,
    clear_cart,
)

mcp = FastMCP("ShoppingServer")


@mcp.tool()
def search_products(category: str):
    """
    Search products by category.
    """

    results = [
        product
        for product in PRODUCTS
        if product["category"].lower() == category.lower()
    ]

    return results


@mcp.tool()
def get_product_by_name(name: str):
    """
    Find products by product name.
    """

    results = [
        product
        for product in PRODUCTS
        if name.lower() in product["name"].lower().lower()
    ]

    return results if results else [{"message": "No matching product found"}]


@mcp.tool()
def list_categories():
    """
    List all available product categories.
    """

    categories = list(set(product["category"] for product in PRODUCTS))

    return categories


@mcp.tool()
def add_to_cart(product_name: str):
    """
    Add a product to shopping cart.
    """

    cart = load_cart()

    product = next(
        (p for p in PRODUCTS if product_name.lower() in p["name"].lower()),
        None,
    )

    if not product:
        return {"message": "Product not found"}

    cart.append(product)

    save_cart(cart)

    return {
        "message": f"{product['name']} added to cart",
        "cart_items": cart,
    }


@mcp.tool()
def view_cart():
    """
    View all items currently in cart.
    """

    return load_cart()


@mcp.tool()
def checkout():
    """
    Checkout all items from cart.
    """

    cart = load_cart()

    if not cart:
        return {"message": "Cart is empty"}

    total = sum(item["price"] for item in cart)

    result = {
        "message": "Checkout successful",
        "total_amount": total,
        "items": cart,
    }

    clear_cart()

    return result


if __name__ == "__main__":
    mcp.run()
