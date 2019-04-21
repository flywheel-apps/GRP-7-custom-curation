import curator


class Curator(curator.Curator):
    def __init__(self):
        super(Curator, self).__init__(depth_first=True)

    def curate_project(self, project):
        project.update_info({'Harsha': 7})

    def curate_subject(self, subject):
        subject.update_info({'Harsha': 8})

    def curate_session(self, session):
        session.update_info({'Harsha': 9})

    def curate_acquisition(self, acquisition):
        acquisition.update_info({'Harsha': 10})

    def curate_analysis(self, analysis):
        analysis.update_info({'Harsha': 11})

    def curate_file(self, file_):
        pass

