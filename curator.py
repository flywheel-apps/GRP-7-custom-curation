import flywheel
import abc


class Curator(abc.ABC):
    def __init__(self, depth_first=True):
        """An abstract class to be implemented in the input python file"""
        self.depth_first = depth_first

    def curate_container(self, container):
        """Curates a generic container.

        Args:
            container (flywheel.Container| flywheel.FileEntry)
        """
        try:
            container_type = container.container_type
        except AttributeError:
            # element is a file and has no children
            return self.curate_file(container)

        if container_type == 'project':
            return self.curate_project(container)
        elif container_type == 'subject':
            return self.curate_subject(container)
        elif container_type == 'session':
            return self.curate_session(container)
        elif container_type == 'acquisition':
            return self.curate_acquisition(container)
        else:
            return self.curate_analysis(container)

    @abc.abstractmethod
    def curate_project(self, project):
        """Updates a project.

        Args:
            project (flywheel.Project): The project object to curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_subject(self, subject):
        """Updates a subject.

        Args:
            subject (flywheel.Subject): The subject object to curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_session(self, session):
        """Updates a session.

        Args:
            session (flywheel.Session): The session object to curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_acquisition(self, acquisition):
        """Updates an acquisition.

        Args:
            acquisition (flywheel.Acquisition): The acquisition object to
                curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_analysis(self, analysis):
        """Updates an analysis.

        Args:
            analysis (flywheel.Analysis): The analysis object to curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_file(self, file_):
        """Updates a file.

        Args:
            file_ (flywheel.FileEntry): The file entry object to curate
        """
        raise NotImplementedError

    def validate_project(self, project):
        """Validates if a project has been correctly curated.

        Args:
            project (flywheel.Project): The project object to validate

        Returns:
            bool: Whether or not the project is curated correctly
        """
        return False

    def validate_subject(self, subject):
        """Validates if a subject has been correctly curated.

        Args:
            subject (flywheel.Subject): The subject object to validate

        Returns:
            bool: Whether or not the subject is curated correctly
        """
        return False

    def validate_session(self, session):
        """Validates if a session has been correctly curated.

        Args:
            session (flywheel.Session): The session object to validate

        Returns:
            bool: Whether or not the session is curated correctly
        """
        return False

    def validate_acquisition(self, acquisition):
        """Validates if a acquisition has been correctly curated.

        Args:
            acquisition (flywheel.Acquisition): The acquisition object to
                validate

        Returns:
            bool: Whether or not the acquisition is curated correctly
        """
        return False

    def validate_analysis(self, analysis):
        """Validates if a analysis has been correctly curated.

        Args:
            analysis (flywheel.Analysis): The analysis object to validate

        Returns:
            bool: Whether or not the analysis is curated correctly
        """
        return False

    def validate_file(self, file_):
        """Validates if a file_ has been correctly curated.

        Args:
            file_ (flywheel.FileEntry): The file entry object to validate

        Returns:
            bool: Whether or not the file_ is curated correctly
        """
        return False
