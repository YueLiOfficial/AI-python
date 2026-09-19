from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calculate")

@mcp.tool(description="计算两个数字的和")
def add(a: int | float, b: int | float) -> int | float:
    return a + b

@mcp.tool(description="计算两个数字的乘积")
def mul(a: int | float, b: int | float) -> int | float:
    return a * b

if __name__ == "__main__":
    mcp.run(transport="streamable-http")