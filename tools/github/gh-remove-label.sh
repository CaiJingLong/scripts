gh issue list -l 'await triage' -s closed --json number | jq '.[].number' | xargs -I {}  gh issue edit {} --remove-label  'await triage'
