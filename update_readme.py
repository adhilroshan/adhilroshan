import re
import sys

MAX_SUMMARY_LENGTH = 2000  # Maximum length for AI-generated summary

def sanitize_summary(summary):
    """
    Sanitize AI-generated summary to prevent malicious content injection.
    Validates length, removes dangerous patterns, and ensures safe content.
    """
    # Length limit to prevent abuse
    if len(summary) > MAX_SUMMARY_LENGTH:
        summary = summary[:MAX_SUMMARY_LENGTH] + "..."
        print(f"Warning: Summary truncated to {MAX_SUMMARY_LENGTH} characters", file=sys.stderr)

    # Remove potentially dangerous patterns
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'<iframe[^>]*>.*?</iframe>',  # Iframe tags
        r'javascript:',                 # JavaScript URIs
        r'on\w+\s*=',                   # Event handlers (onclick, onerror, etc.)
        r'<object[^>]*>.*?</object>',  # Object tags
        r'<embed[^>]*>',                # Embed tags
    ]

    for pattern in dangerous_patterns:
        summary = re.sub(pattern, '', summary, flags=re.IGNORECASE | re.DOTALL)

    # Validate summary is not empty after sanitization
    if not summary.strip():
        raise ValueError("Summary is empty after sanitization")

    return summary.strip()

# Read and validate summary file
try:
    with open("wakatime_summary.txt", "r") as f:
        raw_summary = f.read()
except FileNotFoundError:
    print("Error: wakatime_summary.txt not found", file=sys.stderr)
    sys.exit(1)

# Sanitize the summary
try:
    summary = sanitize_summary(raw_summary)
except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

# Read README file
try:
    with open("README.md", "r") as f:
        readme = f.read()
except FileNotFoundError:
    print("Error: README.md not found", file=sys.stderr)
    sys.exit(1)

start_marker = "<!--START_SECTION:recentwaka-->"
end_marker = "<!--END_SECTION:recentwaka-->"

start_index = readme.find(start_marker)
end_index = readme.find(end_marker)

if start_index != -1 and end_index != -1:
    # Validate marker positions
    if start_index >= end_index:
        print("Error: Invalid marker positions in README.md", file=sys.stderr)
        sys.exit(1)

    # Extract the part before the start marker and after the end marker
    before = readme[: start_index + len(start_marker)]
    after = readme[end_index :]

    # Construct the new README content
    new_readme = f"{before}\n{summary}\n{after}"

    # Validate new README is not empty
    if not new_readme.strip():
        print("Error: Generated README is empty", file=sys.stderr)
        sys.exit(1)

    # Write updated README
    try:
        with open("README.md", "w") as f:
            f.write(new_readme)
        print("✓ Successfully updated README")
    except IOError as e:
        print(f"Error writing README.md: {e}", file=sys.stderr)
        sys.exit(1)
else:
    print("Error: Markers not found in README.md", file=sys.stderr)
    print(f"  Looking for: {start_marker} and {end_marker}", file=sys.stderr)
    sys.exit(1)