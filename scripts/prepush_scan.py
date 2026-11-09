#!/usr/bin/env python3
"""YON-20 — ell-docs pre-push scan (Sentez 9 Kas). ell-docs is PUBLIC: before every push, the outgoing changes are scanned.

What is scanned: the commit messages and the ADDED lines of every commit being pushed (history already on the remote is not
re-scanned). A match blocks the push (exit 1) and is reported masked (kind + first 2 characters + length — K4); nothing is fixed
automatically.

Patterns:
  connection string   postgres:// / postgresql:// followed by a value
  API key             sk-<20+ key characters>
  token value         token=<8+ value characters>
  IBAN                2 letters + 2 digits + 12-30 alphanumerics (spaces allowed in groups of 4)
  TABAN value         amounts on the "TABAN-N" lines (N >= 2) of LEENA's PRIVATE CLAUDE.md, read at scan time and never written
                      here (GOC-07). The base TABAN (contract 4) is public since Paket 1 and appears in Sentez texts written
                      verbatim — not blocked (SAPMA, defter 9 Kas).
  e-mail address      any address outside the tenant domain elan-expo.com; "Co-Authored-By:" commit trailers are skipped.
A bare pattern name without a value ("postgres://," "sk-," "token=,") is NOT a match — the rule text itself must stay writable.

Usage:
  scripts/prepush_scan.py --hook <remote> <url>    (git pre-push hook; ref lines on stdin)
  scripts/prepush_scan.py --range A..B             (manual)
  scripts/prepush_scan.py --self-test              (synthetic matches + non-matches)
Install: scripts/install_hooks.sh (writes .git/hooks/pre-push).
"""
import os
import re
import subprocess
import sys

TENANT_DOMAIN = 'elan-expo.com'
LEENA_CLAUDE_MD = os.environ.get('LEENA_CLAUDE_MD',
                                 os.path.expanduser('~/Desktop/Leena_Projesi/Leena_v401_monorepo/CLAUDE.md'))
ZERO = '0' * 40

PATTERNS = [
    ('connection string', re.compile(r'postgres(?:ql)?://[^\s,;)\]>\'"`]+')),
    ('API key', re.compile(r'\bsk-[A-Za-z0-9_\-]{20,}')),
    ('token value', re.compile(r'token=[A-Za-z0-9._~%+/\-]{8,}')),
    ('IBAN', re.compile(r'\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}(?: ?[A-Z0-9]{1,3})?\b')),
]
EMAIL = re.compile(r'[A-Za-z0-9._%+\-]+@([A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,})')


def taban_values(path=LEENA_CLAUDE_MD):
    """Amounts on the TABAN-N (N >= 2) lines of LEENA's private CLAUDE.md, as literal strings (dot and comma decimal)."""
    if not os.path.exists(path):
        raise SystemExit(f'YON-20: LEENA CLAUDE.md not found ({path}) — set LEENA_CLAUDE_MD; push blocked.')
    vals = set()
    for line in open(path, encoding='utf-8'):
        if re.match(r'\s*-\s*\*\*TABAN-\d+', line):
            for m in re.finditer(r'\b\d+\.\d{2}\b', line):
                vals.add(m.group(0))
                vals.add(m.group(0).replace('.', ','))
    if not vals:
        raise SystemExit('YON-20: no TABAN-N value found in LEENA CLAUDE.md — push blocked (check the file).')
    return vals


def mask(s):
    return f'{s[:2]}… ({len(s)} chars)'


def scan_text(text, where, taban):
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for kind, rx in PATTERNS:
            for m in rx.finditer(line):
                hits.append((where, n, kind, mask(m.group(0))))
        for v in taban:
            if re.search(r'(?<![\d.,])' + re.escape(v) + r'(?![\d])', line):
                hits.append((where, n, 'TABAN value', mask(v)))
        if not line.lstrip().lower().startswith('co-authored-by:'):
            for m in EMAIL.finditer(line):
                dom = m.group(1).lower()
                if dom != TENANT_DOMAIN and not dom.endswith('.' + TENANT_DOMAIN):
                    hits.append((where, n, 'e-mail address', mask(m.group(0))))
    return hits


