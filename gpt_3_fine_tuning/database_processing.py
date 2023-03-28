import json


with open('../data/transcript_data.jsonl', 'r') as f, open('../data/kb_database.jsonl', 'w') as out_file:
    for line in f:
        data = json.loads(line)
        if data['status'] == 'kb_completed':
            kb_sentences = data['knowledge_base'].split('\n - ')
            for sentence in kb_sentences:
                if sentence.strip() != '':
                    # Create a new dictionary for the current knowledge base sentence
                    new_data = {
                        'transcription_date': data['transcription_date'],
                        'filename': data['filename'],
                        'status': 'kb_databased',
                        'knowledge_base': sentence.strip(),
                        # 'embedding': data['embedding'],
                    }
                    # Write the new dictionary as a JSON object to the output file
                json.dump(new_data, out_file)
                out_file.write('\n')

