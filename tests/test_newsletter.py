import importlib.util
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


gmail = load("gmail", ROOT / "botbot-gmail/scripts/botbot_gmail.py")
newsletter = load("newsletter", ROOT / "meagent-tldr-newsletter/scripts/meagent_tldr_newsletter.py")


class GmailBodyTest(unittest.TestCase):
    def test_html_entities_remain_text(self):
        parser = gmail._TagStripper()
        parser.feed("<p>Use &lt;strong&gt; literally</p>")
        self.assertIn("Use <strong> literally", parser.text())

    def test_inline_link_includes_destination(self):
        parser = gmail._TagStripper()
        parser.feed('<p><a href="https://example.com?a=1&amp;b=2">Read</a></p>')
        self.assertIn("Read (https://example.com?a=1&b=2)", parser.text())


class NewsletterParserTest(unittest.TestCase):
    def test_tldr_article_markers(self):
        body = """Story title (5 minute read)
(https://story.example/?utm_source=x)
Story description

Project title (GitHub Repo)
(https://github.com/example/project)
Project description
"""
        self.assertEqual(
            newsletter._parse_tldr(body),
            [
                ("Story title (5 minute read)", "Story description", "https://story.example/?utm_source=x"),
                ("Project title (GitHub Repo)", "Project description", "https://github.com/example/project"),
            ],
        )

    def test_ai_secret_read_more_format(self):
        body = """AI title
(https://ai.example/)
TL;DR: AI description Read more -> (https://ai.example/)
"""
        self.assertEqual(
            newsletter._parse_aisecret(body),
            [("AI title", "TL;DR: AI description", "https://ai.example/")],
        )

    def test_legacy_formats_remain_supported(self):
        body = """TITLE [1]

Old description

DATA
AI title
https://ai.example/
AI description

Links:
[1] https://old.example/?utm_source=x
"""
        self.assertEqual(
            newsletter._parse_tldr(body),
            [("TITLE [1]", "Old description", "https://old.example/?utm_source=x")],
        )


    def test_ai_section_does_not_cross_boundary(self):
        body = """DATA breach report
https://false.example/
Should not parse

DATA
Missing link
No URL here

GROK
Found link
https://grok.example/
Grok description

Unsubscribe
footer text
"""
        self.assertEqual(
            newsletter._parse_aisecret(body),
            [("Found link", "Grok description", "https://grok.example/")],
        )


class NewsletterDispatchTest(unittest.TestCase):
    def test_dispatches_by_sender_without_reading_unknown_rows(self):
        rows = [
            {"threadid": "tldr", "from": "dan@tldrnewsletter.com", "tstamp": "2026-01-03T00:00:00"},
            {"threadid": "ai", "reply_to": "leo@aisecret.us", "tstamp": "2026-01-02T00:00:00"},
            {"threadid": "other", "from": "other@example.com", "tstamp": "2026-01-01T00:00:00"},
        ]
        output = "\n".join(__import__("json").dumps(row) for row in rows)
        bodies = {"tldr": "tldr body", "ai": "ai body"}

        def run(cmd):
            return output if cmd[-2] == "ls" else bodies[cmd[-1]]

        with patch.object(newsletter, "_run", side_effect=run), \
             patch.object(newsletter, "_parse_tldr", return_value=[]) as parse_tldr, \
             patch.object(newsletter, "_parse_aisecret", return_value=[]) as parse_ai, \
             patch.object(newsletter, "PENDING_PATH", MagicMock()):
            newsletter.cmd_read(MagicMock())

        parse_tldr.assert_called_once_with("tldr body")
        parse_ai.assert_called_once_with("ai body")


if __name__ == "__main__":
    unittest.main()
