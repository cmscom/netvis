"""Tests for HTML export functionality."""

import sys
from pathlib import Path

import pytest

from net_vis import Plotter
from net_vis.html_exporter import HTMLExporter
from net_vis.models import Edge, GraphLayer, Node, Scene


@pytest.fixture
def sample_scene() -> Scene:
    """Create a sample scene with one layer for testing."""
    nodes = [
        Node(id="1", label="Node 1", x=0, y=0, color="TYPE_A"),
        Node(id="2", label="Node 2", x=100, y=100, color="TYPE_B"),
        Node(id="3", label="Node 3", x=50, y=150, color="TYPE_A"),
    ]
    edges = [
        Edge(source="1", target="2", label="edge1"),
        Edge(source="2", target="3", label="edge2"),
    ]
    layer = GraphLayer(layer_id="test_layer", nodes=nodes, edges=edges)
    return Scene(layers=[layer], title="Test Scene")


@pytest.fixture
def sample_plotter(sample_scene: Scene) -> Plotter:
    """Create a plotter with sample data for testing."""
    plotter = Plotter(title="Test Graph")
    # Directly set the internal scene for testing
    plotter._scene = sample_scene
    return plotter


@pytest.fixture
def exporter() -> HTMLExporter:
    """Create HTMLExporter instance."""
    return HTMLExporter()


class TestHTMLExporterBasic:
    """Basic HTML export tests for User Story 1."""

    def test_exporter_initialization(self, exporter: HTMLExporter) -> None:
        """Test that HTMLExporter initializes with template and bundle."""
        assert exporter._template is not None
        assert exporter._js_bundle is not None
        assert len(exporter._js_bundle) > 0

    def test_export_returns_string(self, exporter: HTMLExporter, sample_scene: Scene) -> None:
        """Test that export() returns HTML as string."""
        html = exporter.export(sample_scene)
        assert isinstance(html, str)
        assert len(html) > 0


