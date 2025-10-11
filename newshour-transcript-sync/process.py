"""
Script to convert CADET-based subtitle/caption timing sync annotation (in srt format)
into a more machine-friendly tsv files.

the input looks like this:
'''
1
00:02:05,570 --> 00:02:08,570
Good evening. I'm Jim Lehrer. On the NewsHour tonight coverage
'''

the output looks like this:
'''
start	end	alignment-start	alignment-end
00:02:05.570	00:02:08.570	0	52

In doing so, the script also replaces the underlying text in the CADET srt files with the gold transcript text.
'''


"""
import pathlib
import shutil
import re
from collections import Counter

import pysrt
import argparse
from tqdm import tqdm


def tokenize(text):
    """
    Splits text into words and punctuation tokens, including their spans.
    Returns a list of tuples: (token, start_char, end_char)
    """
    return [(m.group(0), m.start(), m.end()) for m in re.finditer(r'\w+|[^\s\w]', text)]


def analyze_diff(hypothesis_tokens, reference_tokens):
    """
    Calculates WER, top errors, and alignment using Levenshtein distance.
    Works with tokens as tuples (text, start, end).
    """
    # Initialize DP matrix
    dp = [[(0, 0, 0, 0)] * (len(hypothesis_tokens) + 1) for _ in range(len(reference_tokens) + 1)]

    for i in range(len(reference_tokens) + 1):
        dp[i][0] = (i, 0, i, 0)  # Deletions
    for j in range(len(hypothesis_tokens) + 1):
        dp[0][j] = (j, j, 0, 0)  # Insertions

    for i in range(1, len(reference_tokens) + 1):
        for j in range(1, len(hypothesis_tokens) + 1):
            cost = 0 if reference_tokens[i - 1][0] == hypothesis_tokens[j - 1][0] else 1
            del_cost = dp[i - 1][j][0] + 1
            ins_cost = dp[i][j - 1][0] + 1
            sub_cost = dp[i - 1][j - 1][0] + cost

            if sub_cost <= del_cost and sub_cost <= ins_cost:
                s, i_c, d_c = (dp[i-1][j-1][1], dp[i-1][j-1][2], dp[i-1][j-1][3])
                if cost:
                    s += 1
                dp[i][j] = (sub_cost, s, i_c, d_c)
            elif del_cost < sub_cost and del_cost < ins_cost:
                s, i_c, d_c = (dp[i-1][j][1], dp[i-1][j][2], dp[i-1][j][3] + 1)
                dp[i][j] = (del_cost, s, i_c, d_c)
            else:
                s, i_c, d_c = (dp[i][j-1][1], dp[i][j-1][2] + 1, dp[i][j-1][3])
                dp[i][j] = (ins_cost, s, i_c, d_c)

    # Backtrack to find alignment and errors
    i, j = len(reference_tokens), len(hypothesis_tokens)
    alignment = []
    substitutions = Counter()
    insertions = Counter()
    deletions = Counter()
    
    s_count, i_count, d_count = dp[i][j][1], dp[i][j][2], dp[i][j][3]

    while i > 0 or j > 0:
        ref_token_tuple = reference_tokens[i - 1] if i > 0 else ('', -1, -1)
        hyp_token_tuple = hypothesis_tokens[j - 1] if j > 0 else ('', -1, -1)

        if i > 0 and j > 0 and ref_token_tuple[0] == hyp_token_tuple[0]:
            alignment.append(('equal', hyp_token_tuple, ref_token_tuple))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i-1][j-1][0] <= dp[i-1][j][0] and dp[i-1][j-1][0] <= dp[i][j-1][0]:
            alignment.append(('substitution', hyp_token_tuple, ref_token_tuple))
            substitutions[(ref_token_tuple[0], hyp_token_tuple[0])] += 1
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or dp[i-1][j][0] <= dp[i][j-1][0]):
            alignment.append(('deletion', ('', -1, -1), ref_token_tuple))
            deletions[ref_token_tuple[0]] += 1
            i -= 1
        elif j > 0 and (i == 0 or dp[i][j-1][0] < dp[i-1][j][0]):
            alignment.append(('insertion', hyp_token_tuple, ('', -1, -1)))
            insertions[hyp_token_tuple[0]] += 1
            j -= 1

    alignment.reverse()
    
    wer = (s_count + i_count + d_count) / len(reference_tokens) if reference_tokens else 0

    return {
        'wer': wer,
        'substitutions': s_count,
        'insertions': i_count,
        'deletions': d_count,
        'top_substitution': substitutions.most_common(1)[0][0] if substitutions else None,
        'top_insertion': insertions.most_common(1)[0][0] if insertions else None,
        'top_deletion': deletions.most_common(1)[0][0] if deletions else None,
    }, alignment


