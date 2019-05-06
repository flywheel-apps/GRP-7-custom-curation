### Generalized Custom Curation Gear
There are a lot of cases where specific logic must be used to curate a givent project. This custom curation gear is able to take an implementation of the Curator Class and execute it on a project, walking down the hierarchy through project, subject, session, acquisition, and file containers.

## The Curator Class
### Curate Methods
In order to implement the Curator Class, a curate method for each container type (excluding groups and collections)
must be defined. For each container, the method is called `curate_<container_type>`. The method takes the container as an input.

For example, for the project container the curation method is defined as: 
``` python
curate_project(self, project)
```

This pattern is consistent for all containers. For the files container there is a `curate_file` method that must be defined as well. Note that in order to not overwrite the reserved word "file", the input is `file_`. Thus, the method for curating files is:
``` python
curate_file(self, file_)
```

### Validate Methods
In addition to the curate methods, the implementation can inherit _validate_ methods specific to each container. By default these methods will always return `true`. However, if, for example, curating a file is a time consuming process, it may be useful to tag a file during the curation method and check for that tag elsewhere in the validate method. Below is an example of how one might accomplish that:

```
import curator

class MyCurator(curator.Curator):
	.
	.
	.
	def curate_file(self, file_):
		"""Curates a file by setting the field 'file.info.curated' to True"""
		file_.update_info({'curated': True})

	.
	.
	.
	def validate_file(self, file_):
		"""Checks to see if a file has already been curated"""
		return file_.info.get('curated', False)
```

As shown in the `validate_file` method, the method should return `True` if the container does not need to be curated and `False` if it does.

### Input files
There are many cases where custom curation may require the use of input files. This gear provides mechanisms to utilize _optional_ input files.

NOTES: 
1. These input files are optional, thus it is necessary to gracefully handle cases where the input files do not exist.
2. The gear  allows for the use of up to three input files.

The input files can be accessd within the curator class. The path to the input files are stored within the attribute named `input_file_<number>`.

Below is an example of a Project curation method using the first input file:
```
def curate_project(self, project):
	if self.input_file_one:
		with open(self.input_file_one, 'r') as input_file:
			for line in input_file:
				project.add_note(line)
```


