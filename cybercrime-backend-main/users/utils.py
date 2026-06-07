import coolname
import pyotp
from mnemonic import Mnemonic

from backend.settings import APPLICATION_NAME
from users.selectors import username_exists


def initialize_account(username=None):
    """
    Generate a new OTP secret and provisioning URI for user setup.
    """
    totp_secret = pyotp.random_base32()
    username = username or generate_unique_username()
    otp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name=username, issuer_name=APPLICATION_NAME)
    return totp_secret, username, otp_uri

def generate_username():
    return coolname.generate_slug(2)

def generate_unique_username():
    while True:
        username = generate_username()
        if not username_exists(username): return username

def generate_recovery_phrase(num_words=12):
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128 if num_words == 12 else 256)
        
def verify_code(totp_secret, code):
    """
    Verify a TOTP secret using the provided code.
    """
    return pyotp.TOTP(totp_secret).verify(code)