import random
from fastmcp import FastMCP

mcp =FastMCP(name="ExampleMCP", version="1.0.0")

@mcp.tool
def roll_dice(sides: int = 1) -> list[int]:
    """Roll a dice with the given number of sides."""
    return [random.randint(1,6) for _ in range(sides)]
@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

if __name__ == "__main__":
    mcp.run()