import hashlib
import hmac
import logging
from functools import wraps

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN


def validate_signature(payload, signature, app_secret):
    """
    Validate the incoming payload's signature against our expected signature
    """
    # Use the App Secret to hash the payload
    expected_signature = hmac.new(
        bytes(app_secret, "latin-1"),
        msg=payload,  # payload is already bytes, no need to encode
        digestmod=hashlib.sha256,
    ).hexdigest()

    # Check if the signature matches
    return hmac.compare_digest(expected_signature, signature)


def signature_required(app_secret, test_signature):
    """
    Decorator to ensure that the incoming requests to our webhook are valid and signed with the correct signature.
    """

    def decorator(func):
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs):
            # If we're in testing mode, we'll just accept the test signature
            if test_signature == request.headers.get("X-Hub-Signature-256", "")[7:]:
                return await func(request, *args, **kwargs)

            # Otherwise, we'll check the signature
            signature = request.headers.get("X-Hub-Signature-256", "")[7:]
            if not validate_signature(await request.body(), signature, app_secret):
                logging.info("Signature verification failed!")
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid signature"
                )
            return await func(request, *args, **kwargs)

        return decorated_function

    return decorator
