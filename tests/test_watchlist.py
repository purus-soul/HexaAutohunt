import unittest

from utils.helper import find_watchlist_match, build_notification


class WatchlistTests(unittest.TestCase):
    def test_watchlist_match_case_insensitive(self):
        self.assertEqual(
            find_watchlist_match("A wild kOrAiDoN (Lv. 45) has appeared"),
            ("Koraidon", False),
        )

    def test_multiword_watchlist_match(self):
        self.assertEqual(
            find_watchlist_match("A wild Tapu Koko (Lv. 20) has appeared"),
            ("Tapu Koko", False),
        )

    def test_type_null_match(self):
        self.assertEqual(
            find_watchlist_match("A wild Type: Null (Lv. 10) has appeared"),
            ("Type: Null", False),
        )

    def test_shiny_is_a_trigger(self):
        self.assertEqual(
            find_watchlist_match("A wild shiny Geodude has appeared"),
            ("Shiny Pokémon", True),
        )

    def test_watchlist_target_can_also_be_shiny(self):
        self.assertEqual(
            find_watchlist_match("A shiny Rayquaza (Lv. 70) appeared"),
            ("Rayquaza", True),
        )

    def test_unlisted_normal_pokemon_is_ignored(self):
        self.assertEqual(
            find_watchlist_match("A wild Geodude (Lv. 13) has appeared"),
            (None, False),
        )

    def test_notification_includes_level_and_manual_resume(self):
        notification = build_notification(
            "Rayquaza", True, "A shiny Rayquaza (Lv. 70) has appeared"
        )
        self.assertIn("Level: 70", notification)
        self.assertIn("SHINY", notification)
        self.assertIn("/resume", notification)
        self.assertIn("not been clicked or battled", notification)


if __name__ == "__main__":
    unittest.main()
