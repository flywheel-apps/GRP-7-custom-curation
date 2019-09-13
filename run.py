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
        curator.input_file_one = gear_context.get_input_path('additional-input-one')
        curator.input_file_two = gear_context.get_input_path('additional-input-two')
        curator.input_file_three = gear_context.get_input_path('additional-input-three')

        root_container = gear_context.client.get(analysis.parent['id'])
        log.info('Curating project %s', root_container.label)
        log.debug('Additional file input: %s', curator.input_file_one)

        curate.main(gear_context.client, root_container, curator)

