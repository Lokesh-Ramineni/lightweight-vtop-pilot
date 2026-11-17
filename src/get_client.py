import ssl
import httpx
import logging
from enpoints import VTOP_BASE_URL,HEADERS


logger = logging.getLogger(__name__)

sectigo_public="""-----BEGIN CERTIFICATE-----
MIIGkTCCBPmgAwIBAgIQaelsdz55zFOaa2BmSVZ37zANBgkqhkiG9w0BAQsFADBg
MQswCQYDVQQGEwJHQjEYMBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTcwNQYDVQQD
Ey5TZWN0aWdvIFB1YmxpYyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gQ0EgRFYgUjM2
MB4XDTI2MTAzMDAwMDAwMFoXDTI3MDUxNjIzNTk1OVowGDEWMBQGA1UEAwwNKi52
aXRhcC5hYy5pbjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAK03FQKx
BF0zIGJ2U+P8kyNgIqQOBYAFh9oNy2iZUECbbSSAELQyZFleb6OoHWnZ/lI9ChX/
0eZMYBQEDnthHP2MvzR/8q8nSHBpfrLnFmO1aqPFm08xvYX5I9b9FY5wn53IaJAB
DheoBFQ+7gNtvE8mPxjV2LaR4HhaJUJ9iEuOH4BiU2xbOcCJaCdCwwkPGritmApL
/Q4D7Cl/hUBdTDxIJK4ku+SFKGbObc6WdGXR5FSqGnpdmUl6Rp/KFOkN//3qe7q3
2W4LrsMDXnfx0StrKxXdlw/te2IPLexzmY8HAnLpUQopPqNQeTF5mf/7/6FNtmdH
qG3B/655l/QmcMUCAwEAAaOCAw0wggMJMB8GA1UdIwQYMBaAFGjAEhYYDq/O9oem
MlejRlFdywcnMB0GA1UdDgQWBBTWuXt1qAGstQByYA/y3UDvjjrhOTAOBgNVHQ8B
Af8EBAMCBaAwDAYDVR0TAQH/BAIwADAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYB
BQUHAwIwSQYDVR0gBEIwQDA0BgsrBgEEAbIxAQICBzAlMCMGCCsGAQUFBwIBFhdo
dHRwczovL3NlY3RpZ28uY29tL0NQUzAIBgZngQwBAgEwgYQGCCsGAQUFBwEBBHgw
djBPBggrBgEFBQcwAoZDaHR0cDovL2NydC5zZWN0aWdvLmNvbS9TZWN0aWdvUHVi
bGljU2VydmVyQXV0aGVudGljYXRpb25DQURWUjM2LmNydDAjBggrBgEFBQcwAYYX
aHR0cDovL29jc3Auc2VjdGlnby5jb20wJQYDVR0RBB4wHIINKi52aXRhcC5hYy5p
boILdml0YXAuYWMuaW4wggGPBgorBgEEAdZ5AgQCBIIBfwSCAXsBeQB+AFlubDOG
lLJZcqJWyKDo3ZBKdugIPdqHOwEIOCgUPO5ZAAABoYsa75kACAAABQAYCDHrBAMA
RzBFAiEAz2gv0FHCNljvVg1wGmPeqw9DRICWBG+O77omTc7Orc0CIGGguUujJuoh
bigvtfRnsNJc8IsUejaM3YBj0GTCkeQNAHcA1tWNqdAXU/NqSqDHV0kCr+vH3CzT
jNn3ZMgMiRkenwIAAAGhixrv0QAABAMASDBGAiEAg6i+PhtHYjKJqBmvqZI1kl5B
Sl10ztJ+CtrgarC2jjUCIQCzT8R5k0f0E+o0oPf2tdgUnYtFhASlri/BDm68H5Uw
VgB+ABqLnWuN15HRzQVJ7bYDVdYGtk+tMNtx/niPD8fI+8SxAAABoYsa840ACAAA
BQAP5jjuBAMARzBFAiEAzEORemWe2vnsSDy0rwkMa/s8bo5UN/PwPVcqzr4HcwAC
IDS5oFgEUX3W5fG/SM82k1U97pQG8edKFCY8G7FqXXeqMA0GCSqGSIb3DQEBCwUA
A4IBgQAO7B2RUrk8GjyK4MvG4xV94/KH3TqJcdeR6xtQJI8KYfT1wP2+PVG8NWxn
CpJTtUZUOvUE7kfb4e4cpjooH+Qs4UEClSkXRI1nP+/6DwG4NheIkwb1lnEyJbUd
knKKGEcXX0z2EIhBzZV41MhzwBJuzfsX+5XCn77foF6NEa/85hr1ePm3533d1a91
4yYe8XzZvjKECnu29AKt6uvZ65KRKicHn5I4K037vMYdPyloPGyPHJZPhblarj6N
MWbQdkajmq0fCDjZPpiH+xeAF17dilee5qwxwkhZJ+RjxPap071c0XDpvvz3uufB
flhij7rFwR7uH3TwVgGLfw+pqqPXXTTQctx51d6GgqWmv1PcbJyq3EngWZshaGF9
Tvsgd04IZnjjBdJvpWyCynVC8R2ugQf5UONY92zqjY8Mj3IEKT62mAJMKTdQ/KPf
Ojn58Zf/wJKQ3LiavtjfogbiQB87UX+Zj3duwcosG8yE2LIrQH7jLrqyggPNZEkW
4PesFt4=
-----END CERTIFICATE-----
"""

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(cadata=sectigo_public)

async def get_client() -> httpx.AsyncClient:
    # Certificate verification is never disabled. A TLS failure must surface
    # as an error, not fall back to an unverified connection.
    return httpx.AsyncClient(
        base_url=VTOP_BASE_URL,
        headers=HEADERS,
        follow_redirects=True,
        verify=ssl_context,
        timeout=httpx.Timeout(
            connect=15.0,
            read=30.0,
            write=30.0,
            pool=30.0,
        ),
    )