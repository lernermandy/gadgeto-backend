import uuid
import httpx
from ..core.config import settings

class CashfreeService:
    def create_session(self, order_id: int, amount: float):
        reference = str(uuid.uuid4())
        pa = settings.UPI_VPA
        pn = settings.UPI_NAME
        upi_link = (
            f"upi://pay?pa={pa}&pn={pn}&am={amount:.2f}&cu=INR&tn=Order%20{order_id}&tr={reference}"
        )
        return {"status": "created", "session_id": reference, "amount": amount, "upi_link": upi_link, "reference_id": reference}

    def verify_payment(self, reference_id: str):
        return {"status": "paid"}
