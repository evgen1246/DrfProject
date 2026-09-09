import stripe
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from learnix.models import Course, Lesson

from .models import Payment
from .services import StripeService


class CreatePaymentView(APIView):
    """Создание оплаты для курса или урока"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        lesson_id = request.data.get("lesson_id")
        amount = request.data.get("amount")
        currency = request.data.get("currency", "usd")

        if not amount:
            return Response(
                {"error": "Сумма обязательна"}, status=status.HTTP_400_BAD_REQUEST
            )

        product_name = "Курс"
        product_id = None
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            product_name = course.title
            product_id = course.id
        elif lesson_id:
            lesson = get_object_or_404(Lesson, id=lesson_id)
            product_name = lesson.title
            product_id = lesson.id
        else:
            return Response(
                {"error": "Укажите course_id или lesson_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product_result = StripeService.create_product(
            name=f"{product_name} (ID: {product_id})",
            description=f"Оплата за {product_name}",
        )

        if not product_result["success"]:
            return Response(
                {"error": product_result["error"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        amount_cents = int(float(amount) * 100)
        price_result = StripeService.create_price(
            product_id=product_result["product_id"],
            amount=amount_cents,
            currency=currency,
        )

        if not price_result["success"]:
            return Response(
                {"error": price_result["error"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Создаём сессию
        success_url = (
            request.build_absolute_uri(reverse("payments:payment_success"))
            + f"?session_id={{CHECKOUT_SESSION_ID}}"
        )
        cancel_url = request.build_absolute_uri(reverse("payments:payment_cancel"))

        session_result = StripeService.create_checkout_session(
            price_id=price_result["price_id"],
            success_url=success_url,
            cancel_url=cancel_url,
        )

        if not session_result["success"]:
            return Response(
                {"error": session_result["error"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        payment = Payment.objects.create(
            user=request.user,
            course_id=course_id if course_id else None,
            lesson_id=lesson_id if lesson_id else None,
            amount=amount,
            payment_method="stripe",
            stripe_session_id=session_result["session_id"],
            is_paid=False,
        )

        return Response(
            {
                "payment_id": payment.id,
                "session_id": session_result["session_id"],
                "payment_url": session_result["url"],
                "message": "Перейдите по ссылке для оплаты",
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentSuccessView(APIView):
    """Обработка успешной оплаты"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        session_id = request.GET.get("session_id")

        if not session_id:
            return Response(
                {"error": "session_id не передан"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session = stripe.checkout.Session.retrieve(session_id)

            if session.payment_status == "paid":
                payment = Payment.objects.get(
                    stripe_session_id=session_id, user=request.user
                )
                payment.is_paid = True
                payment.stripe_payment_intent_id = session.payment_intent
                payment.save()

                return Response(
                    {"message": "Оплата прошла успешно!", "payment_id": payment.id}
                )

            return Response(
                {"error": "Платёж не был завершён"}, status=status.HTTP_400_BAD_REQUEST
            )

        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Payment.DoesNotExist:
            return Response(
                {"error": "Платёж не найден"}, status=status.HTTP_404_NOT_FOUND
            )


class PaymentCancelView(APIView):
    """Обработка отмены оплаты"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Оплата была отменена"})
