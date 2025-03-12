from openibanlib import openiban


from openibanlib.exceptions import IBANFormatValidationException
# By trying to initialize an IBAN object
try:
    openiban.IBAN('DE89370400440532013000')
except IBANFormatValidationException:
        print("Invalid IBAN provided")
# Or using a static method
print(openiban.IBAN.format_validate('DE89370400440532013000'))