def generate_html_report(metrics, alignment, output_filename):
    """
    Generates an HTML report with metrics and a diff table.
    """
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('<html><head><style>')
        f.write('table { border-collapse: collapse; width: 100%; }')
        f.write('th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }')
        f.write('.correct { background-color: #ffffff; }')
        f.write('.insertion { background-color: #ddffdd; }')
        f.write('.deletion { background-color: #ffdddd; }')
        f.write('.substitution { background-color: #fff8dc; }')
        f.write('</style></head><body>')
        
        f.write('<h1>Comparison Report</h1>')
        f.write(f"<h2>Overall WER Score: {metrics['wer']:.2%}</h2>")
        f.write('<ul>')
        f.write(f"<li><b>Top Deletion:</b> {metrics['top_deletion']}</li>")
        f.write(f"<li><b>Top Insertion:</b> {metrics['top_insertion']}</li>")
        if metrics['top_substitution']:
            f.write(f"<li><b>Top Substitution:</b> {metrics['top_substitution'][0]} -> {metrics['top_substitution'][1]}</li>")
        else:
            f.write(f"<li><b>Top Substitution:</b> None</li>")
        f.write('</ul>')

        f.write('<table>')
        f.write('<tr><th>SRT (Hypothesis)</th><th>TXT (Reference)</th><th>Ref Start</th><th>Ref End</th></tr>')
        for op, hyp_tuple, ref_tuple in alignment:
            hyp_text = hyp_tuple[0]
            ref_text = ref_tuple[0]
            ref_start = ref_tuple[1] if ref_tuple[1] != -1 else ""
            ref_end = ref_tuple[2] if ref_tuple[2] != -1 else ""
            
            f.write(f'<tr>')
            if op == 'equal':
                f.write(f'<td class="correct">{hyp_text}</td>')
                f.write(f'<td class="correct">{ref_text}</td>')
                f.write(f'<td class="correct">{ref_start}</td>')
                f.write(f'<td class="correct">{ref_end}</td>')
            elif op == 'insertion':
                f.write(f'<td class="insertion">{hyp_text}</td>')
                f.write(f'<td class="insertion"></td>')
                f.write(f'<td class="insertion"></td>')
                f.write(f'<td class="insertion"></td>')
            elif op == 'deletion':
                f.write(f'<td class="deletion"></td>')
                f.write(f'<td class="deletion">{ref_text}</td>')
                f.write(f'<td class="deletion">{ref_start}</td>')
                f.write(f'<td class="deletion">{ref_end}</td>')
            elif op == 'substitution':
                f.write(f'<td class="substitution">{hyp_text}</td>')
                f.write(f'<td class="substitution">{ref_text}</td>')
                f.write(f'<td class="substitution">{ref_start}</td>')
                f.write(f'<td class="substitution">{ref_end}</td>')
            f.write('</tr>')
        f.write('</table>')
        f.write('</body></html>')


