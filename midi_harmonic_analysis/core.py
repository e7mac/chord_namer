import music21

def filter_weighted_duration(notes, threshold=0.25, cumulative_threshold=1.0):
    """Filters out short notes unless their cumulative duration exceeds a threshold."""
    filtered_notes = []
    short_notes = []
    
    for note in notes:
        if note.quarterLength > threshold:  # Longer notes are directly included
            if sum(n.quarterLength for n in short_notes) >= cumulative_threshold:
                filtered_notes.extend(short_notes)  # Include short notes if cumulative duration is enough
            short_notes = []  # Reset short notes collection
            filtered_notes.append(note)
        else:
            short_notes.append(note)
    
    # Check the last batch of short notes
    if sum(n.quarterLength for n in short_notes) >= cumulative_threshold:
        filtered_notes.extend(short_notes)  # Include the group of short notes if cumulative duration is enough

def remove_unpitched_parts(score):
    """Remove unpitched parts from the score to avoid issues with chordify."""
    parts_to_keep = []
    
    for part in score.parts:
        # Check if the part contains any pitched notes
        contains_pitched_notes = any(isinstance(element, music21.note.Note) and not isinstance(element, music21.note.Unpitched) for element in part.flatten().notes)
        
        if contains_pitched_notes:
            parts_to_keep.append(part)
    
    return music21.stream.Score(parts_to_keep)

def get_bass_note_on_downbeat(measure):
    """Return the lowest note or pitch occurring on the downbeat (beat 1) of a measure."""
    downbeat_elements = [element for element in measure.notes if element.offset == 0.0]
    if downbeat_elements:
        lowest_pitch = None
        
        # Find the lowest pitch, whether the element is a Note or Chord
        for element in downbeat_elements:
            if isinstance(element, music21.note.Note):
                if lowest_pitch is None or element.pitch < lowest_pitch:
                    lowest_pitch = element.pitch
            elif isinstance(element, music21.chord.Chord):
                # Get the lowest pitch in the chord
                chord_lowest_pitch = min(element.pitches, key=lambda p: p.midi)
                if lowest_pitch is None or chord_lowest_pitch < lowest_pitch:
                    lowest_pitch = chord_lowest_pitch
        
        return lowest_pitch
    return None

def filter_notes_below_bass_floor(notes_in_measure, bass_floor):
    """Filter out any notes that are lower than the bass note on the downbeat (bass_floor)."""
    filtered_notes = []
    
    for element in notes_in_measure:
        if element.offset == 0.0:  # Keep notes on the downbeat
            filtered_notes.append(element)
        elif isinstance(element, music21.note.Note):
            if bass_floor and element.pitch >= bass_floor:
                filtered_notes.append(element)  # Keep notes if they are higher than or equal to the downbeat bass note
        elif isinstance(element, music21.chord.Chord):
            # For chords, filter out pitches lower than the bass note on the downbeat
            pitches_above_bass = [p for p in element.pitches if bass_floor is None or p >= bass_floor]
            if pitches_above_bass:
                filtered_notes.append(music21.chord.Chord(pitches_above_bass))
    
    return filtered_notes
    

def generate_chord_symbols_from_chordify(score, threshold=0.25, cumulative_threshold=1.0):
    
    # Remove unpitched parts before chordification
    score = remove_unpitched_parts(score)
    
    # Chordify the entire score to create a harmonic reduction
    chordified_score = score.chordify()
    
    # Iterate through each measure in the chordified score
    for measure in chordified_score.getElementsByClass(music21.stream.Measure):
        notes_in_measure = []
        
        # Collect all chords/notes in the measure
        for element in measure.notes:
            if isinstance(element, music21.note.Note) or isinstance(element, music21.chord.Chord):
                notes_in_measure.append(element)

        # Get the lowest note on the downbeat (beat 1)
        bass_note_on_downbeat = get_bass_note_on_downbeat(measure)
        
        # Filter out any notes below the bass floor
        filtered_notes = filter_notes_below_bass_floor(notes_in_measure, bass_note_on_downbeat)
        
        # Apply the filter to exclude passing tones
        filtered_notes = filter_weighted_duration(filtered_notes,threshold,cumulative_threshold)

        
        if filtered_notes:
            # Create a chord from all filtered notes in the measure
            combined_chord = music21.chord.Chord(filtered_notes)

            
            try:
                # Attempt to generate a chord symbol
                chord_symbol = music21.harmony.ChordSymbol()
                chord_symbol.figure = music21.harmony.chordSymbolFigureFromChord(combined_chord)
                
                # Ensure the chord symbol has a valid root
                if not chord_symbol.root():
                    raise ValueError("Invalid root note in chord symbol.")
                
                # Insert the ChordSymbol into the measure at the beginning
                measure.insert(0, chord_symbol)
                
            except Exception as e:
                #if returning an error, try setting the root to the lowest note of the chord
                try:
                    #set lowest note on beat 1 as root of the chord
                    combined_chord.root(bass_note_on_downbeat)

                    # Attempt to generate a chord symbol
                    chord_symbol = music21.harmony.ChordSymbol()
                    chord_symbol.figure = music21.harmony.chordSymbolFigureFromChord(combined_chord)
                    
                    # Ensure the chord symbol has a valid root
                    if not chord_symbol.root():
                        raise ValueError("Invalid root note in chord symbol.")
                    
                    # Insert the ChordSymbol into the measure at the beginning
                    measure.insert(0, chord_symbol)

                except Exception as e:
                    # Skip the measure if an error occurs
                    print(f"Skipping measure {measure.number} due to error: {e}")
    
    return chordified_score


