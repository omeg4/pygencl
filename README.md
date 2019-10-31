It is common practice amongst job-seekers to create one or more cover letter templates, changing only the company name and job title for each new application.

But even this system requires several trivial-but-tedious steps to complete, which can disrupt the flow that one seeks to attain when applying to job after job for an extended period of time.

So, here's a little Python script that prompts the user for the company name and job title, and also allows for choosing between multiple templates.
After entering the relevant information at these prompts, the script generates a new .tex file in the subdirectory `autogen` and compiles that file with `pdflatex`.
The newly generated PDF is then be copied elsewhere on the user's system - for example a job-application-specific folder that the user accesses frequently.

For the most streamlined experience, create an alias to run the script from any directory:

> `echo " alias pygencl='cd ~/RepoPath && python3 gencl.py'" >> ~/.zshrc`

*Note*: It is important to execute `cd ~/RepoPath && python3 gencl.py`, since the script is written using relative directories, such that `gencl.py` must be executed from within `~/RepoPath`.

TODO:

	* Implement a quick setup.py script to guide new users
