# Changelog

## 0.4.0 (2025-XX-XX)

**Major Release: Migration to MIME Renderer Architecture**

### Breaking Changes

- **Removed ipywidgets dependency**: NetVis no longer requires or uses ipywidgets for rendering
- **Removed nbextension support**: The Jupyter Notebook classic extension has been removed
- **Simplified installation**: No manual extension enabling required - works automatically in JupyterLab 3.x/4.x
- **Python API unchanged**: Existing code using `NetVis(value=data)` continues to work without modification

### New Features

- MIME Renderer Architecture using custom MIME type `application/vnd.netvis+json`
- Automatic rendering in JupyterLab output cells
- Version validation between frontend and backend
- Enhanced error handling for invalid graph data

### Improvements

- Cleaner codebase with duplicate code removed
- Better performance with simplified rendering pipeline
- Comprehensive test coverage (Python 75%, TypeScript 41%)
- Modern JupyterLab 3.x/4.x architecture

### Migration

See [MIGRATION.md](./MIGRATION.md) for migration guide from 0.3.x to 0.4.0.

### Compatibility

- Supported: JupyterLab 3.x and 4.x
- Not Supported: Jupyter Notebook Classic
- Python: 3.10+
- D3.js: 7.9+ (all visualization features preserved)

## 0.3.1 (2025-07-12)

- bugfix for build version (terapyon)

## 0.3.0 (2025-07-12)

- Add node text (karad)

## 0.2.0 (2025-04-04)

- Additional styling capabilities for network visualization (karad)
- Enhanced customization options for nodes and links (karad)
- Improved color scheme and style configuration support (karad)
- Fixed package installation and CI/CD workflows (terapyon)

## 0.1.1 (2025-04-02)

- Modify document links (terapyon)
- PyPI releases using GitHub Actions (terapyon)

## 0.1.0 (2025-03-08)

- internal release (terapyon)
