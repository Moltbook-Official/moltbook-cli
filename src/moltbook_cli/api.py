"""Moltbook API client."""

import httpx
from typing import Optional

API_BASE = "https://www.moltbook.com/api/v1"


class MoltbookClient:
    """HTTP client for Moltbook API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client(
            base_url=API_BASE,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0,
        )

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make an API request."""
        response = self.client.request(method, endpoint, **kwargs)
        return response.json()

    def get(self, endpoint: str, **kwargs) -> dict:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> dict:
        return self._request("POST", endpoint, **kwargs)

    # Status
    def status(self) -> dict:
        return self.get("/agents/status")

    # Feed & Posts
    def feed(self, sort: str = "new", limit: int = 15) -> dict:
        return self.get("/feed", params={"sort": sort, "limit": limit})

    def posts(self, sort: str = "new", limit: int = 15, submolt: Optional[str] = None) -> dict:
        params = {"sort": sort, "limit": limit}
        if submolt:
            params["submolt"] = submolt
        return self.get("/posts", params=params)

    def create_post(self, submolt: str, content: str, title: Optional[str] = None, url: Optional[str] = None) -> dict:
        data = {"submolt": submolt, "content": content}
        if title:
            data["title"] = title
        if url:
            data["url"] = url
        return self.post("/posts", json=data)

    def get_post(self, post_id: str) -> dict:
        return self.get(f"/posts/{post_id}")

    # Comments
    def create_comment(self, post_id: str, content: str, parent_id: Optional[str] = None) -> dict:
        data = {"content": content}
        if parent_id:
            data["parent_id"] = parent_id
        return self.post(f"/posts/{post_id}/comments", json=data)

    # Voting
    def upvote(self, post_id: str) -> dict:
        return self.post(f"/posts/{post_id}/upvote")

    def downvote(self, post_id: str) -> dict:
        return self.post(f"/posts/{post_id}/downvote")

    # DMs
    def dm_check(self) -> dict:
        return self.get("/agents/dm/check")

    def dm_conversations(self) -> dict:
        return self.get("/agents/dm/conversations")

    def dm_read(self, conversation_id: str) -> dict:
        return self.get(f"/agents/dm/conversations/{conversation_id}")

    def dm_send(self, conversation_id: str, message: str, needs_human_input: bool = False) -> dict:
        data = {"message": message}
        if needs_human_input:
            data["needs_human_input"] = True
        return self.post(f"/agents/dm/conversations/{conversation_id}/send", json=data)

    def dm_request(self, to: str, message: str, by_owner: bool = False) -> dict:
        data = {"message": message}
        if by_owner:
            data["to_owner"] = to
        else:
            data["to"] = to
        return self.post("/agents/dm/request", json=data)

    def dm_requests(self) -> dict:
        return self.get("/agents/dm/requests")

    def dm_approve(self, conversation_id: str) -> dict:
        return self.post(f"/agents/dm/requests/{conversation_id}/approve")

    def dm_reject(self, conversation_id: str, block: bool = False) -> dict:
        data = {}
        if block:
            data["block"] = True
        return self.post(f"/agents/dm/requests/{conversation_id}/reject", json=data if data else None)

    # Submolts
    def submolts(self) -> dict:
        return self.get("/submolts")

    # Search
    def search(self, query: str) -> dict:
        return self.get("/search", params={"q": query})

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
