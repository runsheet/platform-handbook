#!/usr/bin/env python3
"""Tests for scripts/check-skills: python3 scripts/check_skills_test.py

Each case writes a small handbook into a temporary folder (not a git
repository, so the checker walks it) and checks what is reported. The
secrets are put together at run time so this file holds none itself.
"""
import importlib.machinery
import importlib.util
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
loader = importlib.machinery.SourceFileLoader("check_skills", os.path.join(HERE, "check-skills"))
spec = importlib.util.spec_from_loader("check_skills", loader)
cs = importlib.util.module_from_spec(spec)
loader.exec_module(cs)

GOOD = "---\nname: example\ndescription: An example skill, only for the checker's tests.\n---\n\nSteps.\n"


class CheckSkills(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.write("scripts/allowed-hosts.txt", "github.com\n# comment\ngo.dev\n")
        self.write("README.md", "# handbook\n")

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, path, text):
        full = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(text)

    def problems(self):
        return cs.check(self.root)

    def assertOne(self, where, words):
        got = self.problems()
        self.assertEqual(len(got), 1, got)
        self.assertTrue(got[0].startswith(where), got)
        self.assertIn(words, got[0])

    def test_good_skill_and_variant(self):
        self.write("skills/example/SKILL.md", GOOD)
        self.write("skills/example/go.md", "---\nstack: go\n---\nGo steps, see https://go.dev/doc.\n")
        self.write("skills/example/templates/x.txt", "a template\n")
        self.assertEqual(self.problems(), [])

    def test_folded_description(self):
        self.write("skills/example/SKILL.md", "---\nname: \"example\"\ndescription: >\n  A longer description that\n  folds over two lines.\nstack: go\n---\n")
        self.assertEqual(self.problems(), [])

    def test_no_skill_md(self):
        self.write("skills/example/go.md", "---\nstack: go\n---\n")
        self.assertOne("skills/example:1:", "no SKILL.md")

    def test_no_frontmatter(self):
        self.write("skills/example/SKILL.md", "# example\n")
        self.assertOne("skills/example/SKILL.md:1:", "no frontmatter")

    def test_unclosed_frontmatter(self):
        self.write("skills/example/SKILL.md", "---\nname: example\n")
        self.assertOne("skills/example/SKILL.md:1:", "no closing")

    def test_malformed_line(self):
        self.write("skills/example/SKILL.md", "---\nname: example\nthis is not yaml\n---\n")
        self.assertOne("skills/example/SKILL.md:3:", "malformed")

    def test_name_mismatch(self):
        self.write("skills/example/SKILL.md", GOOD.replace("name: example", "name: other"))
        self.assertOne("skills/example/SKILL.md:2:", "does not match its folder")

    def test_short_description(self):
        self.write("skills/example/SKILL.md", "---\nname: example\ndescription: too short\n---\n")
        self.assertOne("skills/example/SKILL.md:3:", "under 20")

    def test_empty_description(self):
        self.write("skills/example/SKILL.md", "---\nname: example\ndescription:\n---\n")
        self.assertOne("skills/example/SKILL.md:3:", "no description")

    def test_variant_without_frontmatter(self):
        self.write("skills/example/SKILL.md", GOOD)
        self.write("skills/example/go.md", "Go steps\n")
        self.assertOne("skills/example/go.md:1:", "no frontmatter")

    def test_variant_stack_mismatch(self):
        self.write("skills/example/SKILL.md", GOOD)
        self.write("skills/example/go.md", "---\nstack: typescript\n---\n")
        self.assertOne("skills/example/go.md:2:", "does not match the file name")

    def test_secrets(self):
        samples = {
            "AWS": "AKIA" + "ABCDEFGHIJKLMNOP",
            "GCP API": "AIza" + "S" * 35,
            "GCP service": '"type": "service' + '_account"',
            "GitHub token": "ghp_" + "a1" * 18,
            "GitHub fine": "github_pat_" + "A" * 30,
            "Anthropic": "sk-ant-" + "api03-" + "x" * 30,
            "OpenAI": "sk-proj-" + "y" * 30,
            "private key": "-----BEGIN RSA " + "PRIVATE KEY-----",
        }
        for what, secret in samples.items():
            with self.subTest(what):
                self.write("docs/notes.md", "line one\nkey = %s\n" % secret)
                got = self.problems()
                self.assertEqual(len(got), 1, got)
                self.assertTrue(got[0].startswith("docs/notes.md:2:"), got)
                self.assertIn(what, got[0])

    def test_url_hosts(self):
        self.write("docs/a.md", "ok https://github.com/x and http://go.dev:443/y\nbad " + "https:/" + "/evil.example.com/z.\n")
        self.assertOne("docs/a.md:2:", "evil.example.com")

    def test_layout(self):
        self.write("main.go", "package main\n")
        self.assertOne("main.go:1:", "outside")
        os.remove(os.path.join(self.root, "main.go"))
        self.write("src/x.md", "x\n")
        self.assertOne("src/x.md:1:", "outside")

    def test_this_repository_passes(self):
        self.assertEqual(cs.check(os.path.join(HERE, "..")), [])


if __name__ == "__main__":
    unittest.main()
