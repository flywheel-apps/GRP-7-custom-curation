import flywheel
import walker
import utils
import argparse


def main(client, root_container, curator):
    """Curates a flywheel project using a curator.

    Args:
        client (flywheel.Client): The flywheel sdk client
        root_container (flywheel.Container): The project to curate
        curator (Curator): The curator class to curate the project with
    """
    curate.init()
    if curator.depth_first:
        hierarchy_walker = walker.DepthFirstWalker(root_container)
    else:
        hierarchy_walker = walker.BreadthFirstWalker(root_container)
    for container in hierarchy_walker.walk():
        curator.curate_container(container)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Argument parser for curation')
    parser.add_argument('--api-key', default=None,
                        help='Pass in api key if not logged in with cli')
    parser.add_argument('--curator', '-c', required=True,
                        help='path to curator implementation')
    parser.add_argument('--input-file-one', help='Input file one')
    parser.add_argument('--input-file-two', help='Input file two')
    parser.add_argument('--input-file-three', help='Input file three')
    parser.add_argument('path', help='The resolver path to the project')

    args = parser.parse_args()
    client = flywheel.Client(args.api_key)
    root_container = client.lookup(args.path)
    curator = utils.load_converter(args.curator).Curator()

    curator.input_file_one = args.input_file_one
    curator.input_file_two = args.input_file_two
    curator.input_file_three = args.input_file_three

    main(client, root_container, curator)

