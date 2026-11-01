import sys
from pathlib import Path


def main(repo: str):
    all_counts = {}
    projects_path = Path(repo) / 'projects'
    for project in projects_path.iterdir():
        if project.name == 'README.md':
            continue
        print(project)
        counts = {'total': 0, 'extensions': {}}
        golds_dir = project / 'golds'
        if golds_dir.is_dir():
            c = 0
            for gold in (project / 'golds').iterdir():
                counts['total'] += 1
                c += 1
                if c <= 5:
                    print('   ', gold.name)
                counts['extensions'].setdefault(gold.suffix, 0)
                counts['extensions'][gold.suffix] += 1
        all_counts[project.name] = counts.copy()
    print_counts(all_counts)


def print_counts(all_counts: dict):
    for project in sorted(all_counts):
        extensions = sorted(all_counts[project]['extensions'].keys())
        print(f'| {project:35s} | {all_counts[project]["total"]:4d} | {" ".join(extensions):5s} |')



if __name__ == '__main__':

    repo = sys.argv[1]
    main(repo)