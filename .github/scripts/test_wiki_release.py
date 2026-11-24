"""Regression checks for wiki release preparation and publication."""

from datetime import date
import unittest

from wiki_release import next_tag, prepare, release_notes


class WikiReleaseTests(unittest.TestCase):
    """Exercise version collisions, changelog boundaries, and release selection."""

    today = date(2026, 11, 24)
    pending = '# Changelog\n\n## [Unreleased]\n\n### Fixed\n\n- Correct links.\n'

    def test_version_sequence(self):
        """Use numeric suffix ordering and ignore other sites and months."""
        self.assertEqual(next_tag(['blog-2026.11', 'wiki-2026.10.9'], '', self.today),
                         'wiki-2026.11')
        self.assertEqual(next_tag(['wiki-2026.11'], '', self.today), 'wiki-2026.11.1')
        self.assertEqual(next_tag(['wiki-2026.11.2', 'wiki-2026.11.10'], '', self.today),
                         'wiki-2026.11.11')
        self.assertEqual(next_tag([], '## [wiki-2026.11.1] - 2026-11-24', self.today),
                         'wiki-2026.11.2')

    def test_prepare_and_publish(self):
        """Move only pending entries and preserve history and reference links."""
        history = ('\n## [wiki-2026.07] - 2026-07-20\n\n### Added\n\n- Older page.\n\n'
                   '[wiki-2026.07]: https://example.com/old\n')
        tag, text = prepare(self.pending + history, [], self.today)
        self.assertEqual(tag, 'wiki-2026.11')
        self.assertIn('## [Unreleased]\n\n## [wiki-2026.11] - 2026-11-24', text)
        self.assertIn(history.strip(), text)
        self.assertEqual(release_notes(text, []), (tag, '### Fixed\n\n- Correct links.'))
        self.assertIsNone(release_notes(text, [tag]))

    def test_links_without_history(self):
        """Keep final link definitions out of release notes."""
        _, text = prepare(self.pending + '\n[guide]: https://example.com\n', [], self.today)
        self.assertEqual(text.count('[guide]: https://example.com'), 1)
        self.assertNotIn('[guide]:', release_notes(text, [])[1])

    def test_empty_and_duplicate_pending(self):
        """Never prepare an empty release or an ambiguous changelog."""
        for text in ('## [Unreleased]\n\n### Fixed\n', self.pending + self.pending):
            with self.assertRaises(ValueError):
                prepare(text, [], self.today)

    def test_month_boundary_and_existing_tag(self):
        """Publication uses the prepared version rather than today's month."""
        text = '## [Unreleased]\n\n## [wiki-2026.10.2] - 2026-10-31\n\n- Fix.\n'
        self.assertEqual(release_notes(text, [])[0], 'wiki-2026.10.2')
        self.assertIsNone(release_notes(text, ['wiki-2026.10.2']))

    def test_invalid_release(self):
        """Reject malformed dates and empty dated releases."""
        for text in ('## [wiki-2026.11] - 2026-11-99\n- Fix.\n',
                     '## [wiki-2026.11] - 2026-11-24\n### Fixed\n'):
            with self.assertRaises(ValueError):
                release_notes(text, [])


if __name__ == '__main__':
    unittest.main()
