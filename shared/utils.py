import re

CATEGORY_PATTERNS = {
    "mobile": [
        r"phone",
        r"phones",
        r"mobile",
        r"mobiles",
        r"smartphone",
        r"smartphones",
        r"cell phone",
    ],
    "laptop": [
        r"laptop",
        r"laptops",
        r"notebook",
        r"notebooks",
        r"gaming laptop",
        r"macbook",
    ],
}


PRODUCT_PATTERNS = {
    "dell": [r"dell", r"dell laptop", r"dell laptops"],
    "iphone": [r"iphone", r"apple phone"],
    "samsung": [r"samsung", r"galaxy"],
}


def normalize_category(text: str):

    text = text.lower()

    for category, patterns in CATEGORY_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, text):
                return category

    return text


def normalize_product_name(text: str):

    text = text.lower()

    for canonical_name, patterns in PRODUCT_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, text):
                return canonical_name

    return text