def srt_to_tsv(srt_filename, gold_transcript_filename, tsv_filename, generate_html=False):
    """
    Given a srt file and its corresponding gold transcript file,
    replace the srt text with the gold transcript corresponding texts
    and output it to the given tsv file.
    Optionally generates an HTML comparison report.
    """
    subs = pysrt.open(srt_filename, encoding='utf-8')
    
    hypothesis_tokens_with_source = []
    for sub in subs:
        # We don't need positional data for hypothesis, just text and source sub
        sub_tokens = [t[0] for t in tokenize(sub.text.replace('\n', ' '))]
        for token in sub_tokens:
            hypothesis_tokens_with_source.append((token, sub.index))
    
    hypothesis_tokens = [(item[0], -1, -1) for item in hypothesis_tokens_with_source] # Add dummy span

    with open(gold_transcript_filename, 'r', encoding='utf-8') as f:
        gold_content = f.read()
    reference_text = gold_content.strip()
    reference_tokens = tokenize(reference_text) # These have real spans

    metrics, alignment = analyze_diff(hypothesis_tokens, reference_tokens)

    # Reconstruct subtitle text from alignment
    new_sub_texts = {sub.index: [] for sub in subs}
    hyp_token_idx = 0
    
    for op, hyp_token_tuple, ref_token_tuple in alignment:
        if op == 'equal' or op == 'substitution':
            if hyp_token_idx < len(hypothesis_tokens_with_source):
                sub_index = hypothesis_tokens_with_source[hyp_token_idx][1]
                new_sub_texts[sub_index].append(ref_token_tuple)
                hyp_token_idx += 1
        elif op == 'deletion':
            # Heuristic: place deleted (gold-only) tokens in the same subtitle
            # as the token that came before them.
            if hyp_token_idx > 0:
                prev_sub_index = hypothesis_tokens_with_source[hyp_token_idx - 1][1]
                new_sub_texts[prev_sub_index].append(ref_token_tuple)
            elif subs:
                new_sub_texts[subs[0].index].append(ref_token_tuple)
        elif op == 'insertion':
            # An SRT token is ignored, advance the hypothesis pointer.
            if hyp_token_idx < len(hypothesis_tokens_with_source):
                hyp_token_idx += 1

    # Write TSV file using original text slices
    with open(tsv_filename, 'w', encoding='utf-8') as out:
        out.write("start\tend\talignment-start\talignment-end\n")
        for sub in subs:
            start = str(sub.start).replace(',', '.')
            end = str(sub.end).replace(',', '.')
            
            token_info_list = new_sub_texts[sub.index]
            if token_info_list:
                # Get the start and end character offsets from the token tuples
                start_char = token_info_list[0][1]
                end_char = token_info_list[-1][2]
            else:
                start_char = ""
                end_char = ""
            out.write(f"{start}\t{end}\t{start_char}\t{end_char}\n")

    # Generate HTML report if requested
    if generate_html:
        html_filename = f"diff_{pathlib.Path(srt_filename).stem}.html"
        generate_html_report(metrics, alignment, html_filename)


def process(source_directory, destination_directory, gold_transcript_directory, generate_html=False):
    print(f"Processing directory: {source_directory}")
    srt_files = list(source_directory.glob('*.srt'))
    for source_path in tqdm(srt_files, desc=f"Processing {source_directory.name}"):
        gold_transcript_path = source_path.name.split(".")[0]+"-transcript.txt"
        gold_txt_path = gold_transcript_directory / gold_transcript_path
        if gold_txt_path.exists():
            dest_path = destination_directory / source_path.with_suffix('.tsv').name
            srt_to_tsv(source_path, gold_txt_path, dest_path, generate_html)
        else:
            print(source_path, "has no corresponding gold transcript in", gold_transcript_directory)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--gold-txt-dir', required=True,
                            help='the directory to the gold transcripts which should be txt files.')
    arg_parser.add_argument('--html', action='store_true',
                            help='Generate an HTML comparison report in the current directory.')
    parsed_args = arg_parser.parse_args()
    
    task_dir = pathlib.Path(__file__).parent
    golds_dir = task_dir / 'golds'

    # delete golds directory if it exists
    shutil.rmtree(golds_dir, ignore_errors=True)
    # then start from clean slate
    golds_dir.mkdir(exist_ok=True)

    # find all directories starts with six digits and a dash
    batch_dirs = list(task_dir.glob('[0-9][0-9][0-9][0-9][0-9][0-9]-*'))
    for batch_dir in batch_dirs:
        process(batch_dir, golds_dir, pathlib.Path(parsed_args.gold_txt_dir), parsed_args.html)

