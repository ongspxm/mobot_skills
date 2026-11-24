import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import meagent_tldr_newsletter as newsletter


class ParseAisecretTests(unittest.TestCase):
    def test_parses_new_headline_and_inline_link_format(self) -> None:
        body = """United Bans Meta Muse

United Bans Meta Muse (https://aisecret.us/r/story)

By Magna & Ben

Good Morning, AI Enthusiasts!

United Bans Meta Muse

Photo: ChromeGames

United Airlines will stop personal AI agents (https://aisecret.us/r/citation) from booking its flights, the first US carrier to say so.
"""

        self.assertEqual(
            newsletter._parse_aisecret(body),
            [(
                "United Bans Meta Muse",
                "United Airlines will stop personal AI agents from booking its flights, the first US carrier to say so.",
                "https://aisecret.us/r/story",
            )],
        )


    def test_uses_preheader_for_long_form_issue(self) -> None:
        body = """World Model is A Waiting Room

https://aisecret.us/ Welcome back, AI Enthusiasts! $2.3B went into world models this year.

World Model is A Waiting Room (https://aisecret.us/r/story)
"""

        self.assertEqual(
            newsletter._parse_aisecret(body),
            [(
                "World Model is A Waiting Room",
                "Welcome back, AI Enthusiasts! $2.3B went into world models this year.",
                "https://aisecret.us/r/story",
            )],
        )


    def test_skips_short_image_caption_for_lead(self) -> None:
        body = """Huang Admits Affair With Suspected Spy

Huang Admits Affair With Suspected Spy (https://aisecret.us/r/story)

Huang Admits Affair With Suspected Spy

Jensen & Alice

Jensen Huang told Nvidia staff Sunday he had cheated on his wife (https://aisecret.us/r/citation), confirming reports of an affair.
"""

        self.assertEqual(
            newsletter._parse_aisecret(body),
            [(
                "Huang Admits Affair With Suspected Spy",
                "Jensen Huang told Nvidia staff Sunday he had cheated on his wife, confirming reports of an affair.",
                "https://aisecret.us/r/story",
            )],
        )


if __name__ == "__main__":
    unittest.main()
