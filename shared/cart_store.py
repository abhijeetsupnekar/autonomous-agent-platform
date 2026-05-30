import json
import os

CART_FILE = "cart.json"


def load_cart():

    if not os.path.exists(CART_FILE):
        return []

    with open(CART_FILE, "r") as f:
        return json.load(f)


def save_cart(cart):

    with open(CART_FILE, "w") as f:
        json.dump(cart, f, indent=2)


def clear_cart():

    save_cart([])
