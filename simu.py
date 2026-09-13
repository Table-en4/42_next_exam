import argparse
import importlib.util
import json
import os
import random
import re
import shutil
import subprocess
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
RENDU_DIR = Path(__file__).parent / "rendu"

CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
MAGENTA = "\033[1;35m"
BLUE = "\033[1;34m"
RESET = "\033[0m"

STRINGS = {
    "fr": {
        "title": "42 EXAM SIMULATOR (Python)",
        "lang_prompt": "[fr/en] (fr) : ",
        "no_data": "Aucune donnée trouvée dans {dir}.\nLancez d'abord : make scrape\n",
        "ranks_available": "Rangs disponibles : {ranks}",
        "rank_selected": "\nRang {rank} sélectionné. {n} niveaux disponibles.",
        "modes_header": "Modes disponibles :",
        "mode_random": "  - random (un exercice au hasard par niveau)",
        "mode_custom": "  - custom (choisir un exercice précis)",
        "invalid_rank": "Rang invalide. Choisissez parmi : {ranks}",
        "unknown_mode": "Commande inconnue. 'random', 'custom' ou 'back'.",
        "exo_list_header": "\nExercices disponibles pour le rang {rank} :",
        "exo_list_footer": "Tapez le nom de l'exercice (dossier ou fonction) :",
        "exo_not_found": "Exercice introuvable. Nom exact requis, ou 'back'.",
        "assigned": "ASSIGNATION : {name}",
        "level_header": "{level} | EXERCICE : {name}",
        "score_line": "SCORE ACTUEL : {score}/100",
        "commands_line": (
            " Commandes : subject sujet | prototype prototype | examples exemples | "
            "edit éditer | test tester | cheat tricher | finish quitter\n"
        ),
        "subject_box_title": "SUJET : {name}",
        "no_subject": "(pas de sujet enregistré)",
        "signature_title": "prototype attendue :",
        "no_signature": "(non renseignée)",
        "examples_title": "Exemples :",
        "no_examples": "(non renseignés)",
        "forbidden_title": "Fonctions interdites :",
        "test_running": "=> Lancement des tests pour {name}...",
        "test_case_ok": "  ✓ {call} -> {actual}",
        "test_case_fail": "  ✖ {call} -> {actual}  (attendu {expected})",
        "test_summary_pass": "✓ Tous les tests passent ({passed}/{total}).",
        "test_summary_fail": "✖ {passed}/{total} tests passent. Continuez !",
        "test_no_cases": "Impossible de tester automatiquement cet exercice (pas d'exemples exploitables).",
        "test_error": "Erreur à l'exécution de votre code : {error}",
        "validated_exam": "✓ Testé et validé ! +{points} pts → Score : {score}/100",
        "validated_free": "✓ Exercice validé. Tapez 'back' pour en choisir un autre.\n",
        "cheat_exam": "[CHEAT] +{points} pts → Score : {score}/100",
        "cheat_free": "[CHEAT] Exercice validé !\n",
        "exam_end_title": "EXAMEN TERMINÉ !",
        "exam_end_score": "Score final : {score}/100",
        "exam_end_prompt": "\nQue souhaitez-vous faire ?",
        "retry_line": " ├─ retry : recommencer l'examen",
        "back_line": " ├─ back : choisir un autre rang",
        "finish_line": " └─ finish : quitter\n",
        "modes_reminder": "\nModes : 'random' ou 'custom'\n",
        "unknown_cmd_exam": "Commandes : subject/sujet, prototype, examples/exemples, edit/éditer, test/tester, cheat/tricher, {extra}",
        "extra_exam_mode": "finish/quitter",
        "extra_free_mode": "back, finish/quitter",
        "goodbye": "Merci pour votre participation !",
    },
    "en": {
        "title": "42 EXAM SIMULATOR (Python)",
        "lang_prompt": "[fr/en] (fr) : ",
        "no_data": "No data found in {dir}.\nRun this first: make scrape\n",
        "ranks_available": "Available ranks: {ranks}",
        "rank_selected": "\nRank {rank} selected. {n} levels available.",
        "modes_header": "Available modes:",
        "mode_random": "  - random (one exercise per level, drawn at random)",
        "mode_custom": "  - custom (pick a specific exercise)",
        "invalid_rank": "Invalid rank. Choose from: {ranks}",
        "unknown_mode": "Unknown command. 'random', 'custom' or 'back'.",
        "exo_list_header": "\nAvailable exercises for rank {rank}:",
        "exo_list_footer": "Type the exercise name (folder or function):",
        "exo_not_found": "Exercise not found. Exact name required, or 'back'.",
        "assigned": "ASSIGNED: {name}",
        "level_header": "{level} | EXERCISE: {name}",
        "score_line": "CURRENT SCORE: {score}/100",
        "commands_line": (
            "Commands: subject brief | prototype prototype | examples examples | "
            "edit edit | test run tests | cheat skip | finish quit\n"
        ),
        "subject_box_title": "SUBJECT: {name}",
        "no_subject": "(no subject saved)",
        "signature_title": "Expected prototype:",
        "no_signature": "(not available)",
        "examples_title": "Examples:",
        "no_examples": "(not available)",
        "forbidden_title": "Forbidden functions:",
        "test_running": "=> Running tests for {name}...",
        "test_case_ok": "  ✓ {call} -> {actual}",
        "test_case_fail": "  ✖ {call} -> {actual}  (expected {expected})",
        "test_summary_pass": "✓ All tests pass ({passed}/{total}).",
        "test_summary_fail": "✖ {passed}/{total} tests pass. Keep going!",
        "test_no_cases": "Cannot auto-test this exercise (no usable examples).",
        "test_error": "Error while running your code: {error}",
        "validated_exam": "✓ Tested and validated! +{points} pts → Score: {score}/100",
        "validated_free": "✓ Exercise validated. Type 'back' to pick another.\n",
        "cheat_exam": "[CHEAT] +{points} pts → Score: {score}/100",
        "cheat_free": "[CHEAT] Exercise validated!\n",
        "exam_end_title": "EXAM FINISHED!",
        "exam_end_score": "Final score: {score}/100",
        "exam_end_prompt": "\nWhat would you like to do?",
        "retry_line": " ├─ retry: restart the exam",
        "back_line": " ├─ back: pick another rank",
        "finish_line": " └─ finish: quit\n",
        "modes_reminder": "\nModes: 'random' or 'custom'\n",
        "unknown_cmd_exam": "Commands: subject, prototype, examples, edit, test, cheat, {extra}",
        "extra_exam_mode": "finish",
        "extra_free_mode": "back, finish",
        "goodbye": "Thanks for taking part!",
    },
}


