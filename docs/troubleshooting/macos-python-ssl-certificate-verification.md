# SSL Certificate Verification Failure on macOS

## Summary

Requests to the KRX OpenAPI failed during the TLS handshake when Atlas was run
with Python 3.12 installed from python.org on macOS.

## Error

```text
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED]
certificate verify failed: unable to get local issuer certificate
```

The error was wrapped by `urllib` as:

```text
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] ...>
```

## Cause

The Python installation did not have a configured root CA certificate bundle.
As a result, Python's SSL context could not verify the KRX server certificate.

This occurred before the HTTP request was sent and was unrelated to the KRX
OpenAPI authentication key or response processing.

## Resolution

Run the certificate installation script bundled with the python.org macOS
installer:

```shell
"/Applications/Python 3.12/Install Certificates.command"
```

After installing the certificates, the KRX OpenAPI request completed
successfully.

## Verification

The number of certificates loaded by Python can be checked with:

```shell
python -c \
'import ssl; print(ssl.create_default_context().cert_store_stats())'
```

The `x509_ca` value should be greater than zero.

## Security Note

Do not work around this problem by disabling SSL certificate verification.
Install or configure a valid CA certificate bundle instead.
