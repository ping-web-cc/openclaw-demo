"""Seed the database with the 6 existing crontab tasks.

Run inside the container:
    python seed.py
"""
import sys

from app import create_app
from app.models import Task, db
from app.scheduler import sync_all_jobs

SEED_TASKS = [
    {
        'name': 'Backup OpenClaw (Personal + Work)',
        'description': 'tar.gz backup of ~/.openclaw-personal and ~/.openclaw-work, upload to Google Drive, clean old backups (keep 7)',
        'cron_expr': '0 3 * * *',
        'command': (
            '/host_home/.openclaw-personal/.claude/skills/backup/scripts/backup.sh /host_home backup all && '
            '/host_home/.openclaw-personal/.claude/skills/backup/scripts/backup.sh /host_home upload all && '
            '/host_home/.openclaw-personal/.claude/skills/backup/scripts/backup.sh /host_home clean all 7'
        ),
        'working_dir': '/host_home',
        'timeout_secs': 1800,
        'enabled': True,
    },
    {
        'name': 'Memory to LanceDB + Cleanup',
        'description': 'Scan OpenClaw workspace memory dirs, extract important memories to LanceDB via agent, clean processed files',
        'cron_expr': '30 7 * * *',
        'command': '/host_home/.openclaw-personal/.claude/skills/memory-cleanup/scripts/memory_to_lancedb.sh',
        'working_dir': '/host_home',
        'timeout_secs': 600,
        'enabled': True,
    },
    {
        'name': 'Claude Code Session Cleanup',
        'description': 'Clean empty/minimal session memory files across Claude Code workspace agents',
        'cron_expr': '35 7 * * *',
        'command': '/host_home/.openclaw-personal/.claude/skills/memory-cleanup/scripts/clean_memory.sh clean',
        'working_dir': '/host_home',
        'timeout_secs': 300,
        'enabled': True,
    },
    {
        'name': 'OpenClaw Rebuild',
        'description': 'Fetch latest stable release tag, rebuild Docker image, restart services',
        'cron_expr': '0 4 */2 * *',
        'command': '/host_home/.openclaw-personal/.claude/skills/openclaw-rebuild/scripts/rebuild.sh',
        'working_dir': '/host_home',
        'timeout_secs': 3600,
        'enabled': True,
    },
    {
        'name': 'Docker Cleanup',
        'description': 'Remove old dangling Docker images, keeping newest 7',
        'cron_expr': '30 4 */2 * *',
        'command': '/host_home/.openclaw-personal/.claude/skills/docker-cleanup/scripts/cleanup.sh clean',
        'working_dir': '/host_home',
        'timeout_secs': 300,
        'enabled': True,
    },
    {
        'name': 'Backup Cron Dashboard DB',
        'description': 'SQLite backup of /data/cron_dashboard.db, upload to Google Drive (gdrive:backups/cron-dashboard), keep 7 copies',
        'cron_expr': '15 3 * * *',
        'command': '/host_home/.openclaw-personal/.claude/skills/backup/scripts/backup_cron_db.sh',
        'working_dir': '/host_home',
        'timeout_secs': 300,
        'enabled': True,
    },
]


def seed():
    app = create_app()
    with app.app_context():
        if Task.query.count() > 0:
            print(f'Database already has {Task.query.count()} tasks, skipping seed.')
            return

        for data in SEED_TASKS:
            task = Task(**data)
            db.session.add(task)
            print(f'  + {task.name}')

        db.session.commit()
        sync_all_jobs()
        print(f'Seeded {len(SEED_TASKS)} tasks.')


if __name__ == '__main__':
    seed()
