#!/usr/bin/env python3
"""Test MCP client to verify server connectivity."""
import httpx
import asyncio

async def test_connection():
    """Test basic connection to the MCP server."""
    base_url = "http://localhost:8003"

    print(f"Testing connection to {base_url}")

    async with httpx.AsyncClient() as client:
        # Test root endpoint
        print("\n1. Testing root endpoint...")
        response = await client.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        # Test SSE endpoint
        print("\n2. Testing SSE endpoint...")
        try:
            async with client.stream('GET', f"{base_url}/sse",
                                    headers={"Accept": "text/event-stream"},
                                    timeout=5.0) as response:
                print(f"   Status: {response.status_code}")
                print(f"   Headers: {dict(response.headers)}")

                # Read first few events
                print("   Reading events...")
                count = 0
                async for line in response.aiter_lines():
                    print(f"   Event: {line}")
                    count += 1
                    if count > 5:
                        break
        except httpx.TimeoutException:
            print("   Connection established but no events received (timeout)")
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