def generate_roman_numerals(score,threshold=0.25, cumulative_threshold=1.0):
    # Chordify the entire score to create a harmonic reduction
    chordified_score = score.chordify()
    
    # Determine the key signature and assume major key
    key_signature = score.analyze('key')
    if key_signature.mode == 'minor':
        key_signature = key_signature.relative

    # Iterate through each measure in the chordified score
    for measure in chordified_score.getElementsByClass(music21.stream.Measure):
        notes_in_measure = []
        
        # Collect all chords/notes in the measure
        for element in measure.notes:
            if isinstance(element, music21.note.Note) or isinstance(element, music21.chord.Chord):
                notes_in_measure.append(element)

        # Get the lowest note on the downbeat (beat 1)
        bass_note_on_downbeat = get_bass_note_on_downbeat(measure)
        
        # Filter out any notes below the bass floor
        filtered_notes = filter_notes_below_bass_floor(notes_in_measure, bass_note_on_downbeat)
        
        # Apply the filter to exclude passing tones
        filtered_notes = filter_weighted_duration(filtered_notes,threshold,cumulative_threshold)
        
        
        if filtered_notes:
            # Create a chord from all filtered notes in the measure
            combined_chord = music21.chord.Chord(filtered_notes)
            
            try:
                # Generate Roman numeral analysis based on the assumed key
                roman_numeral = music21.roman.romanNumeralFromChord(combined_chord, key_signature)
                
                # Add the Roman numeral as a lyric to the first note/chord of the measure
                if measure.notes:
                    first_element = measure.notes[0]
                    if isinstance(first_element, music21.note.Note):
                        first_element.addLyric(roman_numeral.romanNumeral)
                    elif isinstance(first_element, music21.chord.Chord):
                        first_element.addLyric(roman_numeral.romanNumeral)  # Add to the entire chord
                
            except Exception as e:
                # Skip the measure if an error occurs
                print(f"Skipping measure {measure.number} due to error: {e}")
    
    return chordified_score

def generate_chord_symbols_from_chordify_beats(score, threshold=0.25, cumulative_threshold=1.0, beats_per_segment=4):
    # Remove unpitched parts before chordification
    score = remove_unpitched_parts(score)
    
    # Chordify the entire score to create a harmonic reduction
    chordified_score = score.chordify()

    # Iterate through each measure in the chordified score
    for measure in chordified_score.getElementsByClass(music21.stream.Measure):
        measure_duration = measure.duration.quarterLength
        num_segments = int(measure_duration / beats_per_segment)

        for i in range(num_segments):
            start_offset = i * beats_per_segment
            end_offset = start_offset + beats_per_segment
            notes_in_segment = []

            # Collect notes/chords within the segment
            for element in measure.notes:
                if start_offset <= element.offset < end_offset:
                    notes_in_segment.append(element)

            # Apply the filter to exclude passing tones
            filtered_notes = filter_weighted_duration(notes_in_segment, threshold, cumulative_threshold)
            
            if filtered_notes:
                try:
                    # Create a chord from all filtered notes in the segment
                    combined_chord = music21.chord.Chord(filtered_notes)
                    
                    # Ensure the chord symbol has a valid root
                    if not combined_chord.pitches:
                        continue  # Skip empty chords
                    
                    # Attempt to generate a chord symbol
                    chord_symbol = music21.harmony.ChordSymbol()
                    chord_symbol.figure = music21.harmony.chordSymbolFigureFromChord(combined_chord)

                    # Insert the ChordSymbol into the measure at the appropriate offset
                    measure.insert(start_offset, chord_symbol)
                    
                except Exception as e:
                    # If returning an error, try setting the root to the lowest note of the chord
                    try:
                        # Set bass note as root of the chord
                        combined_chord.root(combined_chord.bass())

                        # Attempt to generate a chord symbol
                        chord_symbol = music21.harmony.ChordSymbol()
                        chord_symbol.figure = music21.harmony.chordSymbolFigureFromChord(combined_chord)

                        # Ensure the chord symbol has a valid root
                        if not combined_chord.root():
                            raise ValueError("Invalid root note in chord symbol.")
                        
                        # Insert the ChordSymbol into the measure at the appropriate offset
                        measure.insert(start_offset, chord_symbol)

                    except Exception as e:
                        # Skip the measure if an error occurs
                        print(f"Skipping segment in measure {measure.number} due to error: {e}")
    
    return chordified_score
