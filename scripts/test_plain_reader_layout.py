from __future__ import annotations
import unittest
from note_validation import (CONTENT_FIRST_HEADINGS, PLAIN_CONTENT_FIRST_HEADINGS,
                             validate_content_first_layout, validate_lecture_note)
from unit_validation import validate_unit_layout

def questions():
    return ('#### Recall Q01 · Address\n\nWhat does the address identify?\n\n'
            '<details><summary>Answer</summary>\nA location under the stated model.\n</details>\n\n'
            '#### Practice P01 · Size\n\nSynthetic: add two four-byte fields.\n\n'
            '<details><summary>Answer</summary>\nFour plus four is eight.\n</details>\n')

class PlainReaderLayoutTests(unittest.TestCase):
    def test_unit_keeps_concepts_question_answers_and_sources_in_both_languages(self):
        for language,recall,sources,summary in [('ko','확인·연습문제','출처','핵심 정리'),
                                                ('en','Recall and Practice','Sources','Key Takeaways')]:
            body=f'## Addresses\n\nAn address names a location under stated assumptions.\n\n## {recall}\n\n'+questions()+f'\n## {sources}\n\nAn exact reviewed lecture.\n'
            self.assertEqual(validate_unit_layout(body,language,reader_layout='content_first'),[])
            self.assertTrue(validate_unit_layout('Overview.\n\n'+body,language,reader_layout='content_first'))
            repeated=body.replace(f'## {recall}',f'## {summary}\n\nSame explanation again.\n\n## {recall}')
            self.assertTrue(validate_unit_layout(repeated,language,reader_layout='content_first'))
            self.assertTrue(validate_unit_layout(body.replace('<details>','<details open>'),language,reader_layout='content_first'))
            self.assertTrue(validate_unit_layout(body.replace('Practice P01','Recall Q01'),language,reader_layout='content_first'))
            self.assertTrue(validate_unit_layout(body,language,reader_layout='unknown'))

    def test_lecture_legacy_and_plain_layout_are_explicit_distinct_choices(self):
        for language in ['ko','en']:
            legacy='\n\n'.join('## '+h+'\n\nSubstantive text.' for h in CONTENT_FIRST_HEADINGS[language])+'\n'
            plain='\n\n'.join('## '+h+'\n\nSubstantive text.' for h in PLAIN_CONTENT_FIRST_HEADINGS[language])+'\n'
            self.assertEqual(validate_content_first_layout(legacy,language),[])
            self.assertEqual(validate_content_first_layout(plain,language,reader_layout='content_first'),[])
            self.assertTrue(validate_content_first_layout(plain,language))
            self.assertTrue(validate_content_first_layout(legacy,language,reader_layout='content_first'))
            self.assertTrue(validate_content_first_layout('Introduction.\n\n'+plain,language,reader_layout='content_first'))

    def test_plain_lecture_does_not_waive_depth_evidence_questions_or_coverage(self):
        note='---\nnote_layout: content_first_v1\nreader_layout: content_first\n---\n'+'\n\n'.join('## '+h+'\n\nA short paragraph.' for h in PLAIN_CONTENT_FIRST_HEADINGS['ko'])
        errors=validate_lecture_note(note,'ko')
        self.assertTrue(any('너무 짧' in e for e in errors))
        self.assertTrue(any('근거 표시' in e for e in errors))
        self.assertTrue(any('능동회상' in e for e in errors))
        self.assertTrue(any('coverage table' in e for e in errors))
        invalid=note.replace('reader_layout: content_first','reader_layout: [content_first]')
        self.assertTrue(any('reader_layout' in e for e in validate_lecture_note(invalid,'ko')))

if __name__=='__main__':unittest.main()
