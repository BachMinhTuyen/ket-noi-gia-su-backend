import hashlib
import hmac
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict

class VNPAY:
    def __init__(self, tmn_code: str, hash_secret: str, base_url: str):
        self.tmn_code = tmn_code
        self.hash_secret = hash_secret
        self.base_url = base_url

    def generate_payment_url(self, payment_id: str, amount: float, return_url: str, ip_address: str) -> str:
        """
        Create the full VNPAY payment URL with secure hash.
        """
        createDate = datetime.now()
        expireDate = createDate + timedelta(minutes=15)
        params = {
            "vnp_Version": "2.1.0",
            "vnp_Command": "pay",
            "vnp_TmnCode": self.tmn_code,
            "vnp_Amount": str(int(amount * 100)),  # VNPAY yêu cầu amount * 100
            "vnp_CurrCode": "VND",
            "vnp_TxnRef": str(payment_id),
            "vnp_OrderInfo": f"Thanh toan don hang {str(payment_id)}",
            "vnp_OrderType": "billpayment",
            "vnp_Locale": "vn",
            "vnp_ReturnUrl": return_url,
            "vnp_IpAddr": ip_address,
            "vnp_CreateDate": createDate.strftime("%Y%m%d%H%M%S"),
            "vnp_ExpireDate": expireDate.strftime("%Y%m%d%H%M%S"),
        }

        sorted_params = sorted(params.items())
        print('---------------------')
        print(sorted_params)
        print('---------------------')
        hash_data = '&'.join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params)

        secure_hash = self._generate_secure_hash(self, hash_data)
        params["vnp_SecureHash"] = secure_hash
        params["vnp_SecureHashType"] = "SHA512"
        print('---------------------')
        print("HashData:", hash_data)
        print("SecureHash:", secure_hash)
        print('---------------------')

        query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote_plus)
        
        return f"{self.base_url}?{query_string}"

    def validate_return_data(self, query_params: Dict[str, str]) -> bool:
        """
        Validate VNPAY return query parameters with hash.
        """
        params = query_params.copy()
        received_hash = params.pop("vnp_SecureHash", None)
        params.pop("vnp_SecureHashType", None)

        sorted_params = sorted(params.items())
        query_string = "&".join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params])

        expected_hash = self._generate_secure_hash(self, query_string)
        return expected_hash == received_hash
    
    @staticmethod
    def _generate_secure_hash(self, data: str) -> str:
        """
        Internal method to generate SHA512 hash with secret key.
        """
        byte_key = self.hash_secret.encode('utf-8')
        byte_data = data.encode('utf-8')
        return hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()
