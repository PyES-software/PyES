import argparse
import os
import subprocess
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("current_version", help="Current project version", type=str)
    parser.add_argument("new_version", help="New project version", type=str)
    args = parser.parse_args()

    result = subprocess.run(
        f"git log {args.current_version}.. --format=%B%H----DELIMITER----",
        shell=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout
    commits = {
        i.split("\n")[1]: i.split("\n")[0]
        for i in result.split("----DELIMITER----\n")[:-1]
    }

    organized_commits = {
        "Features": [],
        "Enhancements": [],
        "Fixes": [],
        "Chores": [],
        "Others": [],
    }

    for sha, commit in commits.items():
        commit_type, message = commit.split(" ", maxsplit=1)

        match commit_type:
            case "[chore]":
                organized_commits["Chores"].append(
                    f"* {message} ([{sha[:7]}](https://github.com/Kastakin/PyES/commit/{sha}))\n"
                )
            case "[feat]":
                organized_commits["Features"].append(
                    f"* {message} ([{sha[:7]}](https://github.com/Kastakin/PyES/commit/{sha}))\n"
                )
            case "[fix]":
                organized_commits["Fixes"].append(
                    f"* {message} ([{sha[:7]}](https://github.com/Kastakin/PyES/commit/{sha}))\n"
                )
            case "[enh]":
                organized_commits["Enhancements"].append(
                    f"* {message} ([{sha[:7]}](https://github.com/Kastakin/PyES/commit/{sha}))\n"
                )
            case other:
                organized_commits["Others"].append(
                    f"* {message} ([{sha[:7]}](https://github.com/Kastakin/PyES/commit/{sha}))\n"
                )

    with open(f"{os.path.dirname(sys.argv[0])}/../CHANGELOG.md") as old_file:
        old_content = old_file.read()

    new_content = f"# Version {args.new_version}\n\n"

    for commit_type, commits in organized_commits.items():
        if commits:
            new_content += f"## {commit_type}\n"
            for commit in commits:
                new_content += commit
            new_content += "\n"
    new_content += "\n"

    with open(
        f"{os.path.dirname(sys.argv[0])}/../CHANGELOG.md", "w"
    ) as changelog, open(
        f"{os.path.dirname(sys.argv[0])}/../release_text.md", "w"
    ) as release_notes:
        changelog.write(new_content + old_content)
        release_notes.write(new_content)
