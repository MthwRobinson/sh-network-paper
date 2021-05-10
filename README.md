## About the paper

Title: Network Structure and Requirements Crowdsourcing for OSS Projects

Autors: M. Robinson, S. Sarkani and M. Mazzuchi

Affiliation: School of Engineering and Applied Science, George Washington University

Abstract: Crowdsourcing system requirements enables project managers to elicit feedback from a broader range of stakeholders. The advantages of crowdsourcing include a higher volume of requirements reflecting a more comprehensive array of use cases and a more engaged and committed user base. Researchers cite the inability of project teams to effectively manage an increasing volume of system requirements as a possible drawback. This paper analyzes a data set consisting of project management artifacts from 562 open source software (OSS) projects to determine how OSS project performance varies as the share of crowdsourced requirements increases using six measures of effectiveness: requirement close-out time, requirement response time, average comment activity, the average number of requirements per crowd member, the average retention time for crowd members, and the total volume of requirements. Additionally, the models measure how the impact of increasing the share of crowdsourced requirements changes with stakeholder network structure. The analysis shows that stakeholder network structure impacts OSS performance outcomes, and that the effect changes with the share of crowdsourced requirements. OSS projects with more concentrated stakeholder networks perform the best. The results indicate that requirements crowdsourcing faces diminishing marginal returns. OSS projects that crowdsource more than 70\% of their requirements benefit more from implementing processes to organize and prioritize existing requirements than from incentivizing the crowd to generate additional requirements. Analysis in the paper also suggests that OSS projects could benefit from employing CrowdRE techniques and assigning dedicated community managers to more effectively channel input from the crowd.

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


