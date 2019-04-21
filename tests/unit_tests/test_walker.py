import mock
import pytest
import walker


def test_depth_first_walker_project():
    w = walker.DepthFirstWalker(mock.MagicMock(container_type='project',
                                               subjects=lambda: [], files=[]))
    containers = list(w.walk())
    assert len(containers) == 1
    assert containers[0].container_type == 'project'


def test_depth_first_walker_subject():
    w = walker.DepthFirstWalker(mock.MagicMock(container_type='subject',
                                               sessions=lambda: [], files=[]))
    containers = list(w.walk())
    assert len(containers) == 1
    assert containers[0].container_type == 'subject'


def test_depth_first_walker_session():
    w = walker.DepthFirstWalker(mock.MagicMock(container_type='session',
                                               acquisitions=lambda: [],
                                               files=[]))
    containers = list(w.walk())
    assert len(containers) == 1
    assert containers[0].container_type == 'session'


def test_depth_first_walker_acquisition():
    w = walker.DepthFirstWalker(mock.MagicMock(container_type='acquisition',
                                               files=[]))
    containers = list(w.walk())
    assert len(containers) == 1
    assert containers[0].container_type == 'acquisition'


def test_depth_first_walker_children():
    subjects = lambda: [mock.MagicMock(container_type='subject',
                                       sessions=lambda: [], files=[])]
    w = walker.DepthFirstWalker(mock.MagicMock(container_type='project',
                                               subjects=subjects, files=[]))

    containers = list(w.walk())
    assert len(containers) == 2
    assert containers[0].container_type == 'project'
    assert containers[1].container_type == 'subject'

