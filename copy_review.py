"""Require a fresh private editorial review; never certify reader comprehension."""
from pathlib import Path
import argparse
import hashlib
import json


SOURCES = (
    'index.html', 'properties.html', 'whitepaper.md', 'devsheet.md', 'pitchdeck.json',
    'model-guide.json', 'contact-routes.json', 'project-reference.json',
    'build_publication.py', 'model_guide.py', 'contact_page.py', 'project_reference.py',
    'copy_review.py', 'assets/site.js', 'assets/contact.js', 'assets/style.css', 'assets/brand.css',
)
QUESTIONS = ('housing_offer', 'resident_decisions', 'funding', 'project_status', 'next_action')
READER_PAGES = ('index.html', 'rent-to-own.html', 'roadmap.html',
                'transparency.html', 'contact.html', 'properties.html', 'resources.html',
                'whitepaper.html', 'devsheet.html', 'pitchdeck.html', 'reference.html')


def fingerprints(root):
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in SOURCES}


def verify(root, record_path):
    """Validate review evidence and freshness, without judging its prose or answers."""
    root = root.resolve()
    record_path = Path(record_path).resolve()
    if record_path.is_relative_to(root):
        raise ValueError('Keep the copy review outside the published website directory.')
    record = json.loads(record_path.read_text())
    if record.get('schema') != 1:
        raise ValueError('Copy review needs schema 1.')
    expected = fingerprints(root)
    actual = record.get('sources', {})
    changed = [name for name, value in expected.items() if actual.get(name) != value]
    if changed:
        raise ValueError('Copy review is stale or incomplete: ' + ', '.join(changed))
    for field in ('reader', 'medium', 'prior_knowledge', 'purpose', 'scope', 'reviewer'):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError('Copy review needs ' + field + '.')
    if record.get('editorial_status') != 'reviewed':
        raise ValueError('Copy review needs a completed editorial review.')
    # Actual participant feedback is deliberately distinct and may still be pending.
    if record.get('audience_testing') not in ('pending', 'recorded_separately'):
        raise ValueError('State audience_testing as pending or recorded_separately.')
    if record['audience_testing'] == 'recorded_separately':
        evidence = Path(record.get('audience_evidence', '')).resolve()
        if not evidence.is_file() or evidence.is_relative_to(root):
            raise ValueError('Audience evidence must exist outside the published site.')
    answers = record.get('reader_questions', {})
    for question in QUESTIONS:
        item = answers.get(question, {})
        for field in ('question', 'answer', 'source_section'):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError('Missing editorial answer: ' + question + '/' + field)
    for field in ('meaning_preserved', 'claims_supported', 'medium_fit', 'internal_notes_excluded'):
        if record.get('editorial_checks', {}).get(field) is not True:
            raise ValueError('Editorial review must address ' + field + '.')
    page_reviews = record.get('page_reviews', {})
    for name in READER_PAGES:
        review = page_reviews.get(name, {})
        for field in ('reader', 'question', 'answer', 'next_destination'):
            if not isinstance(review.get(field), str) or not review[field].strip():
                raise ValueError('Missing reader-journey review: ' + name + '/' + field)
        if not isinstance(review.get('answer_sections'), list) or not review['answer_sections']:
            raise ValueError('Missing answer sections for ' + name)
    checks = record.get('browser_checks', [])
    for language in ('pt', 'en'):
        for device in ('mobile', 'desktop'):
            matches = [x for x in checks if x.get('language') == language and x.get('device') == device]
            if not any(x.get('status') == 'observed' and x.get('evidence')
                       and Path(x['evidence']).is_file()
                       and not Path(x['evidence']).resolve().is_relative_to(root) for x in matches):
                raise ValueError('Missing private browser evidence: ' + language + '/' + device)
    return record


def require_review(root):
    parser = argparse.ArgumentParser(description='Build IMOBX with a fresh private copy review.')
    parser.add_argument('--copy-review', type=Path,
                        help='Private JSON record outside this published directory.')
    parser.add_argument('--preview', action='store_true',
                        help='Render local HTML for review; do not build PDF, PowerPoint or ZIP exports.')
    args = parser.parse_args()
    if args.preview:
        if args.copy_review:
            parser.error('Use --preview to inspect HTML, then --copy-review for reviewed exports.')
        print('Unreviewed local HTML preview. PDF, PowerPoint and ZIP exports will not be built.')
        return True
    if not args.copy_review:
        parser.error('Reviewed exports require --copy-review.')
    try:
        record = verify(root, args.copy_review)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.error(str(error))
    print('Copy review current: ' + record['scope'] + '; audience testing: ' + record['audience_testing'] + '.')
    return False
