"""Tests for the diff parser module."""

from pr_reviewer_bot.diff_parser import DiffFile, DiffHunk, parse_diff


SIMPLE_DIFF = """\
diff --git a/hello.py b/hello.py
index 1234567..abcdefg 100644
--- a/hello.py
+++ b/hello.py
@@ -1,3 +1,4 @@
 import os
+import sys
 
 def main():
"""

MULTI_FILE_DIFF = """\
diff --git a/a.py b/a.py
index 1111111..2222222 100644
--- a/a.py
+++ b/a.py
@@ -1,2 +1,3 @@
 x = 1
+y = 2
 z = 3
diff --git a/b.py b/b.py
index 3333333..4444444 100644
--- a/b.py
+++ b/b.py
@@ -1,3 +1,2 @@
 a = 1
-b = 2
 c = 3
"""

MULTI_HUNK_DIFF = """\
diff --git a/file.py b/file.py
--- a/file.py
+++ b/file.py
@@ -1,3 +1,4 @@
 line1
+added_top
 line2
 line3
@@ -10,3 +11,4 @@
 line10
+added_bottom
 line11
 line12
"""

REMOVAL_ONLY_DIFF = """\
diff --git a/old.py b/old.py
--- a/old.py
+++ b/old.py
@@ -1,4 +1,2 @@
 keep1
-remove1
-remove2
 keep2
"""


class TestParseDiffSingleFile:
    def test_parses_filename(self):
        files = parse_diff(SIMPLE_DIFF)
        assert len(files) == 1
        assert files[0].filename == "hello.py"

    def test_parses_added_lines(self):
        files = parse_diff(SIMPLE_DIFF)
        assert len(files[0].added_lines) == 1
        line_num, content = files[0].added_lines[0]
        assert line_num == 2
        assert content == "import sys"

    def test_no_removed_lines(self):
        files = parse_diff(SIMPLE_DIFF)
        assert len(files[0].removed_lines) == 0

    def test_parses_hunk(self):
        files = parse_diff(SIMPLE_DIFF)
        assert len(files[0].hunks) == 1
        hunk = files[0].hunks[0]
        assert hunk.old_start == 1
        assert hunk.old_count == 3
        assert hunk.new_start == 1
        assert hunk.new_count == 4


class TestParseDiffMultipleFiles:
    def test_parses_two_files(self):
        files = parse_diff(MULTI_FILE_DIFF)
        assert len(files) == 2
        assert files[0].filename == "a.py"
        assert files[1].filename == "b.py"

    def test_first_file_additions(self):
        files = parse_diff(MULTI_FILE_DIFF)
        assert len(files[0].added_lines) == 1
        assert files[0].added_lines[0][1] == "y = 2"

    def test_second_file_removals(self):
        files = parse_diff(MULTI_FILE_DIFF)
        assert len(files[1].removed_lines) == 1
        assert files[1].removed_lines[0][1] == "b = 2"


class TestParseDiffMultiHunk:
    def test_parses_two_hunks(self):
        files = parse_diff(MULTI_HUNK_DIFF)
        assert len(files) == 1
        assert len(files[0].hunks) == 2

    def test_hunk_line_numbers(self):
        files = parse_diff(MULTI_HUNK_DIFF)
        assert files[0].hunks[0].new_start == 1
        assert files[0].hunks[1].new_start == 11

    def test_added_line_numbers(self):
        files = parse_diff(MULTI_HUNK_DIFF)
        added = files[0].added_lines
        assert len(added) == 2
        assert added[0][0] == 2
        assert added[1][0] == 12


class TestParseDiffEdgeCases:
    def test_empty_input(self):
        assert parse_diff("") == []

    def test_removal_only(self):
        files = parse_diff(REMOVAL_ONLY_DIFF)
        assert len(files) == 1
        assert len(files[0].added_lines) == 0
        assert len(files[0].removed_lines) == 2

    def test_hunk_lines_stored(self):
        files = parse_diff(SIMPLE_DIFF)
        hunk = files[0].hunks[0]
        assert len(hunk.lines) == 4  # context + addition + blank + context