class Translator:
    def __init__(self, lang):
        self.lang = lang if lang in STRINGS else "fr"

    def t(self, key, **kwargs):
        text = STRINGS[self.lang].get(key, STRINGS["fr"][key])
        return text.format(**kwargs)


class ExamState:
    def __init__(self):
        self.rank = None
        self.levels = []
        self.exam_exos = {}
        self.current_level_index = 0
        self.score = 0
        self.points_per_level = 0
        self.is_exam_mode = False
        self.current_exo_dir = None
        self.current_exo_id = None
        self.current_func_name = None
        self.current_display_name = None


def list_ranks():
    if not DATA_DIR.exists():
        return []
    return sorted(p.name.replace("rank", "") for p in DATA_DIR.glob("rank*") if p.is_dir())


def list_levels(rank):
    rank_dir = DATA_DIR / f"rank{rank}"
    if not rank_dir.exists():
        return []
    levels = [p for p in rank_dir.glob("level*") if p.is_dir()]
    return sorted(levels, key=lambda p: int(p.name.replace("level", "") or 0))


def list_exercises(level_dir):
    return sorted(p for p in level_dir.iterdir() if p.is_dir())


def list_all_exercises(rank):
    result = []
    for level_dir in list_levels(rank):
        result.extend(list_exercises(level_dir))
    return result


def read_text(path, default=""):
    if path.exists():
        return path.read_text(encoding="utf-8")
    return default


def read_meta(exo_dir):
    meta_path = exo_dir / "meta.json"
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return {}


def func_name_from_signature(signature):
    match = re.match(r"def\s+([a-zA-Z0-9_]+)\s*\(", signature.strip())
    return match.group(1) if match else None


def display_name_for(exo_dir):
    meta = read_meta(exo_dir)
    title = meta.get("title")
    if title and not title.startswith("#"):
        return title
    signature = read_text(exo_dir / "signature.txt")
    func_name = func_name_from_signature(signature)
    return func_name or exo_dir.name


def subject_path_for(exo_dir, lang):
    if lang == "fr":
        fr_path = exo_dir / "subject.fr.md"
        if fr_path.exists():
            return fr_path
    return exo_dir / "subject.md"


