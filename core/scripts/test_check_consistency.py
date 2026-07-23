# core/scripts/test_check_consistency.py
import subprocess, sys, tempfile, os, textwrap
SCRIPT = os.path.join(os.path.dirname(__file__), "check_consistency.py")

GLOSSARY = textwrap.dedent("""\
    | JP | EN | Aliases/Banned | Gender/Context |
    |-|-|-|-|
    | 西部戦線 | Western Front | Western Theatre, West Front | place |
    | 田中 | Tanaka-san | | male, teacher |
    | 大鳥 | Ootori | Otori, Ōtori | female |
    | グレムリン | Gremlin | | term |
    | 超越者 | Transcendent | | term |
    | アイちゃん | Ai-chan | Ai | character |
""")

def run(chapter_text, extra_args=(), glossary=GLOSSARY):
    d = tempfile.mkdtemp()
    g = os.path.join(d, "glossary.md"); c = os.path.join(d, "ch.md")
    open(g, "w", encoding="utf-8").write(glossary)
    open(c, "w", encoding="utf-8").write(chapter_text)
    p = subprocess.run([sys.executable, SCRIPT, "--glossary", g, c, *extra_args],
                       capture_output=True, text=True)
    return p.returncode, p.stdout

def test_clean_passes():
    rc, out = run("They marched to the Western Front. Tanaka-san smiled. Ootori waited.")
    assert rc == 0, out

def test_banned_alias_fails():
    rc, out = run("They reached the Western Theatre at dawn.")
    assert rc == 1 and "Western Theatre" in out

def test_name_drift_fails():
    rc, out = run("Ootorri turned away.")  # close-but-wrong spelling
    assert rc == 1 and "Ootorri" in out

def test_regular_plurals_pass():
    rc, out = run("Gremlins fought while Transcendents watched.")
    assert rc == 0, out

def test_alias_inside_its_canonical_term_passes():
    rc, out = run("The Ai-chan Model sat on the shelf.")
    assert rc == 0, out

def test_standalone_alias_still_fails():
    rc, out = run("Ai sat on the shelf.")
    assert rc == 1 and "banned alias 'Ai'" in out

def test_titlecase_alias_does_not_flag_lowercase_common_word():
    glossary = GLOSSARY + "| ギャザ | Gath | Gather | game title |\n"
    rc, out = run("They gather materials, then play Gath.", glossary=glossary)
    assert rc == 0, out

def test_titlecase_alias_still_fails_at_matching_case():
    glossary = GLOSSARY + "| ギャザ | Gath | Gather | game title |\n"
    rc, out = run("They played Gather after dinner.", glossary=glossary)
    assert rc == 1 and "banned alias 'Gather'" in out

def test_honorific_mismatch_fails():
    rc, out = run("Tanaka-kun raised a hand.")
    assert rc == 1 and "Tanaka-kun" in out

def test_multiple_glossary_honorifics_for_same_base_pass():
    glossary = GLOSSARY + "| 青ちゃん | Ao-chan | | nickname |\n| 青さん | Ao-san | | nickname |\n"
    rc, out = run("Ao-chan waved to Ao-san.", glossary=glossary)
    assert rc == 0, out

def test_unlisted_honorific_fails_once_with_multiple_allowed_forms():
    glossary = GLOSSARY + "| 青ちゃん | Ao-chan | | nickname |\n| 青さん | Ao-san | | nickname |\n"
    rc, out = run("Ao-kun waved.", glossary=glossary)
    assert rc == 1 and out.count("honorific mismatch") == 1, out

def test_macron_fails():
    rc, out = run("Ōtori is banned anyway, but ō alone must flag too.")
    assert rc == 1 and "macron" in out.lower()

if __name__ == "__main__":
    for f in [v for k, v in list(globals().items()) if k.startswith("test_")]:
        f()
    print("ok")
