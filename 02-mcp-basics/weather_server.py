"""MCP SERVER minh hoạ — công bố tool `get_weather` qua giao thức MCP.

Khác với function calling: tool nằm ở một server ĐỘC LẬP. Server tự "khai
báo" tool của mình; bất kỳ MCP client nào (Claude Code, Claude Desktop,
Cursor, hoặc weather_client.py) cũng cắm vào dùng được mà không cần biết
code bên trong.

Schema của tool được TỰ ĐỘNG sinh ra từ type hints + docstring.

Chạy trực tiếp:
    pip install -r ../requirements.txt
    python weather_server.py

Đăng ký với Claude Code (làm 1 lần, dùng mãi):
    claude mcp add weather -- python /đường/dẫn/tới/weather_server.py
"""

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("weather")

_MOCK_DB = {
    "Hanoi": "29°C, trời mưa",
    "Haiphong": "33°C, mưa rào",
    "Danang": "30°C, nhiều mây",
}

_MOCK_FORECAST = {
    "Hanoi": ["29°C, trời mưa", "30°C, nhiều mây", "31°C, có nắng"],
    "Haiphong": ["33°C, mưa rào", "32°C, nhiều mây", "31°C, trời mưa"],
    "Danang": ["30°C, nhiều mây", "31°C, có nắng", "32°C, nắng nhẹ"],
}


@mcp.tool()
def get_weather(city: str) -> str:
    """Lấy thời tiết hiện tại của một thành phố."""
    return f"{city}: {_MOCK_DB.get(city, '28°C, không có dữ liệu chi tiết')}"


@mcp.tool()
def get_forecast(city: str, days: int = 2) -> str:
    """Dự báo thời tiết N ngày tới cho một thành phố.

    Args:
        city: Tên thành phố (Hanoi, Danang, Haiphong).
        days: Số ngày dự báo, từ 1 đến 3 (mặc định 2).
    """
    if not 1 <= days <= 3:
        return "Số ngày dự báo phải nằm trong khoảng từ 1 đến 3."

    forecasts = _MOCK_FORECAST.get(
        city,
        ["28°C, không có dữ liệu chi tiết"] * 3,
    )
    details = "\n".join(
        f"Ngày {day}: {weather}"
        for day, weather in enumerate(forecasts[:days], start=1)
    )
    return f"Dự báo {city} trong {days} ngày:\n{details}"


if __name__ == "__main__":
    mcp.run()  # mặc định chạy qua stdio
