import requests


def proxy_currency(environ, start_response):
    currency = environ.get("PATH_INFO")
    if currency is None:
        start_response("404 Not Found", [("Content-Type", "text/html")])
        return [bytes("Not found", "utf-8")]
    currency = currency[1:]
    response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}")
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        start_response("404 Not Found", [("Content-Type", "text/html")])
        return [bytes("Not found", "utf-8")]
    start_response("200 OK", [("Content-Type", "application/json")])
    return [bytes(str(response_json), "utf-8")]


# run: waitress-serve --listen=*:8000 src.m_6_t_7:proxy_currency
