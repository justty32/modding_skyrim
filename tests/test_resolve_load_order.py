import tempfile
import unittest
from pathlib import Path

from scripts import resolve_load_order


class ResolveLoadOrderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.mo2 = self.root / "mo2"
        self.profile = self.mo2 / "profiles" / "Modpack-KR"
        self.data = self.root / "Data"
        self.profile.mkdir(parents=True)
        self.data.mkdir()

    def tearDown(self):
        self.temporary.cleanup()

    def write_profile(self, *, order: list[str], plugins: list[str], mods: list[str]):
        (self.profile / "loadorder.txt").write_text("\n".join(order) + "\n")
        (self.profile / "plugins.txt").write_text("\n".join(plugins) + "\n")
        (self.profile / "modlist.txt").write_text("\n".join(mods) + "\n")

    @staticmethod
    def provide(path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def test_overwrite_wins_named_mod_and_game_data(self):
        self.write_profile(
            order=["Skyrim.esm", "Shared.esp"],
            plugins=["*Shared.esp"],
            mods=["+High", "+Low"],
        )
        self.provide(self.data / "Skyrim.esm", "game master")
        self.provide(self.data / "Shared.esp", "game")
        self.provide(self.mo2 / "mods" / "Low" / "Shared.esp", "low")
        self.provide(self.mo2 / "mods" / "High" / "Shared.esp", "high")
        self.provide(self.mo2 / "overwrite" / "Shared.esp", "overwrite")

        resolved, missing, order_count, enabled_count = resolve_load_order.resolve(
            self.profile, self.mo2, self.data
        )

        self.assertEqual([name for name, unused in resolved], ["Skyrim.esm", "Shared.esp"])
        self.assertEqual(resolved[1][1], self.mo2 / "overwrite" / "Shared.esp")
        self.assertEqual(missing, [])
        self.assertEqual((order_count, enabled_count), (2, 2))

    def test_named_mod_priority_precedes_game_data_without_overwrite(self):
        self.write_profile(order=["Shared.esp"], plugins=["*Shared.esp"], mods=["+High", "+Low"])
        self.provide(self.data / "Shared.esp", "game")
        self.provide(self.mo2 / "mods" / "Low" / "Shared.esp", "low")
        self.provide(self.mo2 / "mods" / "High" / "Shared.esp", "high")

        resolved, missing, unused_order, unused_enabled = resolve_load_order.resolve(
            self.profile, self.mo2, self.data
        )

        self.assertEqual(resolved, [("Shared.esp", self.mo2 / "mods" / "High" / "Shared.esp")])
        self.assertEqual(missing, [])

    def test_disabled_plugin_is_omitted_and_missing_enabled_plugin_is_reported(self):
        self.write_profile(
            order=["Disabled.esp", "Missing.esl"],
            plugins=["Disabled.esp"],
            mods=[],
        )

        resolved, missing, order_count, enabled_count = resolve_load_order.resolve(
            self.profile, self.mo2, self.data
        )

        self.assertEqual(resolved, [])
        self.assertEqual(missing, ["Missing.esl"])
        self.assertEqual((order_count, enabled_count), (2, 1))


if __name__ == "__main__":
    unittest.main()
