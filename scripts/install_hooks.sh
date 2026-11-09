#!/bin/sh
# YON-20: install the pre-push scan hook for this clone (hooks are not versioned by git).
set -e
top=$(git rev-parse --show-toplevel)
cat > "$top/.git/hooks/pre-push" <<'HOOK'
#!/bin/sh
# YON-20 pre-push scan (installed by scripts/install_hooks.sh)
exec python3 "$(git rev-parse --show-toplevel)/scripts/prepush_scan.py" --hook "$@"
HOOK
chmod +x "$top/.git/hooks/pre-push"
echo "YON-20 pre-push hook installed: $top/.git/hooks/pre-push"
