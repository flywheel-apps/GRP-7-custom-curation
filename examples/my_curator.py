import curator
import tempfile
import zipfile
import json
import logging

log = logging.getLogger('my_curator')
log.setLevel('DEBUG')

SESSION_LABEL_CORRECTION = {
    'screening': 'Screening',
    'w04': 'Week_04',
    'w12': 'Week_12',
    'w16': 'Week_16',
    'w20': 'Week_20',
    'w24': 'Week_24',
    'w28': 'Week_28',
    'w36': 'Week_36',
    'w48': 'Week_48',
    'REV1': 'Relapse_Evaluation_1'
}


class Curator(curator.Curator):
    def __init__(self):
        super(Curator, self).__init__(depth_first=True)

    def curate_project(self, project):
        log.debug('Curating project with %s', self.input_file_one)
        if self.input_file_one:
            with open(self.input_file_one, 'r') as fp:
                updates = json.load(fp)
            log.debug('Updates are %s', updates)
            project.update(updates)

    def curate_subject(self, subject):
        pass

    def curate_session(self, session):
        new_label = SESSION_LABEL_CORRECTION.get(session.label)
        if new_label:
            session.update({'label': new_label})

    def curate_acquisition(self, acquisition):
        acquisition.update_info({'Harsha': 10})

    def curate_analysis(self, analysis):
        pass

    def curate_file(self, file_):
        new_classification = self.classifiy_file(file_)
        if new_classification is None:
            return
        else:
            file_.update

    def classifiy_file(self, file_):
        TR = file_.info.get('RepetitionTime')
        TE = file_.info.get('EchoTime')
        TI = file_.info.get('InversionTime')
        SD = file_.info.get('SeriesDescription')
        IOP = file_.info.get('ImageOrientationPatient')
        measurement = []
        features = []
        intent = []
        custom = []
        contrast = False

        if TE < 30 and TR < 800:
            measurement = ['T1w']
        elif (TE > 50 and TR > 2000) and (TI == 0 or TI is None):
            measurement = ['T2w']
        elif TE >50 and TR > 8000 and TI > 1500 and TI < 3000:
            custom = ['FLAIR']
        elif TE < 50 and TR > 1000:
            custom = ['PDw']
        else:
            return

        if 'post' in SD.lower():
            if 'T1w' in measurement or 'FLAIR' in custom:
                contrast =  True

        if file_.zip_member_count < 10:
            intent = ['Localizer']

        if not self.check_consistent_IOP(file_):
            custom = custom + ['3-Plane']

    def check_consistent_IOP(self, file_):
        if not file_.type == 'dicom':
            return True
        tempfile_path = tempfile.mktemp()
        file_.download(tempfile_path)

        for image in tempfile_path:
            dcm = pydicom.dcmread(image)
            if dcm.ImageOrientationPatient != file_.info.get('ImageOrientationPatient'):
                return False
        return True


