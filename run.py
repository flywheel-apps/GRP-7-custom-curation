import curate
import flywheel
import logging
import utils

log = logging.getLogger(__name__)


if __name__ == '__main__':
    with flywheel.GearContext() as gear_context:
        gear_context.init_logging()
        log.info('Entered gear context')

        analysis_id = gear_context.destination['id']
        analysis = gear_context.client.get_analysis(analysis_id)
        curator_path = gear_context.get_input_path('curator')
        curator = utils.load_converter(curator_path).Curator()

        project = gear_context.client.get(analysis.parent['id'])
        log.info('Curating project %s', project.label)

        curate.main(gear_context.client, project, curator)

