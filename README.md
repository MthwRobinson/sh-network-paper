## About the paper

Title: Network Structure and the Effectiveness of Crowd Based Requirements Processes

Autors: M. Robinson, S. Sarkani and M. Mazzuchi

Affiliation: School of Engineering and Applied Science, George Washington University

Abstract: In recent years, researchers have argued that crowd sourcing generates better requirements by eliciting feedback from a broader range of stakeholders. Proposed benefits of crowd-based requirements process include a higher volume of requirements reflecting a broader array of use cases and a more engaged and committed user base. Researchers cite the inability of project teams to effectively manage an overwhelming volume of crowd-sourced system requirements as a possible drawback. Using a data set consisting of project management artifacts from 562 open source software projects, this paper uses generalized linear models to analyze how system performance varies as the percentage of requirements sourced from the crowd increases with respect to five measures of effectiveness: the average requirement close-out and response times, the average comment activity on requirements, the average number of issues per crowd member, and the average volume of requirements over time. Additionally, the models measure how the impact of additional crowd engagement changes with stakeholder network structure. For each measure of effectiveness except issues per crowd member, the analysis shows that the effect of increasing crowd engagement changes depending on the structure of the stakeholder network and the percentage of requirements sourced from the crowd. The results imply stakeholder networks with multiple, disjoint hubs and a low level of localized clustering absorb additional crowd engagement most effectively and suggest that systems engineers who seek to employ crowd-based requirements processes should encourage contributors to specialize and develop processes to route incoming requirements to the appropriate specialist.

## About this repo

This repo contains data, code and research notebooks that were created in support of the paper. Currently, the repo intentionally has ***no license***, meaning the code cannot be reused for any purpose without express permission from the authors. Once the paper is published, we'll add a license to allow for code reuse and modification.

## Code

### Installation

The code developed for the analysis is written in Python and requires `python>=3.6`. To install the dependencies for the research code, clone the repo and run the following command:

```
pip install -r requirements
```

## Data

### GitHub

The GitHub data set that was used for the analysis is included as `github_data.csv`. This is aggregated data that was produced by process raw data collected from the GitHub API. The full data set sourced from GitHub is too large to include in the repo. However, the authors can provide a PostgresSQL dump of the full data set on request.

### Network Plots

Plots depicting the network structure for each stakeholder network in the data set appear in the `network_plots` folder. Building the networks from scratch requires the full Postgres database which, as noted above, is too large to include the repo. However, `pickle` binaries for the stakeholde networks are included in the `network_binaries` folder. You can load and plot a network by running the following commands from the `code` directory.

```
from stakeholder_network import StakeholderNetwork

network = StakeholderNetwork(organization='alibaba', package='fastjson')
network.plot_nework()
```

A `networkx` representation of the stakeholder network is available on the `network` attribute of the `StakeholderNetwork` instance.


