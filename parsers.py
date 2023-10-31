from model import Header, Feedback, Stats


def parse_header(header_lines):
    if len(header_lines) > 1:
        return Header(
            header_lines[1],
            header_lines[2] if len(header_lines) > 2 else "",
            header_lines[3] if len(header_lines) > 3 else "",
        )

    return Header("", "", "")


def parse_feedback(feedback_lines):
    if len(feedback_lines) > 6:
        return Feedback(
            feedback_lines[1], feedback_lines[2], feedback_lines[4], feedback_lines[6]
        )
    return Feedback("", "", "", "")


def parse_stats(stats_lines):
    stats_data = {
        "all_trades": "",
        "buy_sell_ratio": "",
        "buy": "",
        "sell": "",
        "30d_trades": "",
        "30d_completion_rate": "",
        "avg_release_time": "",
        "avg_pay_time": "",
    }

    buy = ""
    sell = ""
    ratio = "Error"
    for i, line in enumerate(stats_lines):
        if "All Trades" in line:
            stats_data["all_trades"] = stats_lines[i + 1]
        elif "Buy" in line and "Sell" in line:
            buy_sell_parts = line.split("/")
            buy = int(buy_sell_parts[0].split(" ")[1].strip())
            sell = int(buy_sell_parts[1].split(" ")[1].strip())
            stats_data["buy"] = buy
            stats_data["sell"] = sell
        elif "Buy" in line:
            buy = int(line.split(" ")[1].strip())
            stats_data["buy"] = buy
        elif "Sell" in line:
            sell = int(line.split(" ")[1].strip())
            stats_data["sell"] = sell
        elif "30d Trades" in line:
            stats_data["30d_trades"] = stats_lines[i + 1]
        elif "30d Completion Rate" in line:
            stats_data["30d_completion_rate"] = stats_lines[i + 1] + " %"
        elif "Avg. Release Time" in line:
            stats_data["avg_release_time"] = stats_lines[i + 1] + " Minute(s)"
        elif "Avg. Pay Time" in line:
            stats_data["avg_pay_time"] = stats_lines[i + 1] + " Minute(s)"

    if buy and sell:
        ratio = round(buy / sell, 2)
    stats_data["buy_sell_ratio"] = ratio

    return Stats(
        stats_data["all_trades"],
        stats_data["buy_sell_ratio"],
        stats_data["buy"],
        stats_data["sell"],
        stats_data["30d_trades"],
        stats_data["30d_completion_rate"],
        stats_data["avg_release_time"],
        stats_data["avg_pay_time"],
    )
