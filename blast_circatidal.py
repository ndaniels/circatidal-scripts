# ## Steps:
# 1. read .fasta file
# 	create dictionary:
# 		key = cycID
# 		value = genomic sequence

# 2. read .csv
# 	for each cycID
# 		identify in .fasta file
# 		BLAST in genbank


from Bio import SeqIO
import Bio.Blast.NCBIWWW as blast

import sys
import re
import csv

fasta_file = sys.argv[1]
csv_file = sys.argv[2]

sequences = {}
#read fasta file
for seq_record in SeqIO.parse(fasta_file, "fasta"):
    # seq_id_long = re.search(r'^[^\s]+', seq_record.id).group(0)
    seq_id = re.search(r'^[^_]+_[^_]+_[^_]+_[^_]+', seq_record.id).group(0)
    sequences[seq_id] = seq_record.seq
    # print(seq_id)

# read csv file
seqs_to_blast = {}
with open(csv_file) as csv_contents:
    csv_reader = csv.reader(csv_contents)
    counter = 0
    for row in csv_reader:
        cyc_id = row[0]
        # print(cyc_id)
        if cyc_id in sequences.keys():
            seqs_to_blast[cyc_id] = sequences[cyc_id]
            # print(f'>{cyc_id}')
            # print(f'{sequences[cyc_id]}')
            counter += 1
print(f'querying {counter} sequences')

n = 0
for seqid in seqs_to_blast.keys():
    n += 1
    sys.stderr.write(f'{n}..')
    sys.stderr.flush()
    # print(f'>{seqid}')
    # print(seqs_to_blast[seqid])
    # alternatively, we may want blastn, nt (or nt_euk)
    result_stream = blast.qblast("blastn", "nt_euk", seqs_to_blast[seqid], format_type="Text")
    # result_stream = blast.qblast("blastx", "swissprot", seqs_to_blast[seqid], format_type="Text")
    result = result_stream.read()
    with open(f'{seqid}_out.txt', 'w') as save_file:
        save_file.write(result)
