"""HTML export functionality for standalone visualization files."""

import json
from dataclasses import dataclass
from pathlib import Path
from string import Template

from .models import Scene


@dataclass
class ExportOptions:
    """Options for HTML export customization.

    Attributes:
        title: Custom title for the HTML document.
            Overrides Scene.title if provided.
        description: Description text to display in the HTML.
        width: Container width as CSS value (e.g., "100%", "800px").
            Default: "100%"
        height: Container height in pixels.
            Default: 600
    """

    title: str | None = None
    description: str | None = None
    width: str = "100%"
    height: int = 600


class HTMLExporter:
    """Converts Scene objects to standalone HTML documents.

    This class handles the template-based generation of self-contained
    HTML files that embed all necessary resources (D3.js, CSS, data)
    for offline visualization.

    This is an internal implementation class. Users should use
    Plotter.export_html() instead.
    """

    def __init__(self) -> None:
        """Initialize exporter with cached template and resources.

        Loads the HTML template and JS bundle once at initialization
        for efficient reuse across multiple export calls.
        """
        self._template: Template = self._load_template()
        self._js_bundle: str = self._load_js_bundle()

    def export(
        self,
        scene: Scene,
        options: ExportOptions | None = None,
    ) -> str:
        """Generate standalone HTML from scene.

        Args:
            scene: Scene object containing graph layers to export.
            options: Optional ExportOptions for customization.
                If None, default options are used.

        Returns:
            Complete HTML document as UTF-8 string.

        Notes:
            - Empty scenes produce valid HTML with empty visualization
            - All scene layers are included in the export
            - Node/edge metadata is preserved in embedded JSON
        """
        if options is None:
            options = ExportOptions()

        # Resolve title
        title = self._resolve_title(options, scene)

        # Generate components
        css_styles = self._generate_css()
        json_data = self._serialize_data(scene)

        # Substitute template variables
        html = self._template.substitute(
            title=title,
            display_title=title if title != "Network Visualization" else "",
            description=options.description or "",
            width=options.width,
            height=options.height,
            css_styles=css_styles,
            js_bundle=self._js_bundle,
            json_data=json_data,
        )

        return html

    def _load_template(self) -> Template:
        """Load HTML template from package resources.

        Returns:
            string.Template object with placeholder variables.

        Raises:
            FileNotFoundError: If template file is missing from package.
        """
        template_path = Path(__file__).parent / "templates" / "standalone.html"
        if not template_path.exists():
            raise FileNotFoundError(f"HTML template not found: {template_path}")
        template_content = template_path.read_text(encoding="utf-8")
        return Template(template_content)

    def _load_js_bundle(self) -> str:
        """Load minified JavaScript bundle.

        The bundle includes:
        - D3.js (selection, force, zoom, drag modules)
        - NetVis rendering code (adapted from graph.ts)
        - Settings and color schemes

        Returns:
            Minified JavaScript code as string.

        Raises:
            FileNotFoundError: If bundle file is missing from package.
        """
        bundle_path = Path(__file__).parent / "resources" / "netvis-standalone.min.js"
        if not bundle_path.exists():
            raise FileNotFoundError(f"JavaScript bundle not found: {bundle_path}")
        return bundle_path.read_text(encoding="utf-8")

    def _generate_css(self) -> str:
        """Generate CSS styles for the visualization.

        Returns:
            CSS stylesheet as string.

        Styles include:
        - Container layout (responsive width, fixed height)
        - Title and description typography
        - SVG element sizing
        - Node and edge default styles
        - Hover and selection states
        """
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                         'Helvetica Neue', Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }

        .netvis-container {
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
        }

        .netvis-title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #222;
        }

        .netvis-description {
            font-size: 14px;
            color: #666;
            margin-bottom: 20px;
            line-height: 1.5;
        }

        #netvis-graph {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 4px;
            overflow: hidden;
        }

        #netvis-graph svg {
            width: 100%;
            height: 100%;
            display: block;
        }

        .node-group circle {
            cursor: pointer;
            stroke: #fff;
            stroke-width: 1.5px;
        }

        .node-group circle:hover {
            stroke: #333;
            stroke-width: 2px;
        }

        .node-group.clicked circle {
            stroke: #000;
            stroke-width: 3px;
        }

        .node-group text {
            pointer-events: none;
            font-size: 12px;
            fill: #333;
            text-shadow: 0 1px 2px rgba(255,255,255,0.8);
        }
        """

    def _serialize_data(self, scene: Scene) -> str:
        """Serialize scene to JSON for embedding.

        Uses Scene.to_dict() to convert the scene to the netvis
        JSON format, then serializes to a JSON string suitable
        for embedding in a <script> tag.

        Args:
            scene: Scene object to serialize.

        Returns:
            JSON string (UTF-8, no extra whitespace).
        """
        scene_dict = scene.to_dict()
        return json.dumps(scene_dict, ensure_ascii=False)

    def _resolve_title(
        self,
        options: ExportOptions | None,
        scene: Scene,
    ) -> str:
        """Resolve final title from options and scene.

        Priority:
        1. options.title (if provided)
        2. scene.title (if provided)
        3. "Network Visualization" (default)

        Args:
            options: Export options (may be None).
            scene: Scene object.

        Returns:
            Resolved title string.
        """
        if options and options.title:
            return options.title
        if scene.title:
            return scene.title
        return "Network Visualization"
