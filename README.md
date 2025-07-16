# Basic Memory GitHub Sync Solution

This project provides automated synchronization between Basic Memory projects and GitHub repositories using MCP (Model Context Protocol) tools.

## The Problem

Basic Memory stores knowledge locally in Markdown files, but there's no built-in way to automatically sync these files to GitHub when they're created or updated. This creates a gap where:

- Basic Memory creates/updates files locally
- Users have to manually commit and push changes to GitHub
- Knowledge can get out of sync between local and cloud storage
- Team collaboration becomes difficult

## The Solution

This sync solution bridges Basic Memory and GitHub by:

1. **Monitoring Basic Memory projects** for file changes
2. **Reading file contents** using Basic Memory MCP tools 
3. **Automatically pushing changes** to GitHub using GitHub MCP tools
4. **Maintaining project structure** across local and remote repositories

## Features

- ✅ **Automatic sync** from Basic Memory to GitHub
- ✅ **Multi-project support** - sync different Basic Memory projects to different GitHub repos/paths
- ✅ **Configurable sync intervals** and batch sizes
- ✅ **Dry-run mode** to test without making changes
- ✅ **File filtering** to exclude temporary files
- ✅ **MCP integration** leveraging existing Claude Desktop tools
- ✅ **Cross-platform** Python solution

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Your Projects

Edit `sync_config.ini` to match your setup:

```ini
[main]
local_path = C:\Users\nicka\dev\knowledge\main
github_repo = nickagillis/dev-knowledge-base
github_path = main
sync_enabled = true
```

### 3. Test the Sync (Dry Run)

```bash
python basic_memory_sync.py --sync-all --dry-run
```

### 4. Sync a Single Project

```bash
python basic_memory_sync.py --project main
```

### 5. Start Continuous Monitoring

```bash
python basic_memory_sync.py --monitor
```

## Configuration

### Project Configuration

Each Basic Memory project can be configured in `sync_config.ini`:

- `local_path`: Path to Basic Memory project files
- `github_repo`: Target GitHub repository (owner/repo)
- `github_path`: Subdirectory in GitHub repo (optional)
- `sync_enabled`: Enable/disable sync for this project

### Sync Settings

- `check_interval_seconds`: How often to check for changes (default: 300)
- `batch_size`: Maximum files to sync per run (default: 10)
- `commit_message_template`: Template for commit messages
- `exclude_patterns`: File patterns to ignore (comma-separated)
- `dry_run`: Test mode - show what would be synced without doing it

## Usage Examples

### Sync All Projects
```bash
# Dry run to see what would be synced
python basic_memory_sync.py --sync-all --dry-run

# Actually sync all projects
python basic_memory_sync.py --sync-all
```

### Sync Specific Project
```bash
python basic_memory_sync.py --project main
```

### Continuous Monitoring
```bash
# Monitor with default interval (5 minutes)
python basic_memory_sync.py --monitor

# Monitor with custom interval (1 minute)
python basic_memory_sync.py --monitor --interval 60
```

### Custom Configuration
```bash
python basic_memory_sync.py --config my_config.ini --sync-all
```

## Integration with Claude Desktop

This solution is designed to work alongside your existing Claude Desktop MCP setup:

1. **Basic Memory MCP** - Already configured for knowledge management
2. **GitHub MCP** - Already configured for repository access
3. **This Sync Tool** - Bridges the two automatically

### Required MCP Tools

Ensure you have these MCP servers configured in Claude Desktop:

```json
{
  "mcpServers": {
    "basic-memory": {
      "command": "uvx",
      "args": ["basic-memory", "mcp"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Workflow

### Automatic Sync Workflow

1. **File Change Detection**
   - Monitor Basic Memory project directories
   - Detect .md files modified recently
   - Filter out excluded file patterns

2. **Content Reading**
   - Read file contents from local filesystem
   - Maintain Basic Memory frontmatter and formatting

3. **GitHub Sync**
   - Create or update files in GitHub repository
   - Use meaningful commit messages with timestamps
   - Respect repository structure and paths

4. **Error Handling**
   - Log sync failures and retry logic
   - Skip problematic files and continue
   - Report sync statistics

### Manual Sync Options

- Sync individual projects on demand
- Dry-run mode for testing
- Force sync all files (not just recent changes)

## File Structure

```
basic-memory-sync/
├── basic_memory_sync.py      # Main sync script
├── sync_config.ini           # Configuration file
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
└── examples/
    ├── claude_integration.py # Claude MCP integration examples
    └── monitoring_setup.py   # System monitoring setup
```

## Troubleshooting

### Common Issues

**"No recent changes found"**
- Check that the local_path exists and contains .md files
- Verify file modification times are recent enough
- Try increasing the time window or forcing a full sync

**"GitHub authentication failed"**
- Verify your GitHub Personal Access Token is set correctly
- Check token permissions include repository access
- Test GitHub MCP tools separately in Claude Desktop

**"MCP tools not available"**
- Ensure Claude Desktop is running with MCP servers configured
- Test Basic Memory and GitHub tools individually
- Check Claude Desktop configuration file syntax

### Debug Mode

Run with verbose output to diagnose issues:

```bash
python basic_memory_sync.py --sync-all --dry-run --verbose
```

## Advanced Usage

### Custom Sync Strategies

You can extend the sync script to support:

- **Selective sync**: Only sync files with specific tags
- **Conditional sync**: Sync based on file content or metadata
- **Multi-repo sync**: Send different projects to different repositories
- **Branch-specific sync**: Sync to feature branches instead of main

### Integration with CI/CD

Set up automatic sync as part of your development workflow:

```yaml
# GitHub Action example
name: Basic Memory Sync
on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Basic Memory Sync
        run: python basic_memory_sync.py --sync-all
```

## Contributing

This sync solution is designed to be extensible:

1. **Fork the repository**
2. **Add new features** (e.g., different version control systems)
3. **Submit pull requests** with improvements
4. **Report issues** and suggest enhancements

## License

This project is open source. Use and modify as needed for your Basic Memory workflows.

---

## Next Steps

Once you have this basic sync working:

1. **Test with your actual Basic Memory projects**
2. **Integrate with actual MCP tools** (currently uses filesystem simulation)
3. **Set up monitoring and alerting** for sync failures
4. **Expand to support additional repositories** or sync targets
5. **Create automated deployment** for team use

The goal is to make Basic Memory -> GitHub sync completely transparent, so you can focus on building knowledge while everything stays automatically backed up and synchronized.
