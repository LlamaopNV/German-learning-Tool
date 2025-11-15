"""
Export statistics and push to GitHub
Automatically updates GitHub Pages dashboard
"""

import sys
from pathlib import Path
import subprocess
from datetime import datetime

# Add app to path
sys.path.append(str(Path(__file__).parent.parent / 'app'))

from analytics.exporter import get_stats_exporter
from config import GITHUB_CONFIG

def export_stats():
    """Export stats to JSON file"""
    print("📊 Exporting statistics...")
    exporter = get_stats_exporter()
    output_path = exporter.export_and_save()
    print(f"✓ Stats exported to: {output_path}")
    return output_path

def git_push_stats(retry_count=0):
    """
    Push stats to GitHub with exponential backoff retry

    Args:
        retry_count: Current retry attempt

    Returns:
        bool: Success status
    """
    if not GITHUB_CONFIG['auto_push']:
        print("⚠ Auto-push is disabled in config")
        return False

    max_retries = GITHUB_CONFIG['max_retries']
    branch = GITHUB_CONFIG['branch']

    try:
        # Stage the stats file
        print("📝 Staging stats.json...")
        subprocess.run(
            ['git', 'add', 'docs/data/stats.json'],
            check=True,
            capture_output=True
        )

        # Check if there are changes to commit
        result = subprocess.run(
            ['git', 'diff', '--cached', '--quiet'],
            capture_output=True
        )

        if result.returncode == 0:
            print("✓ No changes to commit - stats are up to date!")
            return True

        # Commit the changes
        commit_message = GITHUB_CONFIG['commit_message_template'].format(
            date=datetime.now().strftime('%Y-%m-%d %H:%M')
        )

        print(f"💾 Committing changes...")
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            check=True,
            capture_output=True
        )

        # Push to GitHub
        print(f"🚀 Pushing to GitHub (branch: {branch})...")
        push_result = subprocess.run(
            ['git', 'push', '-u', 'origin', branch],
            capture_output=True,
            text=True,
            timeout=30
        )

        if push_result.returncode == 0:
            print("✓ Successfully pushed stats to GitHub!")
            print("🌐 Your GitHub Pages dashboard will update automatically")
            return True
        else:
            # Check if it's a network error or auth issue
            if '403' in push_result.stderr or 'forbidden' in push_result.stderr.lower():
                print(f"❌ Push failed: Permission denied (403)")
                print("   Check that the branch name starts with 'claude/' and matches session ID")
                return False
            else:
                # Network error - retry
                raise subprocess.CalledProcessError(push_result.returncode, 'git push', push_result.stderr)

    except subprocess.CalledProcessError as e:
        if retry_count < max_retries:
            # Exponential backoff
            delay = GITHUB_CONFIG['retry_delays'][min(retry_count, len(GITHUB_CONFIG['retry_delays']) - 1)]
            print(f"⚠ Push failed, retrying in {delay}s... (attempt {retry_count + 1}/{max_retries})")

            import time
            time.sleep(delay)

            return git_push_stats(retry_count + 1)
        else:
            print(f"❌ Failed to push after {max_retries} retries")
            print(f"   Error: {e}")
            return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 50)
    print("German Learning Tool - Stats Export & Push")
    print("=" * 50)
    print()

    # Export stats
    stats_path = export_stats()

    print()

    # Push to GitHub
    success = git_push_stats()

    print()
    print("=" * 50)

    if success:
        print("✓ Stats successfully updated on GitHub Pages!")
        print("🌐 View your dashboard at:")
        print("   https://llamaopnv.github.io/German-learning-Tool/")
    else:
        print("⚠ Stats exported but not pushed to GitHub")
        print("  You can manually push with: git push")

    print("=" * 50)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
