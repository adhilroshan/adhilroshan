with open("wakatime_summary.txt", "r") as f:
    summary = f.read()

with open("README.md", "r") as f:
    readme = f.read()

start_marker = "<!--START_SECTION:recentwaka-->"
end_marker = "<!--END_SECTION:recentwaka-->"

start_index = readme.find(start_marker)
end_index = readme.find(end_marker)

if start_index != -1 and end_index != -1:
    # Extract the part before the start marker and after the end marker
    before = readme[: start_index + len(start_marker)]
    after = readme[end_index :]

    # Construct the new README content
    new_readme = f"{before}\n{summary}\n{after}"
else:
    print("Markers not found in README.md")
    exit(1) #exit the script with an error.

with open("README.md", "w") as f:
    f.write(new_readme)