import trio
import httpx
from holehe.core import *
from holehe.modules import *

async def main():
    email = "subhadip.sec@gmail.com"
    out = []
    
    # modules is a list of functions from holehe.modules
    # let's just import a few common ones or import all
    
    # Let's see what holehe.modules contains
    import holehe.modules
    all_modules = [getattr(holehe.modules, m) for m in dir(holehe.modules) if callable(getattr(holehe.modules, m)) and not m.startswith("__")]
    print(f"Loaded {len(all_modules)} modules")
    
    # We will run just a few modules to test
    client = httpx.AsyncClient()
    for module in all_modules[:5]:
        print(f"Running {module.__name__}...")
        try:
            await module(email, client, out)
        except Exception as e:
            print(e)
            
    await client.aclose()
    print("Results:")
    for res in out:
        if res.get("exists"):
            print(f"FOUND: {res['name']}")

if __name__ == "__main__":
    trio.run(main)
