# Snippet Searchers Project Proposal

## What are the names and NetIDs of all your team members? Who is the captain?

### Team Roster
* Mark Bauer  (Team Captain) - markab5@illinois.edu
* Cameron Keenan- keenan5@illinois.edu
* Ben Carman - bac8@illinois.edu
* Armaan Kohli - kohli9@illinois.edu

## What is your free topic? Please give a detailed description. What is the task? Why is it important or interesting? What is your planned approach? What tools, systems or datasets are involved? What is the expected outcome? How are you going to evaluate your work?

Our topic is to solve the problem of searching through commands/scripts you have run/collected for a web browser’s javascript console and python juypter notebooks.  All of our team members heavily use console/jupyter commands, and we had the idea of finding a better way to find that command we ran 5-10 commands ago (or maybe it was last week… if we remembered, we would need this tool less). We all are working on a similar system, so we also want commands run by one individual to be searchable by others. 

The approach we are currently planning on is to create a chrome extension that forwards your console command history, and/or lets you select code snippets for upload, then leverages a custom tokenizer to search the snippets/commands.  

For our dataset, we will be providing the code snippet dataset to be searched.  We intend on leveraging AWS for our cloud services (Dynamo/RDS/opensearch for our database etc.).  We will be using Chrome as our base web browser to extend.  

We will evaluate our work using mean average precision, in addition to our own  anecdotal usage experience.  We will also collect statistics, both on how often users upload snippets and by how many snippets users reuse over time relative to the number of searches. 

# Which programming language do you plan to use?
Python and Javascript (primarily javascript but python as need for parsing python snippets)

# Please justify that the workload of your topic is at least 20*N hours, N being the total number of students in your team. You may list the main tasks to be completed, and the estimated time cost for each task.
With four team members, we will be targeting at or slightly above 80 hours of work.  Tasks include:
* Identifying and/or creating (then tuning) a tokenizer that works well for searching javascript and python code: 20hrs
* Evaluating stemming to see if it adds value in the relatively more literal world of searching code: 5hrs
* Access control (logging in, searching only your documents): 15hrs
* Create base chrome extension: 10hrs
* Document upload and download / Pulling in console history directly from Chrome if possible: 5hrs
* Manually uploading workspace snippets: 5hrs
* Downloading snippets identified by search: 5hrs
* Setup and configure OpenSearch: 5hrs
* Collecting user behavior statistics for evaluation: 10hr
