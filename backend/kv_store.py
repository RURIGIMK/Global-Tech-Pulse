import os
import json
from vercel_kv import KV

# Fallback to file-based storage if Vercel KV environment is missing
USE_VERCEL_KV = all(k in os.environ for k in ["KV_REST_API_URL", "KV_REST_API_TOKEN"])

if USE_VERCEL_KV:
    kv = KV()
else:
    print("⚠️  Vercel KV not configured. Using local JSON file for storage.")
    class FakeKV:
        def __init__(self):
            self.file = "local_data.json"
            self._data = {}
            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    self._data = json.load(f)

        async def get(self, key):
            return self._data.get(key)

        async def set(self, key, value):
            self._data[key] = value
            with open(self.file, "w") as f:
                json.dump(self._data, f)

        async def setex(self, key, ttl, value):
            await self.set(key, value)  # TTL not implemented in fallback

    kv = FakeKV()
