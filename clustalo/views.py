from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
import subprocess
import datetime
import requests
from django.core.mail import send_mail
from django.conf import settings


#############################################################################
def list_of_ids_to_list_id_seq_with_API_CALL(list_of_ids):
    list_a, errors_list = [], []
    # the function takes a list of identifiers as the input
    for id in list_of_ids:
        if id != '':
        # calling an API to retrieve sequences associated with the IDs
            response = requests.get(f'https://rest.uniprot.org/uniprotkb/{id}.fasta')
            if response.status_code == 200:
                response_text_list = response.text.split('\n')
            # returning two lists as the output
                ident = [elem for elem in response_text_list if '>' in elem][0]
                seq = ''.join([elem for elem in response_text_list if '>' not in elem])
                list_a.extend([ident, seq])
            else:
            # returning a list of errors
                errors_list.append(id)
    return list_a, errors_list
#####################################################

def result_std_out_to_dic(result_stdout):
# the input string contains the output of a sequence alignment tool
    out_list = result_stdout.split('\n')
    ident, aln, n, dict_ident_aln = '', '', 0, {}
# loop through the list of lines to check if it contains ">"
    for elem in out_list:
        if '>' not in elem:
        # append to the 'aln' string
            aln += elem
        else:
            if n > 0:
        # add the previous ID and aligned sequence to the dictionary
                dict_ident_aln.update({ident:aln})
            n, ident, aln = 1, elem, ''
        # update the ident variable with the current sequence ID
        dict_ident_aln.update({ident:aln})
    return dict_ident_aln
#####################################################

def dict_to_html_with_errors(get_dict, errors_list):
    items_html = ''.join(f'<p>{k}  {v}</p>' for k, v in get_dict.items())
    errors_html = f"<p>The errors were:</p> {'; '.join(errors_list)}" if errors_list else ''
    return f"<html><body>{items_html}{errors_html}</body></html>"

######################################################

# used to convert the Clustal Omega result in the 'result_stdout' string into a html format

def result_stdout_to_html_as_clustal(result_stdout, errors_list=[]):
    # converting into a html format
    lines_html = '<br>'.join(result_stdout.split('\n'))
    # check for errors and add them if they exist
    errors_html = f"<p>The errors were:</p> {'<br>'.join(errors_list)}" if errors_list else ''
    return lines_html + errors_html


#######################################################


def html_send_to_txt(html_send):
    output = html_send.replace('<br>', '%0A')
    output = output.replace('<p>', '%0A')
    output = output.replace('</p>', '%0A')
    return output

#######################################################

def success_return_html(request, input_for_clustal, errors_list=[], format='clu'):
    result = subprocess.run(["clustalo", "-i", "-", f"--outfmt={format}"], input=input_for_clustal, capture_output=True, text=True)
    html_send = result_stdout_to_html_as_clustal(result.stdout, errors_list)
    output_txt = html_send_to_txt(html_send)
    html_send = html_send.replace(' ', '&nbsp;')
    stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return render(request, 'clustalo/output.html', {'html_send': html_send, 'stamp': stamp, 'output_txt': output_txt, 'format': format})

#######################################################

# rendering the main page of a web application

def get_aln(request):
    # initializing forms
    form_uniprotIdForm = uniprotIdForm()
    form_SequencesForm = SequencesForm()
    form_FileUploadForm = FileUploadForm()
    # check if the requested method is POST
    if request.method == 'POST':

        if 'form_uniprotIdForm' in request.POST:
            # retrieve UniProt IDs
            form_uniprotIdForm = uniprotIdForm(request.POST)

            if form_uniprotIdForm.is_valid():
                list_of_ids = str(form_uniprotIdForm.cleaned_data['uniprot_id']).split('\r\n')
                (list_a, errors_list) = list_of_ids_to_list_id_seq_with_API_CALL(list_of_ids)
                sequences_fromUniprotIDs = '\n'.join(list_a)
                format = str(form_uniprotIdForm.cleaned_data['format_options'])
                print(format)
                return success_return_html(request, sequences_fromUniprotIDs, errors_list, format=format)

        if 'form_SequencesForm' in request.POST:
            # retrieve the entered sequences
            form_SequencesForm = SequencesForm(request.POST)

            if form_SequencesForm.is_valid():
                all_inserted_sequences = str(form_SequencesForm.cleaned_data['sequences'])
                format = str(form_SequencesForm.cleaned_data['format_options'])
                return success_return_html(request, all_inserted_sequences, errors_list=[], format=format)

        if 'file' in request.POST:
            # retrieve the uploaded file
            form_FileUploadForm = FileUploadForm(request.POST, request.FILES)
            file = request.FILES['file']

            if form_FileUploadForm.is_valid():
                file = request.FILES['file']
                format = str(form_FileUploadForm.cleaned_data['format_options'])
                content = file.read().decode('utf-8')
                return success_return_html(request, content, errors_list=[], format=format)
                
    context = {'form_uniprotIdForm': form_uniprotIdForm, 'form_SequencesForm':form_SequencesForm, 'form_FileUploadForm':form_FileUploadForm}
    return render(request, 'clustalo/index.html', context)

#######################################################

def send_email(request):
    if request.method == 'POST':
        email_to = request.POST['email']
        output = request.POST['output']
        send_mail(
            'CLUSTALO Output',
            output,
            settings.DEFAULT_FROM_EMAIL,
            [email_to],
            fail_silently=False,
        )
        return render(request, 'success.html')
    else:
        return render(request, 'error.html')



import subprocess

def upload_files():
    # change the directory to the location of the files you want to upload
    directory = '/Users/MARCO/Desktop/dbwnmgvise'
    # run the scp command to upload the files to the remote server
    subprocess.run(['scp', '-r', f'{directory}/*', 'u217741@formacio.bq.ub.edu:public_html'])
