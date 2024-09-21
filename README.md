# midi_harmonic_analysis

midi_harmonic_analysis is a Python library for analyzing musical scores using the music21 library. It provides functionality for generating chord symbols, Roman numeral analysis, and filtering notes based on various criteria.

## Installation

You can install midi_harmonic_analysis using pip:

```
pip install midi_harmonic_analysis
```

## Usage

Here's a quick example of how to use midi_harmonic_analysis:

```python
import music21 as m21
from midi_harmonic_analysis import generate_chord_symbols_from_chordify

# Load a score
score = m21.converter.parse('path/to/your/score.xml')

# Generate chord symbols
chordified_score = generate_chord_symbols_from_chordify(score)

# Show or save the result
chordified_score.show()
```

For more detailed usage instructions and examples, please refer to the documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is not licensed for use by anyone other than the authors.