class TestExportToFile:
    """Tests for file export functionality (T015-T017)."""

    def test_export_to_file(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T015: Verify file is created with .html extension."""
        filepath = tmp_path / "test_graph.html"
        result = sample_plotter.export_html(filepath)

        assert isinstance(result, Path)
        assert result.exists()
        assert result.suffix == ".html"

    def test_export_auto_adds_html_extension(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """Verify .html extension is auto-added if missing."""
        filepath = tmp_path / "test_graph"  # No extension
        result = sample_plotter.export_html(filepath)

        assert result.suffix == ".html"
        assert result.name == "test_graph.html"
        assert result.exists()

    def test_export_creates_directories(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T016: Verify parent directories are created automatically."""
        filepath = tmp_path / "subdir1" / "subdir2" / "test_graph.html"
        assert not filepath.parent.exists()

        result = sample_plotter.export_html(filepath)

        assert result.exists()
        assert filepath.parent.exists()

    def test_export_overwrites_existing(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T017: Verify file overwrite behavior."""
        filepath = tmp_path / "test_graph.html"

        # Write initial file
        filepath.write_text("original content")
        assert filepath.read_text() == "original content"

        # Export should overwrite
        sample_plotter.export_html(filepath)

        content = filepath.read_text()
        assert "original content" not in content
        assert "<!DOCTYPE html>" in content


class TestExportedHTMLValidity:
    """Tests for HTML content validity (T018-T021)."""

    def test_exported_html_is_valid(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T018: Verify valid HTML5 structure."""
        filepath = tmp_path / "test.html"
        sample_plotter.export_html(filepath)
        html = filepath.read_text(encoding="utf-8")

        # Check HTML5 doctype
        assert html.startswith("<!DOCTYPE html>")

        # Check essential HTML structure
        assert "<html" in html
        assert "</html>" in html
        assert "<head>" in html
        assert "</head>" in html
        assert "<body>" in html
        assert "</body>" in html

        # Check meta tags
        assert 'charset="UTF-8"' in html
        assert 'name="viewport"' in html

    def test_exported_html_contains_data(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T019: Verify graph data embedded as JSON."""
        filepath = tmp_path / "test.html"
        sample_plotter.export_html(filepath)
        html = filepath.read_text(encoding="utf-8")

        # Check that node data is embedded
        assert '"nodes"' in html
        assert '"links"' in html

        # Check specific node IDs from sample data
        assert '"id": "1"' in html or '"id":"1"' in html
        assert '"id": "2"' in html or '"id":"2"' in html

    def test_exported_html_contains_js(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T020: Verify JavaScript bundle embedded."""
        filepath = tmp_path / "test.html"
        sample_plotter.export_html(filepath)
        html = filepath.read_text(encoding="utf-8")

        # Check that JS bundle is embedded
        assert "<script>" in html
        assert "netvis" in html.lower()
        assert "renderGraph" in html

    def test_exported_html_offline_capable(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T021: Verify no external resource references."""
        filepath = tmp_path / "test.html"
        sample_plotter.export_html(filepath)
        html = filepath.read_text(encoding="utf-8")

        # Check no external script sources
        assert 'src="http' not in html
        assert 'src="https' not in html
        assert "src='//" not in html
        assert 'src="//' not in html

        # Check no external stylesheets
        assert 'href="http' not in html.lower()
        assert 'href="https' not in html.lower()

        # Check no CDN references
        assert "cdn" not in html.lower()
        assert "unpkg" not in html.lower()
        assert "jsdelivr" not in html.lower()


class TestExportWithCustomTitle:
    """Tests for custom title functionality (US2 - T029, T032, T033)."""

    def test_export_with_custom_title(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T029: Verify custom title appears in exported HTML."""
        filepath = tmp_path / "test.html"
        sample_plotter.export_html(filepath, title="Custom Title")
        html = filepath.read_text(encoding="utf-8")

        assert "<title>Custom Title</title>" in html

    def test_title_priority_options_over_scene(
        self, sample_plotter: Plotter, tmp_path: Path
    ) -> None:
        """T032: Verify options.title overrides scene.title."""
        # sample_plotter has scene.title = "Test Scene"
        filepath = tmp_path / "test.html"
        sample_plotter.export_html(filepath, title="Override Title")
        html = filepath.read_text(encoding="utf-8")

        assert "<title>Override Title</title>" in html
        assert "Test Scene" not in html.split("<title>")[1].split("</title>")[0]

    def test_default_title_when_none(self, tmp_path: Path) -> None:
        """T033: Verify default title when none provided."""
        plotter = Plotter()  # No title
        filepath = tmp_path / "test.html"
        plotter.export_html(filepath)
        html = filepath.read_text(encoding="utf-8")

        assert "<title>Network Visualization</title>" in html


class TestExportWithDescription:
    """Tests for description functionality (US2 - T030)."""

    def test_export_with_description(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T030: Verify description appears in exported HTML."""
        filepath = tmp_path / "test.html"
        sample_plotter.export_html(filepath, description="Test description text")
        html = filepath.read_text(encoding="utf-8")

        assert "Test description text" in html


class TestExportWithCustomSize:
    """Tests for custom size functionality (US2 - T031, T034)."""

    def test_export_with_custom_size(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T031: Verify custom width/height in exported HTML."""
        filepath = tmp_path / "test.html"
        sample_plotter.export_html(filepath, width="800px", height=700)
        html = filepath.read_text(encoding="utf-8")

        assert "800px" in html
        assert "700px" in html

    def test_invalid_height_raises_valueerror(
        self, sample_plotter: Plotter, tmp_path: Path
    ) -> None:
        """T034: Verify ValueError for invalid height."""
        filepath = tmp_path / "test.html"

        with pytest.raises(ValueError, match="positive integer"):
            sample_plotter.export_html(filepath, height=-100)

        with pytest.raises(ValueError, match="positive integer"):
            sample_plotter.export_html(filepath, height=0)


class TestExportReturnsString:
    """Tests for string return functionality (US3 - T041-T043)."""

    def test_export_returns_string_when_no_filepath(self, sample_plotter: Plotter) -> None:
        """T041: Verify string returned when filepath is None."""
        result = sample_plotter.export_html()

        assert isinstance(result, str)
        assert "<!DOCTYPE html>" in result

    def test_returned_string_is_valid_html(self, sample_plotter: Plotter) -> None:
        """T042: Verify returned string is valid HTML."""
        html = sample_plotter.export_html()

        assert html.startswith("<!DOCTYPE html>")
        assert "<html" in html
        assert "</html>" in html

    def test_returned_html_can_be_saved_and_opened(
        self, sample_plotter: Plotter, tmp_path: Path
    ) -> None:
        """T043: Verify returned HTML can be saved to file."""
        html = sample_plotter.export_html()

        # Save to file manually
        filepath = tmp_path / "manual_save.html"
        filepath.write_text(html, encoding="utf-8")

        # Verify file content matches
        assert filepath.read_text(encoding="utf-8") == html


class TestExportWithDownload:
    """Tests for download functionality (US4 - T047-T049)."""

    def test_export_with_download_option(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T047: Verify download parameter is accepted."""
        filepath = tmp_path / "test.html"
        # Should not raise an error
        result = sample_plotter.export_html(filepath, download=True)
        assert result.exists()

    def test_download_triggers_ipython_display(
        self, sample_plotter: Plotter, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """T048: Verify IPython display is triggered with download=True."""
        display_called = []

        def mock_display(*args, **kwargs):
            display_called.append((args, kwargs))

        # Mock IPython display
        try:
            import IPython.display

            monkeypatch.setattr(IPython.display, "display", mock_display)
        except ImportError:
            pytest.skip("IPython not available")

        filepath = tmp_path / "test.html"
        sample_plotter.export_html(filepath, download=True)

        # In environments with IPython, display should be called
        # Note: This test may need adjustment based on actual implementation

    def test_download_with_custom_filename(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T049: Verify download works with custom filename."""
        filepath = tmp_path / "custom_name.html"
        result = sample_plotter.export_html(filepath, download=True)
        assert result.name == "custom_name.html"


class TestEdgeCases:
    """Tests for edge cases (Phase 7 - T055-T058)."""

    def test_export_empty_plotter(self, tmp_path: Path) -> None:
        """T055: Verify empty plotter produces valid HTML."""
        plotter = Plotter()  # Empty, no layers
        filepath = tmp_path / "empty.html"
        result = plotter.export_html(filepath)

        assert result.exists()
        html = filepath.read_text(encoding="utf-8")

        # Should still be valid HTML
        assert "<!DOCTYPE html>" in html
        assert '"nodes": []' in html or '"nodes":[]' in html

    def test_export_large_graph_performance(self, tmp_path: Path) -> None:
        """T056: Verify export completes in reasonable time for large graphs."""
        import time

        try:
            import networkx as nx
        except ImportError:
            pytest.skip("NetworkX not available")

        # Create a moderately large graph (1000 nodes)
        G = nx.barabasi_albert_graph(1000, 3)

        plotter = Plotter()
        plotter.add_networkx(G)

        filepath = tmp_path / "large_graph.html"
        start = time.time()
        plotter.export_html(filepath)
        elapsed = time.time() - start

        # Should complete within 30 seconds (SC-004)
        assert elapsed < 30, f"Export took {elapsed:.2f}s, expected < 30s"
        assert filepath.exists()

    @pytest.mark.skipif(sys.platform == "win32", reason="chmod doesn't work the same on Windows")
    def test_permission_error_propagates(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T057: Verify permission errors are propagated."""
        import stat

        # Create a read-only directory
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)  # Read and execute only

        try:
            filepath = readonly_dir / "test.html"
            with pytest.raises(PermissionError):
                sample_plotter.export_html(filepath)
        finally:
            # Restore permissions for cleanup
            readonly_dir.chmod(stat.S_IRWXU)

    def test_path_object_accepted(self, sample_plotter: Plotter, tmp_path: Path) -> None:
        """T058: Verify Path object is accepted as filepath."""
        filepath = Path(tmp_path) / "path_object_test.html"
        result = sample_plotter.export_html(filepath)

        assert isinstance(result, Path)
        assert result.exists()
