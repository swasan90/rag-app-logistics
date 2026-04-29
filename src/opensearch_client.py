from opensearchpy import OpenSearch
from .config import OPENSEARCH_HOST, OPENSEARCH_PORT, OPENSEARCH_USER, OPENSEARCH_PASSWORD

def get_opensearch_client() -> OpenSearch:
    host_value = (OPENSEARCH_HOST).strip()
    use_ssl = host_value.startswith("https://")
    host_value = host_value.replace("http://", "").replace("https://", "")

    return OpenSearch(
        hosts=[{"host": host_value, "port": int(OPENSEARCH_PORT), "scheme": "https" if use_ssl else "http"}],
        http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
        use_ssl=use_ssl,
        verify_certs=False,
        ssl_show_warn=False
    )


