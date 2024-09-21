import music21
from midi_harmonic_analysis import generate_roman_numerals

# Load the score from a MusicXML file
score = music21.converter.parse('./samples/Title_Theme_-_Ocarina_of_Time.mxl')

# Generate the chordify staff with chord symbols
chordified_score = generate_roman_numerals(score)

# Append the chordify staff to the original score
combined_score = music21.stream.Score()
for part in score.parts:
    combined_score.append(part)
combined_score.append(chordified_score)

# Force a layout update to ensure lyrics are displayed
chordified_score.makeMeasures(inPlace=True)

# music21.environment.set('musicxmlPath', '/Applications/MuseScore\ 4.app/Contents/MacOS/mscore')

chordified_score.measures(1,8).show()
chordified_score.write('musicxml', fp='output.mxl')

print("Analysis complete. Output saved as 'output.mxl'")
