import flywheel
import walker
import utils
import argparse


def main(client, project, curator):
    """Curates a flywheel project using a curator.

    Args:
        client (flywheel.Client): The flywheel sdk client
        project (flywheel.Project): The project to curate
        curator (Curator): The curator class to curate the project with
    """
    if curator.depth_first:
        project_walker = walker.DepthFirstWalker(project)
    else:
        project_walker = walker.BreadthFirstWalker(project)
    for container in project_walker.walk():
        curator.curate_container(container)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Argument parser for curation')
    parser.add_argument('--api-key', default=None,
                        help='Pass in api key if not logged in with cli')
    parser.add_argument('--curator', '-c', required=True,
                        help='path to curator implementation')
    parser.add_argument('--dry-run', help='Changes will not be made')
    parser.add_argument('path', help='The resolver path to the project')

    args = parser.parse_args()
    client = flywheel.Client(args.api_key)
    project = client.lookup(args.path)
    curator = utils.load_converter(args.curator).Curator()

    if args.dry_run:
        curator.dry_run = True

    main(client, project, curator)

