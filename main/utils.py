import hmac
import hashlib
from typing import Optional
import json

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from decouple import config


def generate_address(account_index) -> str:

    MNEMONIC = config('MNEMONIC')

    # Initialize Ethereum mainnet BIP44HDWallet
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)

    # Get Ethereum BIP44HDWallet from mnemonic
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english"
    )

    # Clean default BIP44 derivation indexes/paths
    bip44_hdwallet.clean_derivation()

    # Derivation from Ethereum BIP44 derivation path
    bip44_derivation: BIP44Derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=account_index
    )
    # Drive Ethereum BIP44HDWallet
    bip44_hdwallet.from_path(path=bip44_derivation)

    return bip44_hdwallet.address()


def signature_generator(user_id, reference, amount_in_kobo) -> str:
    destination_account_number = config("DESTINATION_ACCOUNT_NUMBER")
    destination_bank_code = config("DESTINATION_BANK_CODE")

    payload = f"{user_id}:{reference}:{amount_in_kobo}:{destination_account_number}:{destination_bank_code}"
    sendcash_signature_token = config("SENDCASH_SIGNATURE_TOKEN")

    sendcash_signature_token_in_byte = bytes(sendcash_signature_token, 'UTF-8')  # key.encode() would also work in this case
    payload_encoded = payload.encode()
    
    h = hmac.new(sendcash_signature_token_in_byte, payload_encoded, hashlib.sha256)
    return h.hexdigest()


def compare_hashes(request):

    body = request.POST
    json_body = json.dumps(body)

    sendcash_signature_token = config("SENDCASH_SIGNATURE_TOKEN")
    transfer_signature = request.headers.get('X-Transfers-Signature')

    sendcash_signature_token_in_byte = bytes(sendcash_signature_token, 'UTF-8')
    json_body_encoded = json_body.encode()

    h = hmac.new(sendcash_signature_token_in_byte, json_body_encoded, hashlib.sha256)

    return transfer_signature == h.hexdigest()

