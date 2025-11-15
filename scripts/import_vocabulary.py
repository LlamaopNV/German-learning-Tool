"""
Script to import vocabulary from JSON files into the database
"""

import json
import sys
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent.parent / 'app'))

from database.db_manager import get_db
from gamification.srs import get_srs

def import_vocabulary_from_json(json_path: Path):
    """Import vocabulary from a JSON file"""
    print(f"Importing vocabulary from: {json_path}")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    db = get_db()
    srs = get_srs()

    cefr_level = data.get('cefr_level', 'A1')
    words = data.get('words', [])

    print(f"Found {len(words)} words at {cefr_level} level")

    added = 0
    skipped = 0

    for word_data in words:
        try:
            # Add to database
            db.add_vocabulary(
                word=word_data['word'],
                translation=word_data['translation'],
                cefr_level=cefr_level,
                part_of_speech=word_data.get('part_of_speech'),
                gender=word_data.get('gender'),
                plural_form=word_data.get('plural_form'),
                example_sentence=word_data.get('example_sentence'),
                example_translation=word_data.get('example_translation'),
                source=json_path.stem
            )
            added += 1
            print(f"✓ Added: {word_data['word']}")
        except Exception as e:
            skipped += 1
            print(f"✗ Skipped: {word_data['word']} ({e})")

    print(f"\nImport complete!")
    print(f"Added: {added} words")
    print(f"Skipped: {skipped} words (likely already in database)")

    return added, skipped


def import_all_vocabulary():
    """Import all vocabulary JSON files from content/vocabulary/"""
    vocab_dir = Path(__file__).parent.parent / 'content' / 'vocabulary'

    if not vocab_dir.exists():
        print(f"Vocabulary directory not found: {vocab_dir}")
        return

    json_files = list(vocab_dir.glob('*.json'))

    if not json_files:
        print("No vocabulary JSON files found!")
        return

    print(f"Found {len(json_files)} vocabulary file(s)\n")

    total_added = 0
    total_skipped = 0

    for json_file in json_files:
        added, skipped = import_vocabulary_from_json(json_file)
        total_added += added
        total_skipped += skipped
        print("-" * 50)

    print(f"\n=== TOTAL ===")
    print(f"Added: {total_added} words")
    print(f"Skipped: {total_skipped} words")


if __name__ == "__main__":
    import_all_vocabulary()
