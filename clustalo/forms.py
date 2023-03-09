from django import forms
import re
import os

class SequencesForm(forms.Form):
    sequences = forms.CharField(widget=forms.Textarea(\
        attrs={'placeholder': 'Input your sequences here.\n Example:\n>PROTEIN_ID_1\nSequence 1\n>PROTEIN_ID_2\n Sequence 2\n>PROTEIN_ID_3\nSequence 3'}), \
        label='Sequences')
    format_options = forms.ChoiceField(
        label='Format',
        choices=[
            ('fa', 'Fasta'),
            ('clu', 'Clustal'),
            ('msf', 'Msf'),
            ('phy', 'Phylip'),
            ('selex', 'Selex'),
            ('st', 'Stockholm'),
            ('vie', 'Vienna')
        ],
        widget=forms.Select
    )

    def clean_sequences(self):
        data = self.cleaned_data['sequences']
        lines = data.split('\n')
        for i, line in enumerate(lines):
            # Check if this is the first line and if it starts with a ">"
            if i == 0 and not line.startswith('>'):
                raise forms.ValidationError(f"Invalid sequence format. Please enter the sequences in Fasta format.")
            # Check if this is a header line
            if line.startswith('>'):
                # Check if the ID is in the correct format
                if not re.match('^>[A-Z0-9]+\n?$', line.strip()):
                    raise forms.ValidationError(f"Invalid sequence header format on line {i+1}. Please enter the sequences in Fasta format.")
            # Check if this is a sequence line
            else:
                # Check if the sequence is in the correct format
                if not re.match('^[A-Za-z\n]+$', line.strip()):
                    raise forms.ValidationError(f"Invalid sequence format on line {i+1}. Please enter the sequences in Fasta format.")
        return data
    

class uniprotIdForm(forms.Form):
    uniprot_id = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Input your UniProtIDs\nExample:\nP01308\nP67970\nP01321'}), label='UniProt IDs')
    format_options = forms.ChoiceField(
        label='Format',
        choices=[
            ('fa', 'Fasta'),
            ('clu', 'Clustal'),
            ('msf', 'Msf'),
            ('phy', 'Phylip'),
            ('selex', 'Selex'),
            ('st', 'Stockholm'),
            ('vie', 'Vienna')
        ],
        widget=forms.Select
    )

    def clean_uniprot_id(self):
        data = self.cleaned_data['uniprot_id']
        lines = data.split('\n')
        errors = []
        for line in lines:
            if not re.match('^([A-Z0-9]{6})$', line.strip()):
                errors.append(forms.ValidationError("The UniProt ID format is incorrect. Please enter one UniProt ID per line.", code='invalid'))
        if errors:
            raise forms.ValidationError('Invalid format, please check the input', params={'errors': errors})
        return data


class FileUploadForm(forms.Form):
    file = forms.FileField()
    format_options = forms.ChoiceField(
        label='Format',
        choices=[
            ('fa', 'Fasta'),
            ('clu', 'Clustal'),
            ('msf', 'Msf'),
            ('phy', 'Phylip'),
            ('selex', 'Selex'),
            ('st', 'Stockholm'),
            ('vie', 'Vienna')
        ],
        widget=forms.Select
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        filename = file.name
        extension = os.path.splitext(filename)[1][1:].lower()

        # Check if the extension of the file is in the correct format
        if extension not in ['txt','fa','fasta','clu', 'msf', 'phy', 'selex', 'st', 'vie']:
            raise forms.ValidationError("File format is not supported.")

        # Check if the sequence format is correct
        if extension in ['fa', 'fasta']:
            # Read the contents of the file
            contents = file.read().decode('utf-8')
            lines = contents.split('\n')
            for i, line in enumerate(lines):
                # Check if this is the first line and if it starts with a ">"
                if i == 0 and not line.startswith('>'):
                    raise forms.ValidationError(f"Invalid sequence format. Please enter the sequences in Fasta format.")
                # Check if this is a header line
                if line.startswith('>'):
                    # Check if the ID is in the correct format
                    if not re.match('^>[A-Z0-9]+\n?$', line.strip()):
                        raise forms.ValidationError(f"Invalid sequence header format on line {i+1}. Please enter the sequences in Fasta format.")
                # Check if this is a sequence line
                else:
                    # Check if the sequence is in the correct format
                    if not re.match('^[A-Za-z\n]+$', line.strip()):
                        raise forms.ValidationError(f"Invalid sequence format on line {i+1}. Please enter the sequences in Fasta format.")
        return file
