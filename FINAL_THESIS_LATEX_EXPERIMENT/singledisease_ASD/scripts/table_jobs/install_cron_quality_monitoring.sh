#!/bin/bash
# Installs (idempotently) the new quality-monitoring audits in cron.
# Tag: # QUALITY-MONITORING (asd-dissertation)
# Schedule: twice daily at 11:30 and 23:30 (offset from other audits at :00 / :15 / :45)

set -e

PROJECT="/media/praveen/Asthana3/ upgrad/synopysis/FINAL_THESIS_LATEX_EXPERIMENT/singledisease_ASD"
TAG="# QUALITY-MONITORING (asd-dissertation)"

# Build new cron lines (run from project root so all paths resolve)
CRON_NEW=$(cat <<EOF
$TAG
30 11 * * * cd "$PROJECT" && python3 scripts/table_jobs/audit_figure_clarity_per_chapter.py >> jobs/logs/quality_monitoring.log 2>&1
35 11 * * * cd "$PROJECT" && python3 scripts/table_jobs/audit_page_break_causes.py >> jobs/logs/quality_monitoring.log 2>&1
40 11 * * * cd "$PROJECT" && python3 scripts/table_jobs/audit_right_side_space.py >> jobs/logs/quality_monitoring.log 2>&1
30 23 * * * cd "$PROJECT" && python3 scripts/table_jobs/audit_figure_clarity_per_chapter.py >> jobs/logs/quality_monitoring.log 2>&1
35 23 * * * cd "$PROJECT" && python3 scripts/table_jobs/audit_page_break_causes.py >> jobs/logs/quality_monitoring.log 2>&1
40 23 * * * cd "$PROJECT" && python3 scripts/table_jobs/audit_right_side_space.py >> jobs/logs/quality_monitoring.log 2>&1
EOF
)

# Strip any old QUALITY-MONITORING block, then append
EXISTING=$(crontab -l 2>/dev/null || true)
# Remove tag block: anything between "$TAG" line and next blank/tag line
CLEANED=$(echo "$EXISTING" | awk -v tag="$TAG" '
    BEGIN {skip=0}
    $0 == tag {skip=1; next}
    skip && /^#/ && $0 != tag {skip=0}
    !skip {print}
')

# Re-install
mkdir -p "$PROJECT/jobs/logs"
{
    echo "$CLEANED"
    echo "$CRON_NEW"
} | crontab -

echo "Cron updated. Quality-monitoring audits scheduled at 11:30/35/40 and 23:30/35/40."
echo "Verify with: crontab -l | grep QUALITY-MONITORING"
