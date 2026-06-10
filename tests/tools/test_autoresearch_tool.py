import json
import subprocess
from pathlib import Path

from tools.autoresearch_tool import autoresearch
from toolsets import resolve_toolset


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return proc.stdout.strip()


def _init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / "train.py").write_text("score=1.0\n", encoding="utf-8")
    (repo / "run.py").write_text(
        "import re\n"
        "text=open('train.py').read()\n"
        "score=float(re.search(r'score=([0-9.]+)', text).group(1))\n"
        "print(f'val_bpb: {score:.6f}')\n"
        "print('peak_vram_mb: 1024.0')\n",
        encoding="utf-8",
    )
    _git(repo, "add", "train.py", "run.py")
    _git(repo, "commit", "-m", "init")
    return repo


def _call(args):
    return json.loads(autoresearch(args))


def test_autoresearch_toolset_resolves():
    assert "autoresearch" in resolve_toolset("autoresearch")


def test_setup_creates_branch_and_results_file(tmp_path):
    repo = _init_repo(tmp_path)
    result = _call({"action": "setup", "repo_path": str(repo), "run_tag": "test"})

    assert result["success"] is True
    assert result["branch"] == "autoresearch/test"
    assert (repo / "results.tsv").read_text(encoding="utf-8").splitlines()[0] == (
        "commit\tmetric\tmemory_gb\tstatus\tdescription"
    )


def test_run_once_keeps_first_metric_and_logs_result(tmp_path):
    repo = _init_repo(tmp_path)
    result = _call({
        "action": "run_once",
        "repo_path": str(repo),
        "run_command": "python run.py",
        "description": "baseline",
        "timeout_seconds": 30,
    })

    assert result["success"] is True
    assert result["status"] == "keep"
    assert result["metric"] == 1.0
    assert result["memory_gb"] == 1.0
    assert (repo / "run.log").read_text(encoding="utf-8").startswith("val_bpb:")
    assert "\tkeep\tbaseline" in (repo / "results.tsv").read_text(encoding="utf-8")


def test_run_once_discards_non_improvement_commit(tmp_path):
    repo = _init_repo(tmp_path)
    _call({
        "action": "run_once",
        "repo_path": str(repo),
        "run_command": "python run.py",
        "description": "baseline",
        "timeout_seconds": 30,
    })
    start = _git(repo, "rev-parse", "--short=7", "HEAD")

    (repo / "train.py").write_text("score=1.5\n", encoding="utf-8")
    result = _call({
        "action": "run_once",
        "repo_path": str(repo),
        "run_command": "python run.py",
        "description": "worse score",
        "timeout_seconds": 30,
    })

    assert result["status"] == "discard"
    assert result["reset_performed"] is True
    assert _git(repo, "rev-parse", "--short=7", "HEAD") == start
    assert (repo / "train.py").read_text(encoding="utf-8") == "score=1.0\n"
    assert "\tdiscard\tworse score" in (repo / "results.tsv").read_text(encoding="utf-8")


def test_run_once_keeps_improvement_commit(tmp_path):
    repo = _init_repo(tmp_path)
    _call({
        "action": "run_once",
        "repo_path": str(repo),
        "run_command": "python run.py",
        "description": "baseline",
        "timeout_seconds": 30,
    })
    start = _git(repo, "rev-parse", "--short=7", "HEAD")

    (repo / "train.py").write_text("score=0.5\n", encoding="utf-8")
    result = _call({
        "action": "run_once",
        "repo_path": str(repo),
        "run_command": "python run.py",
        "description": "better score",
        "timeout_seconds": 30,
    })

    assert result["status"] == "keep"
    assert result["reset_performed"] is False
    assert _git(repo, "rev-parse", "--short=7", "HEAD") != start
    assert (repo / "train.py").read_text(encoding="utf-8") == "score=0.5\n"


def test_run_once_refuses_unrelated_dirty_files(tmp_path):
    repo = _init_repo(tmp_path)
    (repo / "notes.txt").write_text("do not clobber\n", encoding="utf-8")

    result = _call({
        "action": "run_once",
        "repo_path": str(repo),
        "run_command": "python run.py",
        "description": "unsafe",
        "timeout_seconds": 30,
    })

    assert result["success"] is False
    assert "dirty files outside" in result["error"]
    assert (repo / "notes.txt").read_text(encoding="utf-8") == "do not clobber\n"
