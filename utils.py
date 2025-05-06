import sys
from pathlib import Path
import subprocess
from cookiecutter.main import cookiecutter


def run_command(command: list[str]) -> str:
    print(" ".join(command))
    result = subprocess.run(args=command, text=True, capture_output=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}, for command: {' '.join(command)}")
        sys.exit(1)
    return result.stdout.strip()


def get_git_user_info() -> tuple[str, str]:
    user_email = run_command(['git', "config", "--get", "user.email"])
    user_name = run_command(['git', "config", "--get", "user.name"])
    authors = f"{user_name or 'user_name'} <{user_email or 'user_name@example.com'}>"
    return user_email, authors


def check_git_repository() -> None:
    command = ["git", "rev-parse", "--is-inside-work-tree"]
    is_work_tree = run_command(command)
    if not is_work_tree:
        print("Not in a git repository")
        sys.exit(1)


def get_git_repository_info() -> str:
    remote_url = run_command(['git', "config", "--get", "remote.origin.url"])
    remote = remote_url.split("/")[-1].split(".git")[0]
    return remote


def create_project() -> None:
    print("Creating project")
    check_git_repository()
    user_email, authors = get_git_user_info()
    remote = get_git_repository_info()
    print(f"{authors} <{user_email}>")
    parent_dir = Path().cwd()
    extra_context = {
        "user_email": user_email,
        "authors": authors,
        "project_name": remote,
        "repository": remote,
    }
    cookiecutter(
        template="/Users/vmenshikov/PycharmProjects/template",
        no_input=True,
        overwrite_if_exists=True,
        output_dir=parent_dir,
        extra_context=extra_context,
    )
