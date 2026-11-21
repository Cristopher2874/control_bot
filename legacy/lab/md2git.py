from pathlib import Path
import subprocess

def push_md_to_repo(
    md_content: str,
    relative_path: str,
    branch: str = "main",
    commit_message: str = "update docs",
    repo_root: str | Path | None = None
) -> dict:
    """
    Writes MD content to a file in the repo and pushes to a branch.

    Args:
        md_content: The markdown string you want to write
        relative_path: Path inside repo, ex: "docs/notes.md"
        branch: Branch to push to
        commit_message: Git commit message
        repo_root: Path to repo. If None, uses current working dir.

    Returns:
        dict with file_path, branch, commit_hash
    """
    repo_root = Path(repo_root).resolve() if repo_root else Path.cwd().resolve()
    target_file = repo_root / relative_path

    # 1. Write file - VS Code will pick it up instantly
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(md_content, encoding='utf-8')

    # 2. Git operations
    def git(*args):
        result = subprocess.run(
            ["git"] + list(args),
            cwd=repo_root,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr}")
        return result.stdout.strip()

    # Ensure we are on the right branch
    git("checkout", "-B", branch)
    git("add", relative_path)
    
    # Avoid empty commit error
    status = git("status", "--porcelain", relative_path)
    if not status:
        return {"file_path": str(target_file), "branch": branch, "status": "no changes"}

    git("commit", "-m", commit_message)
    commit_hash = git("rev-parse", "HEAD")
    git("push", "-u", "origin", branch)

    return {
        "file_path": str(target_file),
        "branch": branch,
        "commit_hash": commit_hash,
        "status": "pushed"
    }

#from git_writer import push_md_to_repo

md = """
# Mi reporte de inventario

- Stock sucursal 1: 20 charolas
- Merma: 1 charola
"""

result = push_md_to_repo(
    md_content=md,
    relative_path="docs/reporte-inventario.md",
    branch="feature/inventario-docs",
    commit_message="docs: agregar reporte inventario"
)

print(result)
# -> {'file_path': 'C:\\tu\\repo\\docs\\reporte-inventario.md', 'branch': '...', 'commit_hash': 'a1b2c3...', 'status': 'pushed'}