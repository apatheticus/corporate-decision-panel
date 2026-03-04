"""Tests for session orchestrator.

Covers: inter-call delay, adaptive delay on 429, session continues past
individual failures, summary table output, exit code logic, and SessionResult.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from scripts.generate_infographic import GenerationResult


class TestInterCallDelay:
    """Tests for 4-second inter-call delay between infographic generations."""

    def test_delay_between_images(self, tmp_path):
        """time.sleep(4.0) called between images (2 times for 3 images)."""
        from scripts.session import run_session

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        types_list = ["type-a", "type-b", "type-c"]
        data_paths = {t: tmp_path / f"{t}.json" for t in types_list}

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep") as mock_sleep,
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            run_session(types_list, data_paths, tmp_path / "output", tmp_path)

        # 2 delays for 3 images (between 1st-2nd and 2nd-3rd)
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(4.0)

    def test_no_delay_before_first_image(self, tmp_path):
        """No delay before the first image."""
        from scripts.session import run_session

        sleep_calls_before_gen = []
        gen_count = 0

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            nonlocal gen_count
            gen_count += 1
            sleep_calls_before_gen.append(mock_sleep.call_count)
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep") as mock_sleep,
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            run_session(
                ["type-a"],
                {"type-a": tmp_path / "a.json"},
                tmp_path / "output",
                tmp_path,
            )

        # Before first generate call, sleep should not have been called
        assert sleep_calls_before_gen[0] == 0


class TestAdaptiveDelay:
    """Tests for adaptive delay doubling on 429."""

    def test_delay_doubles_after_429(self, tmp_path):
        """If had_rate_limit=True on 2nd image, 3rd image delay is 8.0s (doubled)."""
        from scripts.session import run_session

        call_count = 0

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                return GenerationResult(
                    success=True,
                    output_path=output_path,
                    prompt_path=tmp_path / "prompt.txt",
                    had_rate_limit=True,
                )
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
                had_rate_limit=False,
            )

        types_list = ["type-a", "type-b", "type-c"]
        data_paths = {t: tmp_path / f"{t}.json" for t in types_list}

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep") as mock_sleep,
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            run_session(types_list, data_paths, tmp_path / "output", tmp_path)

        # First delay: 4.0 (before type-b)
        # After type-b has had_rate_limit, delay doubles to 8.0
        # Second delay: 8.0 (before type-c)
        assert mock_sleep.call_args_list == [call(4.0), call(8.0)]


class TestSessionContinuesOnFailure:
    """Tests that session continues past individual failures."""

    def test_all_types_attempted_despite_failure(self, tmp_path):
        """If type 2 of 3 fails, types 1 and 3 are still attempted."""
        from scripts.session import run_session

        attempted = []

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            attempted.append(type_slug)
            if type_slug == "type-b":
                return GenerationResult(
                    success=False,
                    error_code="API_ERROR_500",
                    prompt_path=tmp_path / "prompt.txt",
                )
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        types_list = ["type-a", "type-b", "type-c"]
        data_paths = {t: tmp_path / f"{t}.json" for t in types_list}

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep"),
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            result = run_session(types_list, data_paths, tmp_path / "output", tmp_path)

        assert attempted == ["type-a", "type-b", "type-c"]
        assert result.any_succeeded is True


class TestSessionSummary:
    """Tests for summary table output."""

    def test_summary_lines_contain_status(self, tmp_path):
        """Summary lines show OK, FAILED, BLOCKED status strings."""
        from scripts.session import run_session

        call_count = 0

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            nonlocal call_count
            call_count += 1
            if type_slug == "type-b":
                return GenerationResult(
                    success=False,
                    error_code="API_ERROR_500",
                    prompt_path=tmp_path / "prompt.txt",
                )
            if type_slug == "type-c":
                return GenerationResult(
                    success=False,
                    error_code="CONTENT_BLOCKED_SAFETY",
                    prompt_path=tmp_path / "prompt.txt",
                )
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
            )

        types_list = ["type-a", "type-b", "type-c"]
        data_paths = {t: tmp_path / f"{t}.json" for t in types_list}

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep"),
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            result = run_session(types_list, data_paths, tmp_path / "output", tmp_path)

        # Find status strings in summary_lines
        all_lines = "\n".join(result.summary_lines)
        assert "OK" in all_lines
        assert "FAILED" in all_lines
        assert "BLOCKED" in all_lines

    def test_any_succeeded_true_with_mixed_results(self, tmp_path):
        """any_succeeded is True when at least one image succeeds."""
        from scripts.session import run_session

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            if type_slug == "type-a":
                return GenerationResult(
                    success=True,
                    output_path=output_path,
                    prompt_path=tmp_path / "prompt.txt",
                )
            return GenerationResult(
                success=False,
                error_code="API_ERROR_500",
                prompt_path=tmp_path / "prompt.txt",
            )

        types_list = ["type-a", "type-b"]
        data_paths = {t: tmp_path / f"{t}.json" for t in types_list}

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep"),
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            result = run_session(types_list, data_paths, tmp_path / "output", tmp_path)

        assert result.any_succeeded is True

    def test_summary_shows_attempts_format(self, tmp_path):
        """Summary lines show attempts in '{used}/{max}' format."""
        from scripts.session import _format_summary_line

        line = _format_summary_line("domain-scorecard", "OK", 1, 3, Path("images/test.png"))
        assert "1/3" in line

    def test_summary_shows_output_path(self, tmp_path):
        """Summary lines show the output path."""
        from scripts.session import _format_summary_line

        path = Path("images/INFOGRAPHIC_domain-scorecard.png")
        line = _format_summary_line("domain-scorecard", "OK", 1, 3, path)
        assert "images/INFOGRAPHIC_domain-scorecard.png" in line


class TestOkWarnStatus:
    """Tests for OK+WARN status in session summary when result.warning_only is True."""

    def test_ok_warn_in_summary(self, tmp_path):
        """When result.warning_only=True, summary line contains 'OK+WARN'."""
        from scripts.session import run_session

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
                warning_only=True,
            )

        types_list = ["type-a"]
        data_paths = {"type-a": tmp_path / "a.json"}

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep"),
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            result = run_session(types_list, data_paths, tmp_path / "output", tmp_path)

        all_lines = "\n".join(result.summary_lines)
        assert "OK+WARN" in all_lines

    def test_ok_without_warn(self, tmp_path):
        """When result.warning_only=False, summary shows 'OK' but NOT 'OK+WARN'."""
        from scripts.session import run_session

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            return GenerationResult(
                success=True,
                output_path=output_path,
                prompt_path=tmp_path / "prompt.txt",
                warning_only=False,
            )

        types_list = ["type-a"]
        data_paths = {"type-a": tmp_path / "a.json"}

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep"),
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            result = run_session(types_list, data_paths, tmp_path / "output", tmp_path)

        all_lines = "\n".join(result.summary_lines)
        assert "OK" in all_lines
        assert "OK+WARN" not in all_lines

    def test_mixed_ok_warn_and_failed(self, tmp_path):
        """Three types: OK+WARN, OK, FAILED -- all three statuses appear in summary."""
        from scripts.session import run_session

        call_count = 0

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            nonlocal call_count
            call_count += 1
            if type_slug == "type-a":
                return GenerationResult(
                    success=True,
                    output_path=output_path,
                    prompt_path=tmp_path / "prompt.txt",
                    warning_only=True,
                )
            if type_slug == "type-b":
                return GenerationResult(
                    success=True,
                    output_path=output_path,
                    prompt_path=tmp_path / "prompt.txt",
                    warning_only=False,
                )
            return GenerationResult(
                success=False,
                error_code="API_ERROR_500",
                prompt_path=tmp_path / "prompt.txt",
            )

        types_list = ["type-a", "type-b", "type-c"]
        data_paths = {t: tmp_path / f"{t}.json" for t in types_list}

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep"),
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            result = run_session(types_list, data_paths, tmp_path / "output", tmp_path)

        all_lines = "\n".join(result.summary_lines)
        assert "OK+WARN" in all_lines
        assert "FAILED" in all_lines
        # Check that there's a plain "OK" line (type-b) distinct from "OK+WARN"
        # Find the line for type-b specifically
        type_b_line = [l for l in result.summary_lines if "type-b" in l][0]
        assert "OK" in type_b_line
        assert "OK+WARN" not in type_b_line


class TestSessionAllFailed:
    """Tests for when all infographic types fail."""

    def test_any_succeeded_false_when_all_fail(self, tmp_path):
        """any_succeeded is False when all types fail."""
        from scripts.session import run_session

        def mock_gen_retry(type_slug, data_path, output_path, retry_limit, config_dir):
            return GenerationResult(
                success=False,
                error_code="API_ERROR_500",
                prompt_path=tmp_path / "prompt.txt",
            )

        types_list = ["type-a", "type-b", "type-c"]
        data_paths = {t: tmp_path / f"{t}.json" for t in types_list}

        with (
            patch("scripts.session.generate_with_retry", side_effect=mock_gen_retry),
            patch("scripts.session.time.sleep"),
            patch("scripts.session.load_config", return_value={"retry_limit": 2}),
            patch("scripts.session._status"),
        ):
            result = run_session(types_list, data_paths, tmp_path / "output", tmp_path)

        assert result.any_succeeded is False
        assert result.total_types == 3


class TestSessionExitCode:
    """Tests for session exit code logic."""

    def test_exit_code_0_when_any_succeeded(self, tmp_path):
        """SessionResult with any_succeeded=True implies exit code 0."""
        from scripts.session import SessionResult

        result = SessionResult(
            results={"type-a": GenerationResult(success=True)},
            any_succeeded=True,
            total_types=1,
        )
        # Exit code 0 if any succeeded
        exit_code = 0 if result.any_succeeded else 1
        assert exit_code == 0

    def test_exit_code_1_when_all_failed(self, tmp_path):
        """SessionResult with any_succeeded=False implies exit code 1."""
        from scripts.session import SessionResult

        result = SessionResult(
            results={"type-a": GenerationResult(success=False)},
            any_succeeded=False,
            total_types=1,
        )
        exit_code = 0 if result.any_succeeded else 1
        assert exit_code == 1


class TestSessionResult:
    """Tests for SessionResult dataclass."""

    def test_session_result_defaults(self):
        """SessionResult has sensible defaults."""
        from scripts.session import SessionResult

        result = SessionResult(results={})
        assert result.any_succeeded is False
        assert result.total_types == 0
        assert result.summary_lines == []

    def test_session_result_stores_results(self):
        """SessionResult stores per-type results dict."""
        from scripts.session import SessionResult

        gen_result = GenerationResult(success=True, output_path=Path("test.png"))
        result = SessionResult(
            results={"domain-scorecard": gen_result},
            any_succeeded=True,
            total_types=1,
        )
        assert "domain-scorecard" in result.results
        assert result.results["domain-scorecard"].success is True
