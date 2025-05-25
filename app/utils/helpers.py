import markdown
from markupsafe import Markup
from datetime import datetime, timezone
from dateutil import parser


def markdown_to_html(text):
    return Markup(markdown.markdown(text, extensions=["fenced_code", "tables"]))


def format_datetime(value, format="%b %d, %Y @ %I:%M%p"):
    """Format an ISO datetime string to a readable format."""
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime(format)
    except Exception as e:
        return value  # fallback to original if there's an error


def time_ago(value):
    try:
        dt = parser.isoparse(value)
        now = datetime.now(timezone.utc)
        diff = now - dt
        seconds = int(diff.total_seconds())
        abs_seconds = abs(seconds)

        def plural(unit, value): return f"{value} {unit}{'' if value == 1 else 's'}"

        if abs_seconds < 60:
            return "just now" if seconds >= 0 else "in a few seconds"
        elif abs_seconds < 3600:
            minutes = abs_seconds // 60
            return f"{plural('minute', minutes)} ago" if seconds >= 0 else f"in {plural('minute', minutes)}"
        elif abs_seconds < 86400:
            hours = abs_seconds // 3600
            return f"{plural('hour', hours)} ago" if seconds >= 0 else f"in {plural('hour', hours)}"
        elif abs_seconds < 604800:
            days = abs_seconds // 86400
            return f"{plural('day', days)} ago" if seconds >= 0 else f"in {plural('day', days)}"
        elif abs_seconds < 2592000:
            weeks = abs_seconds // 604800
            return f"{plural('week', weeks)} ago" if seconds >= 0 else f"in {plural('week', weeks)}"
        elif abs_seconds < 15552000:
            months = abs_seconds // 2592000
            return f"{plural('month', months)} ago" if seconds >= 0 else f"in {plural('month', months)}"
        else:
            return dt.strftime("%b %d, %Y")

    except Exception as e:
        print(f"[time_ago] Failed to parse '{value}': {e}")
        return value


def icon_for_mime(mimetype):
    print('mime', mimetype)
    icon_map = {
        "application/pdf": "lni-file-format-pdf",
        "application/msword": "lni-file-format-doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "lni-file-format-doc",
        "application/vnd.ms-excel": "lni-file-format-xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "lni-file-format-xls",
        "application/zip": "lni-file-zip-1",
        "audio/mpeg": "lni-file-audio",
        "video/mp4": "lni-file-video",
        "image/png": "lni-file-image",
        "image/jpeg": "lni-file-image",
        "text/plain": "lni-file-text",
        "application/json": "lni-file-code"
    }
    return icon_map.get(mimetype, "lni-file-download")  # default fallback
