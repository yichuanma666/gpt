import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
CORE_PATH = PROJECT_DIR / "codex56-orchestrator.py"
GUI_PATH = PROJECT_DIR / "codex56-control-center.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


core = load_module(CORE_PATH, "codex56_orchestrator_test")
gui = load_module(GUI_PATH, "codex56_control_center_test")


class CoreHelpersTests(unittest.TestCase):
    def test_normalize_md_name(self):
        self.assertEqual(core.normalize_md_name("rules"), "rules.md")
        self.assertEqual(core.normalize_md_name("rules.md"), "rules.md")
        for invalid in ("", "../rules", "a/b", "CON", "gpt5.5-unrestricted"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    core.normalize_md_name(invalid)

    def test_render_model_instructions_preserves_existing_config(self):
        content = "model = \"gpt-5\"\n\n[profiles]\nname = \"default\"\n"
        rendered, changed = core.render_model_instructions(content, "rules.md")
        self.assertTrue(changed)
        self.assertIn('model_instructions_file = "./rules.md"', rendered)
        self.assertIn('[profiles]', rendered)
        rendered_again, changed_again = core.render_model_instructions(rendered, "rules.md")
        self.assertFalse(changed_again)
        self.assertEqual(rendered_again, rendered)

    def test_doctor_accepts_a_minimal_codex_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "config.toml").write_text('model = "gpt-5"\n', encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(CORE_PATH),
                    "--doctor",
                    "--codex-dir",
                    directory,
                    "--lang",
                    "en",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("[Doctor]", result.stdout)
            self.assertIn("Structural health: healthy", result.stdout)


class GuiHelpersTests(unittest.TestCase):
    def test_classify_deployment_status(self):
        clean = "Transaction residue: none\ndeployment manifest: regular file\n"
        self.assertEqual(gui.classify_deployment_status(clean, 0), "deployed")
        blocked = "Transaction residue: none\nDeployability: blocked\n"
        self.assertEqual(gui.classify_deployment_status(blocked, 1), "blocked")
        recovery = "Transaction residue: .codex-keysmith-transaction-x\n"
        self.assertEqual(gui.classify_deployment_status(recovery, 0), "recovery")

    def test_format_command_quotes_paths(self):
        command = gui.format_command(["python", "script.py", "C:\\Folder With Space"])
        self.assertIn("Folder With Space", command)


if __name__ == "__main__":
    unittest.main()
