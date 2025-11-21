# Migration Guide: NetVis 0.3.x → 0.4.0

This guide helps you migrate from NetVis version 0.3.x to 0.4.0.

## Overview

Version 0.4.0 introduces a major architectural change from ipywidgets-based rendering to a MIME renderer extension. This simplifies installation and improves compatibility with modern JupyterLab environments.

## Breaking Changes

### 1. Removed ipywidgets Dependency

**What changed**: NetVis no longer uses ipywidgets for rendering graphs.

**Impact**:
- No action required for most users - the Python API remains unchanged
- Graphs now render using JupyterLab's MIME renderer system

**Migration**:
```python
# Your existing code works without changes
import net_vis

data = '{"nodes": [{"id": "A"}], "links": []}'
w = net_vis.NetVis(value=data)
w  # Still displays automatically in JupyterLab
```

### 2. Removed nbextension Support

**What changed**: The Jupyter Notebook classic nbextension has been removed.

**Impact**:
- NetVis 0.4.0 only works in **JupyterLab 3.x and 4.x**
- Jupyter Notebook Classic is **no longer supported**

**Migration**:

If you're using Jupyter Notebook Classic:
- **Option 1 (Recommended)**: Migrate to JupyterLab 3.x or 4.x
- **Option 2**: Stay on NetVis 0.3.x until you can migrate to JupyterLab

### 3. Simplified Installation

**What changed**: Manual extension enabling is no longer required.

**Old installation (0.3.x)**:
```bash
pip install net_vis
jupyter nbextension enable --py net_vis  # No longer needed
```

**New installation (0.4.0)**:
```bash
pip install net_vis
# That's it! No manual enabling required
```

**Migration**: Simply upgrade using pip:
```bash
pip install --upgrade net_vis
```

## Non-Breaking Changes

### Python API (No Changes Required)

The Python API for creating graphs remains **100% compatible**:

```python
import net_vis

# All existing code continues to work
data = """
{
  "nodes": [
    {"id": "A"},
    {"id": "B"}
  ],
  "links": [
    {"source": "A", "target": "B"}
  ]
}
"""

graph = net_vis.NetVis(value=data)
graph  # Displays in JupyterLab output cell
```

### D3.js Visualization Features (Fully Preserved)

All D3.js visualization features from 0.3.x are preserved in 0.4.0:
- ✅ Force-directed layout
- ✅ Node dragging
- ✅ Zoom and pan
- ✅ Interactive tooltips
- ✅ Custom node colors and sizes
- ✅ Directed edges with arrows

## Step-by-Step Migration

### For End Users

1. **Check your JupyterLab version**:
   ```bash
   jupyter lab --version
   ```
   - If version < 3.0: Upgrade to JupyterLab 3.x or 4.x first
   - If version ≥ 3.0: Proceed to step 2

2. **Upgrade NetVis**:
   ```bash
   pip install --upgrade net_vis
   ```

3. **Restart JupyterLab**:
   ```bash
   jupyter lab
   ```

4. **Test your notebooks**:
   - Open an existing notebook with NetVis graphs
   - Re-run cells with `NetVis()` objects
   - Graphs should display automatically

### For Developers

1. **Update development environment**:
   ```bash
   # Remove old nbextension build artifacts
   jupyter nbextension uninstall --py net_vis

   # Pull latest code
   git checkout 001-mime-renderer

   # Reinstall in development mode
   pip install -e ".[test]"
   jupyter labextension develop --overwrite .
   ```

2. **Remove nbextension references**:
   - Update documentation removing nbextension commands
   - Update CI/CD removing nbextension build steps

3. **Run tests**:
   ```bash
   pytest net_vis/tests/
   yarn test
   ```

## Troubleshooting

### "NetVis object displays as plain text"

**Cause**: JupyterLab doesn't have the MIME renderer registered.

**Solution**:
```bash
# Ensure the extension is installed
jupyter labextension list | grep net_vis

# If not listed, reinstall:
pip uninstall net_vis
pip install net_vis

# Restart JupyterLab
```

### "Module 'ipywidgets' not found" error

**Cause**: Old notebooks may have cached imports.

**Solution**:
1. Restart the notebook kernel
2. Clear all outputs: `Cell > All Output > Clear`
3. Re-run cells

### Jupyter Notebook Classic no longer supported

**Cause**: NetVis 0.4.0 uses MIME renderers which are JupyterLab-specific.

**Solution**:
- Migrate to JupyterLab 3.x or 4.x (recommended)
- Or continue using NetVis 0.3.x with Jupyter Notebook Classic

## New Features in 0.4.0

While migrating, take advantage of new features:

### Version Validation

NetVis now validates version compatibility between Python and TypeScript:
- Automatic warnings if frontend/backend versions mismatch
- Helps prevent rendering issues

### Improved Error Messages

Better error messages for common issues:
- Invalid JSON in graph data
- Missing required fields (`nodes`, `links`)
- Duplicate node IDs
- Invalid link references

### Enhanced Testing

More comprehensive test coverage ensures reliability:
- Python: 75% coverage
- TypeScript: 41% coverage
- Integration tests for MIME rendering

## Getting Help

If you encounter issues during migration:

1. **Check compatibility**:
   - JupyterLab version ≥ 3.0
   - Python version ≥ 3.10

2. **Review error messages**:
   - NetVis 0.4.0 provides detailed error messages
   - Check browser console for frontend errors

3. **File an issue**:
   - GitHub Issues: https://github.com/cmscom/netvis/issues
   - Include: NetVis version, JupyterLab version, error messages

## Rollback (if needed)

If you need to temporarily roll back to 0.3.x:

```bash
pip install net_vis==0.3.1
```

Note: This will reinstall the ipywidgets-based version.

## Summary

**Key Points**:
- ✅ Python API unchanged - existing code works
- ✅ All D3.js features preserved
- ⚠️ JupyterLab 3.x/4.x required
- ⚠️ Jupyter Notebook Classic no longer supported
- ✅ Simpler installation (no manual enabling)

**Benefits**:
- Cleaner, more maintainable codebase
- Better alignment with JupyterLab ecosystem
- Improved performance and error handling
- Future-proof architecture

For most users, migration is as simple as upgrading the package - your existing notebooks will continue to work without code changes.