def git(*args):
    return subprocess.run(['git', *args], check=True, capture_output=True, text=True).stdout


def scan_range(rev_args, taban):
    """rev_args: arguments for git rev-list selecting the outgoing commits."""
    hits = []
    commits = [c for c in git('rev-list', '--reverse', *rev_args).split() if c]
    for c in commits:
        short = c[:7]
        hits += scan_text(git('log', '-1', '--format=%B', c), f'{short} commit message', taban)
        diff = git('show', '--format=', '--unified=0', '--no-color', '--no-ext-diff', c)
        cur = None
        added = {}
        for line in diff.splitlines():
            if line.startswith('+++ '):
                cur = line[6:] if line.startswith('+++ b/') else line[4:]
            elif line.startswith('+') and cur and cur != '/dev/null':
                added.setdefault(cur, []).append(line[1:])
        for f, lines in added.items():
            hits += scan_text('\n'.join(lines), f'{short} {f} (added line)', taban)
    return commits, hits


def report(commits, hits):
    if hits:
        print(f'YON-20: {len(hits)} match(es) in {len(commits)} outgoing commit(s) — PUSH BLOCKED (values masked):', file=sys.stderr)
        for where, n, kind, m in hits:
            print(f'  {kind:16} {where} · line {n} · {m}', file=sys.stderr)
        return 1
    print(f'YON-20: {len(commits)} outgoing commit(s) scanned — 0 matches.')
    return 0


def self_test():
    taban = taban_values()
    one = sorted(v for v in taban if '.' in v)[0]
    pos = {
        'connection string': 'see postgres' + 'ql://user:pw@host/db for details',
        'API key': 'key ' + 'sk-' + 'ant-api03-AbCdEfGhIjKlMnOpQrStUv',
        'token value': 'url?to' + 'ken=abcdef1234567890',
        'IBAN': 'pay to TR33 0006 ' + '1005 1978 6457 8413 26 today',
        'TABAN value': 'TABAN-2 earned = ' + one + ' EUR',
        'e-mail address': 'write to someone' + '@example.org',
    }
    neg = [
        'bağlantı dizesi/anahtar desenleri (postgres://, sk-, token=, IBAN)',
        'a risk-free plan · desk-top · Task-12',
        'TABAN 342.00 ✅ · TABAN-2 EŞİT ✅',
        'cc-owner@elan-expo.com · su…@elan-expo.com',
        'Co-Authored-By: Claude <noreply' + '@anthropic.com>',
        'commit a5bafb1 · AF489555 · KES-01 · /ui2/invite.html#token=…',
    ]
    ok = True
    for kind, s in pos.items():
        got = {h[2] for h in scan_text(s, 'self-test', taban)}
        good = kind in got
        ok &= good
        print(f'  {"✅" if good else "❌"} match    {kind}')
    for s in neg:
        got = scan_text(s, 'self-test', taban)
        good = not got
        ok &= good
        print(f'  {"✅" if good else "❌"} no match {s[:60]!r}' + ('' if good else f' → {got}'))
    print('YON-20 self-test:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main(argv):
    if '--self-test' in argv:
        return self_test()
    taban = taban_values()
    if '--range' in argv:
        rng = argv[argv.index('--range') + 1]
        return report(*scan_range([rng], taban))
    if '--hook' in argv:
        commits, hits = [], []
        for line in sys.stdin.read().splitlines():
            parts = line.split()
            if len(parts) != 4:
                continue
            _lref, lsha, _rref, rsha = parts
            if lsha == ZERO:
                continue                                  # branch deletion — nothing outgoing
            rev = [lsha, '--not', '--remotes'] if rsha == ZERO else [f'{rsha}..{lsha}']
            c, h = scan_range(rev, taban)
            commits += c
            hits += h
        return report(commits, hits)
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
