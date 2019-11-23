Proposal
================

## Motivation and Purpose

Today we have men and women working together in many fields, in offices, hospitals or field work. This was not the same a few decades ago. In the past there was a time when some jobs were male dominated, and females were reluctant to join those sectors. However, with time women broke many social norms and entered almost all the sectors. Also, there are sectors in which women never performed earlier, but once they entered that sector, those sectors became female dominated. Moreover, In order to see this change, we are creating this app which will show how technology, or the needs of society led to change in popularity of different jobs and how these sectors changed for men and women.

## Dataset

Our app will visualize the `Jobs` data from the `vega-datasets` python package. We will be visualizing a dataset containing 7500 observations. This dataset contains 5 variables. The column (`job`) specifies the jobs represented in the dataset, which are 250 jobs. Two genders have been considered; men and women and listed in the column (`sex`). The data was collected in 2001, for the years from 1850 till 2000 represented in a 10-year time step in a column (`year`). The reported number of employments for each gender is represented in the (`count`) column. A percentage of the count of employment of a job over the total count of employment of all the jobs for a specific decade is showed in a column (`perc`). We will analyze the top 10 highest occupied jobs by men as well as all the jobs in the dataset as a whole. 


## Research Questions

- What are the top 10 highest occupied jobs by men?
- What is the trend of the total count of each job over the years?
- What is the trend of the total job count between males and females of each job overtime?
- What is the proportion of total women and men workers overtime?

### Usage scenarios:

Katherine is a job analyzer and occupation researcher who is interested to know the trend of the total number of male dominated jobs overtime, especially in the past ten decades. She wants to be able to [explore] a dataset in order to [compare] the trend of the total job count between different occupations. She is also eager to [identify] and [report] the differences of the total job count between males and females of a particular job overtime. It might also be helpful if Katherine can [find out] how the proportion of total female and male workers change over the period. When Katherine clicks into the “Job Analyzer app”, she will see some of the most popular jobs during 1850 to 2000 in the “Job Count” tab. The total number of workers by occupation overtime are presented as a heatmap so that she can see which jobs are more popular than others. Katherine could also see the actual total count of any sex according to a certain job in a specific year by putting her mouse at a certain section of the heatmap. Moreover, she will see a double bar graph showing the selected job, year and total count by sex. The bars change as she moves her mouse to a different section on the heatmap. If she wants to [examine] a particular job, she can click on “Job Trend” tab to see the differences between the female and male counts overtime by using the single-choice dropdown menu. If Katherine is curious about the proportion of female and male workers overtime, she can go to “Gender Ratio” tab to visualize the bar plots and click on an individual bar to see the actual percentage of a certain year of a selected gender. Katherine might notice that the number of women workers increased overtime to almost 50%. From the first tab, she will see that some jobs disappeared while others emerged in later years. This triggers her curiosity to know about the reasons behind this and decides to continue her research on the future change of the job market. From the second tab, Katherine predicts the dominance of a specific gender for certain jobs in the future. Additionally, from the third tab, she hypothesizes that the proportion of women workers will stay stable for the next few decades.  