def find_exercise(exos, cmd):
    needle = cmd.strip().lower()
    for exo in exos:
        meta = read_meta(exo)
        aliases = {
            exo.name.lower(),
            display_name_for(exo).lower(),
            str(meta.get("name") or "").lower(),
            str(meta.get("file") or "").lower(),
            str(meta.get("file") or "").removesuffix(".py").lower(),
        }
        if needle in aliases:
            return exo
    return None


def print_box(lines):
    width = max(len(line) for line in lines) + 4
    print(f"{CYAN}╭{'─' * width}╮{RESET}")
    for line in lines:
        print(f"{CYAN}│{RESET} {line.ljust(width - 2)} {CYAN}│{RESET}")
    print(f"{CYAN}╰{'─' * width}╯{RESET}")


def parse_examples(text):
    lines = text.splitlines()
    cases = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == "Input" and i + 3 < len(lines):
            if lines[i + 2].strip() == "Output":
                call = lines[i + 1].strip()
                expected = lines[i + 3].strip()
                if call and expected:
                    cases.append((call, expected))
                i += 4
                continue
        i += 1
    return cases


def load_student_module(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_auto_tests(exo_dir, rendu_path):
    signature = read_text(exo_dir / "signature.txt")
    func_name = func_name_from_signature(signature)
    examples = read_text(exo_dir / "examples.md")
    cases = parse_examples(examples)
    if not func_name or not cases:
        return {"cases": [], "passed": 0, "total": 0, "error": None}

    try:
        module = load_student_module(rendu_path, f"rendu_{exo_dir.name}")
    except Exception as exc:
        return {"cases": [], "passed": 0, "total": len(cases), "error": str(exc)}

    if not hasattr(module, func_name):
        return {"cases": [], "passed": 0, "total": len(cases), "error": f"function '{func_name}' not found"}

    scope = {
        name: value
        for name, value in vars(module).items()
        if callable(value) and not name.startswith("_")
    }
    results = []
    passed = 0
    for call, expected in cases:
        try:
            actual = eval(call, scope)
            expected_val = eval(expected, {})
            ok = actual == expected_val
        except Exception as exc:
            actual = f"EXCEPTION: {exc}"
            ok = False
        if ok:
            passed += 1
        results.append({"call": call, "expected": expected, "actual": repr(actual), "ok": ok})
    return {"cases": results, "passed": passed, "total": len(cases), "error": None}


def stub_path(func_name):
    RENDU_DIR.mkdir(parents=True, exist_ok=True)
    return RENDU_DIR / f"{func_name}.py"


def ensure_stub(exo_dir, func_name):
    path = stub_path(func_name)
    if not path.exists():
        signature = read_text(exo_dir / "signature.txt").strip()
        lines = [line.strip() for line in signature.splitlines() if line.strip()]
        if lines:
            content = "\n\n".join(f"{line}\n    pass" for line in lines) + "\n"
        else:
            content = "pass\n"
        path.write_text(content, encoding="utf-8")
    return path


def build_exam(state):
    state.exam_exos = {}
    for level_dir in list_levels(state.rank):
        exos = list_exercises(level_dir)
        if exos:
            state.exam_exos[level_dir.name] = random.choice(exos)
    state.levels = list(state.exam_exos.keys())


def enter_exercise(state, exo_dir):
    state.current_exo_dir = exo_dir
    state.current_exo_id = exo_dir.name
    signature = read_text(exo_dir / "signature.txt")
    state.current_func_name = func_name_from_signature(signature) or exo_dir.name
    state.current_display_name = display_name_for(exo_dir)
    ensure_stub(exo_dir, state.current_func_name)


def start_level(state, index, tr):
    level_name = state.levels[index]
    exo_dir = state.exam_exos[level_name]
    enter_exercise(state, exo_dir)
    print_box([
        tr.t("level_header", level=level_name.upper(), name=state.current_display_name),
        tr.t("score_line", score=state.score),
    ])
    print(tr.t("commands_line"))


def start_random_exam(state, tr):
    state.score = 0
    state.current_level_index = 0
    build_exam(state)
    total = len(state.levels)
    state.points_per_level = 100 // total if total else 0
    state.is_exam_mode = True
    if total == 0:
        return False
    start_level(state, 0, tr)
    return True


def show_exam_end(state, tr):
    print_box([
        tr.t("exam_end_title"),
        tr.t("exam_end_score", score=state.score),
    ])
    if RENDU_DIR.exists():
        shutil.rmtree(RENDU_DIR)
    RENDU_DIR.mkdir(parents=True, exist_ok=True)
    print(tr.t("exam_end_prompt"))
    print(f"{BLUE}{tr.t('retry_line')}{RESET}")
    print(f"{BLUE}{tr.t('back_line')}{RESET}")
    print(f"{BLUE}{tr.t('finish_line')}{RESET}")


def print_custom_list(rank, tr):
    exos = list_all_exercises(rank)
    if not exos:
        print(f"{RED}{tr.t('exo_not_found')}{RESET}\n")
        return
    print(tr.t("exo_list_header", rank=rank))
    for exo in exos:
        level_tag = exo.parent.name
        title = display_name_for(exo)
        print(f"  • [{level_tag}] {exo.name}  ({title})")
    print(tr.t("exo_list_footer"))


def cmd_subject(state, tr):
    print(f"\n{BLUE}╭─── {tr.t('subject_box_title', name=state.current_display_name)} ───╮{RESET}\n")
    print(read_text(subject_path_for(state.current_exo_dir, tr.lang), tr.t("no_subject")))
    forbidden = read_meta(state.current_exo_dir).get("forbidden") or []
    if forbidden:
        print(f"\n{YELLOW}{tr.t('forbidden_title')}{RESET} {', '.join(forbidden)}")
    print(f"\n{BLUE}╰{'─' * 48}╯{RESET}\n")


def cmd_signature(state, tr):
    print(f"\n{BLUE}{tr.t('signature_title')}{RESET}")
    print(read_text(state.current_exo_dir / "signature.txt", tr.t("no_signature")))
    print()


def cmd_examples(state, tr):
    print(f"\n{BLUE}{tr.t('examples_title')}{RESET}")
    print(read_text(state.current_exo_dir / "examples.md", tr.t("no_examples")))
    print()


def cmd_edit(state):
    path = stub_path(state.current_func_name)
    editor = os.environ.get("EDITOR")
    vim_edit = subprocess.call(["vim", str(path)])
    if vim_edit:
        return
    if editor:
        subprocess.call([editor, str(path)])
    elif shutil.which("vim"):
        subprocess.call(["vim", str(path)])
    else:
        subprocess.call(["xdg-open", str(path)])


def advance_level(state, tr):
    state.current_level_index += 1
    if state.current_level_index >= len(state.levels):
        show_exam_end(state, tr)
        state.is_exam_mode = False
        return "menu"
    start_level(state, state.current_level_index, tr)
    return "exam"


def cmd_test(state, tr):
    path = stub_path(state.current_func_name)
    print(tr.t("test_running", name=state.current_display_name))
    outcome = run_auto_tests(state.current_exo_dir, path)

    if outcome["error"]:
        print(f"{RED}{tr.t('test_error', error=outcome['error'])}{RESET}\n")
        return "exam"

    if outcome["total"] == 0:
        print(f"{YELLOW}{tr.t('test_no_cases')}{RESET}\n")
        return "exam"

    for case in outcome["cases"]:
        if case["ok"]:
            print(f"{GREEN}{tr.t('test_case_ok', call=case['call'], actual=case['actual'])}{RESET}")
        else:
            print(f"{RED}{tr.t('test_case_fail', call=case['call'], actual=case['actual'], expected=case['expected'])}{RESET}")

    passed, total = outcome["passed"], outcome["total"]
    if passed == total:
        print(f"{GREEN}{tr.t('test_summary_pass', passed=passed, total=total)}{RESET}")
        if state.is_exam_mode:
            state.score += state.points_per_level
            print(f"{GREEN}{tr.t('validated_exam', points=state.points_per_level, score=state.score)}{RESET}")
            return advance_level(state, tr)
        print(f"{GREEN}{tr.t('validated_free')}{RESET}")
        return "exam"

    print(f"{RED}{tr.t('test_summary_fail', passed=passed, total=total)}{RESET}\n")
    return "exam"


def cmd_cheat(state, tr):
    if state.is_exam_mode:
        state.score += state.points_per_level
        print(f"{MAGENTA}{tr.t('cheat_exam', points=state.points_per_level, score=state.score)}{RESET}")
        return advance_level(state, tr)
    print(f"{MAGENTA}{tr.t('cheat_free')}{RESET}")
    return "custom"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["fr", "en"], default=None)
    args = parser.parse_args()

    lang = args.lang
    if lang is None:
        try:
            answer = input(STRINGS["fr"]["lang_prompt"]).strip().lower()
        except EOFError:
            answer = ""
        lang = answer if answer in STRINGS else "fr"

    tr = Translator(lang)
    RENDU_DIR.mkdir(parents=True, exist_ok=True)

    state = ExamState()
    current_state = "choose_rank"

    ranks = list_ranks()
    print(f"{CYAN}╔══════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{tr.t('title').center(48)}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════════╝{RESET}\n")
    if not ranks:
        print(f"{RED}{tr.t('no_data', dir=DATA_DIR)}{RESET}")
        return

    print(tr.t("ranks_available", ranks=", ".join(ranks)))

    while True:
        if current_state == "choose_rank":
            prompt = f"{CYAN}examshell{RESET}> "
        elif current_state in ("choose_mode", "custom_choose_exo"):
            prompt = f"{CYAN}examshell/rank{state.rank}{RESET}> "
        elif current_state == "exam":
            if state.is_exam_mode:
                prompt = f"{GREEN}{state.current_display_name}{RESET} [{YELLOW}{state.score} pts{RESET}]> "
            else:
                prompt = f"{GREEN}{state.current_display_name}{RESET}> "
        else:
            prompt = "> "

        try:
            raw = input(prompt)
        except EOFError:
            print(f"\n{tr.t('goodbye')}")
            break

        cmd = raw.strip()

        if cmd in ("finish", "quitter"):
            if RENDU_DIR.exists():
                shutil.rmtree(RENDU_DIR)
            print(f"{BLUE}{tr.t('goodbye')}{RESET}")
            break

        if current_state == "choose_rank":
            if cmd in ranks:
                state.rank = cmd
                levels = list_levels(cmd)
                print(tr.t("rank_selected", rank=cmd, n=len(levels)))
                print(tr.t("modes_header"))
                print(tr.t("mode_random"))
                print(tr.t("mode_custom"))
                print()
                current_state = "choose_mode"
            else:
                print(f"{RED}{tr.t('invalid_rank', ranks=', '.join(ranks))}{RESET}\n")

        elif current_state == "choose_mode":
            if cmd in ("random", "retry"):
                if start_random_exam(state, tr):
                    current_state = "exam"
            elif cmd == "custom":
                print_custom_list(state.rank, tr)
                current_state = "custom_choose_exo"
            elif cmd == "back":
                current_state = "choose_rank"
                print(tr.t("ranks_available", ranks=", ".join(ranks)))
            else:
                print(f"{RED}{tr.t('unknown_mode')}{RESET}\n")

        elif current_state == "custom_choose_exo":
            exos = list_all_exercises(state.rank)
            found = find_exercise(exos, cmd)
            if found:
                state.is_exam_mode = False
                state.score = 0
                enter_exercise(state, found)
                print_box([tr.t("assigned", name=state.current_display_name)])
                print(tr.t("commands_line"))
                current_state = "exam"
            elif cmd == "back":
                current_state = "choose_mode"
                print(tr.t("modes_reminder"))
            else:
                print(f"{RED}{tr.t('exo_not_found')}{RESET}\n")

        elif current_state == "exam":
            if cmd in ("subject", "sujet", "brief"):
                cmd_subject(state, tr)
            elif cmd == "signature":
                cmd_signature(state, tr)
            elif cmd in ("examples", "exemples"):
                cmd_examples(state, tr)
            elif cmd in ("edit", "éditer", "editer"):
                cmd_edit(state)
            elif cmd in ("test", "tester"):
                result = cmd_test(state, tr)
                if result == "menu":
                    current_state = "choose_mode"
            elif cmd in ("cheat", "tricher"):
                result = cmd_cheat(state, tr)
                if result == "menu":
                    current_state = "choose_mode"
                elif result == "custom":
                    current_state = "custom_choose_exo"
                    print_custom_list(state.rank, tr)
            elif cmd == "back" and not state.is_exam_mode:
                current_state = "custom_choose_exo"
                print_custom_list(state.rank, tr)
            else:
                extra = tr.t("extra_exam_mode") if state.is_exam_mode else tr.t("extra_free_mode")
                print(tr.t("unknown_cmd_exam", extra=extra))
                print()


if __name__ == "__main__":
    main()
