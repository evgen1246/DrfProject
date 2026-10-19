import stripe


class StripeService:
    """Сервис для работы с Stripe API"""

    @staticmethod
    def create_product(name: str, description: str = None) -> dict:
        """Создание продукта в Stripe"""
        try:
            product = stripe.Product.create(
                name=name,
                description=description or "",
                active=True,
            )
            return {"success": True, "product_id": product.id, "product": product}
        except stripe.error.StripeError as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def create_price(product_id: str, amount: int, currency: str = "usd") -> dict:
        """Создание цены для продукта"""
        try:
            price = stripe.Price.create(
                product=product_id,
                unit_amount=amount,
                currency=currency,
            )
            return {"success": True, "price_id": price.id, "price": price}
        except stripe.error.StripeError as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def create_checkout_session(
        price_id: str, success_url: str, cancel_url: str
    ) -> dict:
        """Создание сессии для оплаты"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return {"success": True, "session_id": session.id, "url": session.url}
        except stripe.error.StripeError as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def create_payment_intent(amount: int, currency: str = "usd") -> dict:
        """Создание PaymentIntent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=["card"],
            )
            return {
                "success": True,
                "client_secret": intent.client_secret,
                "intent_id": intent.id,
            }
        except stripe.error.StripeError as e:
            return {"success": False, "error": str(e)}
