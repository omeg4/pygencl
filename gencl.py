import os
import subprocess as sp
from datetime import datetime
import string

homedr = os.getenv('HOME')
gendir = 'autogen/'
pdfdir = homedr + '/datadrop/Dropbox/jobapps/covletts' # Modify as necessary
cldict = { 'ds' : 'bash-datsci.tex', 'fin' : 'bash-finance.tex', 'example' : 'template-example.tex' } # Modify as necessary

def fnameformat(inarg):
    '''
    Process the STDIN arguments and generate a shortened string for use in file name
    INPUT: script argument from STDIN for company name/job title
    OUTPUT: CamelCaseArgum with punctuation removed and each word in the string shortened to 5 chars at most.
    '''
    fnamepart = []

    # for either a job title or company name, ensure Title Case and split each word
    for s in inarg.title().split():

        # Strip punctuation (if necessary)
        s = s.translate(str.maketrans("", "", string.punctuation))

        # Shorten each Word (if necessary)
        if len(s) > 5:
            s = s[:5]

        # Put each processed word into a list
        fnamepart.append(s)

    # After processing each word from the input argument, join() the elements in the list
    return ''.join(fnamepart)

def gencl(cltdkey, compname, jobtitle):
    '''
    -- Open the template .tex file
    -- replace the lines that define the \company and \job commands
    -- save as new .tex file w/ a formatted name
    -- call `pdflatex` on the newly generated file
    -- copy the resulting .pdf to dropbox

    INPUTS:
        cltdkey: (cover letter template dict key) STDIN arg of dict key specifying either the data science or finance FL
        compname: STDIN arg of company name
        jobtitle: STDIN arg of job title
    OUTPUTS:
        True (if everything worked)
        [some error string] (if an exception was caught)
    '''

    # Lines of Latex code that define the company name and job title.
    # Easier to do it this way than to try to string.format() a tex file with a million curly braces
    cncommand = '\\newcommand{\\company}{%COMPNAME%\\ }'.replace('%COMPNAME%', compname)
    jtcommand = '\\newcommand{\\job}{%JOBTITLE%}'.replace('%JOBTITLE%', jobtitle)
    with open(cldict[cltdkey], 'r') as fl:
        texfile = fl.read()
    texfile = texfile.replace('%COMPNAMECOMMAND%', cncommand).replace('%JOBTITLECOMMAND%', jtcommand)

    # Generate a unique file name, something like {date}_{CompName}_{JobTitle}
    fname = datetime.now().strftime('%m-%d') + '_' + fnameformat(compname) + '_' + fnameformat(jobtitle)

    # Save the new tex file:
    # Also, we're gonna stuff all the .tex files and such in a subdir. the dir for generated files is `gendir = 'autogen/'`
    with open(gendir + fname + '.tex', 'w') as f:
        f.write(texfile)

    # call `pdflatex` on the newly saved file
    try:
        sp.run(['pdflatex', fname + '.tex'], cwd=gendir, check=True)
    except:
        return 'something went wrong during compilation!'

    # copy the pdf to dropbox
    try:
        sp.run(['cp', fname + '.pdf', pdfdir + fname + '.pdf'], cwd=gendir, check=True)
    except:
        return 'something went wrong when moving the PDF!'

    return True

if __name__ == '__main__':
    cname = input('Enter company name: ')
    title = input('Enter job title: ')
    cldictkey = input('Cover letter dict key? cldict = ' + str(cldict) + '\n>>')
    gencl(cldictkey, cname, title)
