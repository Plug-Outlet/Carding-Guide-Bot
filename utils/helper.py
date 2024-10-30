# utils/helpers.py

from datetime import datetime
import re

def format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Format a timestamp into a readable string.
    
    :param timestamp: A datetime object or a string that can be parsed into a datetime
    :param format_str: The desired output format (default: YYYY-MM-DD HH:MM:SS)
    :return: Formatted timestamp string
    """
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    return timestamp.strftime(format_str)

def validate_card_number(card_number):
    """
    Validate a credit card number using the Luhn algorithm.
    
    :param card_number: The card number to validate
    :return: True if valid, False otherwise
    """
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10 == 0

def mask_card_number(card_number):
    """
    Mask a credit card number, showing only the last 4 digits.
    
    :param card_number: The full card number
    :return: Masked card number string
    """
    return "X" * (len(card_number) - 4) + card_number[-4:]

def parse_card_info(card_string):
    """
    Parse a card string in the format XXXXXXXXXXXXXXXX|MM|YY|CVV.
    
    :param card_string: The card information string
    :return: A dictionary with parsed information or None if invalid format
    """
    parts = card_string.split("|")
    if len(parts) != 4:
        return None
    
    card_number, month, year, cvv = parts
    if not (card_number.isdigit() and month.isdigit() and year.isdigit() and cvv.isdigit()):
        return None
    
    return {
        "card_number": card_number,
        "expiry_month": month,
        "expiry_year": year,
        "cvv": cvv
    }

def is_valid_bin(bin_number):
    """
    Check if a BIN (Bank Identification Number) is valid.
    
    :param bin_number: The BIN to check
    :return: True if valid, False otherwise
    """
    return bool(re.match(r"^\d{6}$", bin_number))

def format_currency(amount, currency="USD"):
    """
    Format a currency amount.
    
    :param amount: The amount to format
    :param currency: The currency code (default: USD)
    :return: Formatted currency string
    """
    return f"{amount:.2f} {currency}"

def truncate_text(text, max_length=100, ellipsis="..."):
    """
    Truncate text to a maximum length.
    
    :param text: The text to truncate
    :param max_length: Maximum length of the truncated text
    :param ellipsis: String to append if text is truncated
    :return: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(ellipsis)] + ellipsis

# Add more utility functions as needed