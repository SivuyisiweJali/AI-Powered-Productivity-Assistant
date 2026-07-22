from graph_client import GraphClient

def test_headers():
    graph = GraphClient()
    headers = graph.headers()
    assert "Authorization" in headers
    assert "Content-Type" in headers
