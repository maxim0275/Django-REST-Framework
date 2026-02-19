import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Функция создания продукта в Stripe."""

    title_product = f'{product.course_paid.name}' if product.course_paid.name else f'{product.lesson_paid.name}'
    stripe_product = stripe.Product.create(name=f'{title_product}')
    return stripe_product['id']


def create_stripe_price(product, id_product):
    """Функция создания цены в Stripe."""

    return stripe.Price.create(
        currency='rub',
        unit_amount=int(product.payment_amount * 100),
        product=id_product,
    )


def create_stripe_session(price):
    """Функция создания сессии платежа в Stripe."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")