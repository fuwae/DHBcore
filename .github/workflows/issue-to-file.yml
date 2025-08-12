name: Issue to File

on:
  issues:
    types: [opened, edited]
  workflow_dispatch:
    inputs:
      path:
        description: 'Path to write (e.g. 02_Work_In_Progress/background_loop_prototype.md)'
        required: true
      content:
        description: 'File content (raw)'
        required: true

permissions:
  contents: write
  issues: read

jobs:
  write-from-issue:
    if: github.event_name == 'issues' && startsWith(github.event.issue.title, 'push:')
    runs-on: ubuntu-latest
    steps:
      - name: Create or update file from ISSUE
        uses: actions/github-script@v7
        with:
          script: |
            const title = context.payload.issue.title;
            const path = title.replace(/^push:\s*/, '').trim();
            const body = context.payload.issue.body || '';
            const owner = context.repo.owner;
            const repo = context.repo.repo;

            // base64 encode
            const content = Buffer.from(body, 'utf8').toString('base64');

            // get existing sha if file already exists
            let sha = undefined;
            try {
              const { data } = await github.repos.getContent({ owner, repo, path });
              if (!Array.isArray(data)) sha = data.sha;
            } catch (e) { /* file not found -> new */ }

            await github.repos.createOrUpdateFileContents({
              owner, repo, path,
              message: `chore: update via issue -> ${path}`,
              content,
              sha,
              committer: { name: 'Fuwae Bot', email: 'bot@example.com' },
              author: { name: 'Fuwae Bot', email: 'bot@example.com' }
            });

  write-from-dispatch:
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - name: Create or update file from DISPATCH
        uses: actions/github-script@v7
        with:
          script: |
            const path = core.getInput('path');
            const contentRaw = core.getInput('content');
            const owner = context.repo.owner;
            const repo = context.repo.repo;

            const content = Buffer.from(contentRaw, 'utf8').toString('base64');

            let sha = undefined;
            try {
              const { data } = await github.repos.getContent({ owner, repo, path });
              if (!Array.isArray(data)) sha = data.sha;
            } catch (e) {}

            await github.repos.createOrUpdateFileContents({
              owner, repo, path,
              message: `chore: update via dispatch -> ${path}`,
              content,
              sha,
              committer: { name: 'Fuwae Bot', email: 'bot@example.com' },
              author: { name: 'Fuwae Bot', email: 'bot@example.com' }
            });
