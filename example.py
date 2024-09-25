import music21
import midi_harmonic_analysis

# Load the score from a MusicXML file
score = music21.converter.parse('./samples/Title_Theme_-_Ocarina_of_Time.mxl')

# # Generate the chordify staff with chord symbols
# chordified_score = midi_harmonic_analysis.generate_chord_symbols_from_chordify(score)

# # Append the chordify staff to the original score
# combined_score = music21.stream.Score()
# for part in score.parts:
#     combined_score.append(part)
# combined_score.append(chordified_score)

# # music21.environment.set('musicxmlPath', '/Applications/MuseScore\ 4.app/Contents/MacOS/mscore')

# chordified_score.write('musicxml', fp='output.mxl')
# combined_score.write('musicxml', fp='output_combined.mxl')

# print("Analysis complete. Output saved as 'output_combined.mxl'")

import base64

# Replace with the path to your MusicXML file
file_path = './samples/Title_Theme_-_Ocarina_of_Time.mxl'

with open(file_path, 'rb') as file:
    musicxml_content = file.read()
    base64_encoded = base64.b64encode(musicxml_content).decode('utf-8')
    
print(base64_encoded)
