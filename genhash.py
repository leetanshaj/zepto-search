import hashlib
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re


def to_slug(text: str) -> str:
    text = re.sub(r"[']", '', text.lower())  # remove apostrophes
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')

def generate_signature(request_config, secret=""):
    method = request_config.get("method", "GET").lower()
    url = request_config.get("url", "")
    base_url = request_config.get("baseURL", "")
    data = request_config.get("data")
    params = request_config.get("params", {})
    headers = request_config.get("headers", {})

    path, merged_params = extract_path_and_params(url, base_url, params)

    if method == "get":
        body = None
    else:
        if isinstance(data, str):
            body = data
        else:
            import json
            body = json.dumps(data) if data is not None else None

    payload = {
        "body": body if body is not None else "",
        "deviceId": headers.get("device_id", ""),
        "method": method,
        "requestId": headers.get("request_id", ""),
        "secret": secret,
        "url": format_url_with_params(path, merged_params)
    }

    # Build the signature string by sorted keys and pipe-separated values
    sorted_keys = sorted(payload.keys())
    # print("Sorted keys:", sorted_keys)  # Debugging output
    signature_string = "|".join(payload[k] for k in sorted_keys)

    # Generate SHA-256 hex digest
    # print(signature_string)  # Debugging output
    return hashlib.sha256(signature_string.encode("utf-8")).hexdigest()

def extract_path_and_params(url, base_url, config_params):
    # Combine base URL and url path
    parsed_base = urlparse(base_url)
    parsed_url = urlparse(url, scheme=parsed_base.scheme, allow_fragments=True)

    # Combine paths
    path = parsed_url.path or parsed_base.path

    # Parse query params from base_url and url
    base_query = parse_qs(parsed_base.query)
    url_query = parse_qs(parsed_url.query)

    # Merge all query params and the config_params argument
    merged = {}
    for d in [base_query, url_query, config_params]:
        for k, v in d.items():
            # Ensure all values are lists (parse_qs returns lists)
            if isinstance(v, list):
                merged.setdefault(k, []).extend(v)
            else:
                merged.setdefault(k, []).append(v)

    # Flatten lists to last value for simplicity (like URLSearchParams)
    flattened = {k: v[-1] for k, v in merged.items()}

    return path, flattened

def format_url_with_params(path, params):
    if not params:
        return path
    return f"{path}?{urlencode(params)}"

# Example usage
if __name__ == "__main__":
    config = {
        "method": "post",
        "url": "/api/v3/search",
        "baseURL": "https://api.zepto.com/api/",
        "data": '{"query":"chips","pageNumber":0,"mode":"TYPED","intentId":"b992798b-e870-4608-877f-a45ab299ca1c"}',
        "headers": {"request_id": "0662313d-ff24-49aa-87a8-b454bf28a1b8", "device_id": "360b43af-299b-4303-b1c6-324c353d8936"}
    }
    secret = "IEmu_lwtEPSLQAEujbjLc:tnnrGHHirI95GLKgUPNXlGF86v8.vQEiyi5RkpGJ+WakMx43VCK9Z8cj5KnJN2v0iFHx7QA"

    signature = generate_signature(config, secret)
    print("Signature:", signature)



# '{"query":"cheese","pageNumber":0,"mode":"TYPED","intentId":"c662b9fe-5caf-4108-b212-41769ae523b4"}|360b43af-299b-4303-b1c6-324c353d8936|post|f9e8d4f1-cc53-4d94-ad35-f8297597c333|IEmu_lwtEPSLQAEujbjLc:tnnrGHHirI95GLKgUPNXlGF86v8.vQEiyi5RkpGJ+WakMx43VCK9Z8cj5KnJN2v0iFHx7QA|/api/v3/search'